from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import requests
import json
import re

app = Flask(__name__)
CORS(app, resources={r"/query": {"origins": "*"}})

# -----------------------------
# Local LLM config (Ollama)
# -----------------------------
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL_NAME = "llama3.1:8b"  # matches what you pulled

# -----------------------------
# Mock Staples-style product catalog
# -----------------------------
data = [
    {
        "product_id": 101,
        "name": "Recycled Printer Paper",
        "category": "Paper",
        "eco_friendly": True,
        "compatible_with": None,
        "price": 22.99,
    },
    {
        "product_id": 102,
        "name": "Glossy 11x17 Photo Paper",
        "category": "Paper",
        "eco_friendly": False,
        "compatible_with": None,
        "price": 35.99,
    },
    {
        "product_id": 103,
        "name": "HP LaserJet Pro 400 Ink",
        "category": "Ink Cartridges",
        "eco_friendly": False,
        "compatible_with": "HP LaserJet Pro 400",
        "price": 89.99,
    },
    {
        "product_id": 104,
        "name": "Breakroom Supplies Pack (25p)",
        "category": "Breakroom",
        "eco_friendly": False,
        "compatible_with": None,
        "price": 109.99,
    },
    {
        "product_id": 105,
        "name": "Eco-Friendly Coffee Cups",
        "category": "Breakroom",
        "eco_friendly": True,
        "compatible_with": None,
        "price": 18.50,
    },
]

catalog = pd.DataFrame(data)

# -----------------------------
# Helpers for JSON parsing
# -----------------------------
STRICT_SYSTEM_PROMPT = (
    "You map natural language B2B office supply queries to JSON filters.\n"
    "Return ONLY valid minified JSON with keys:\n"
    "  category (string|null), eco_friendly (true|false|null),\n"
    "  compatible_with (string|null), keywords (array of strings).\n"
    "Rules:\n"
    "- Use category values from this set when possible: "
    "['Paper', 'Ink Cartridges', 'Breakroom'].\n"
    "- Only set compatible_with when the user mentions a specific device "
    "model like 'HP LaserJet Pro 400'. Do NOT use generic words like 'printer'.\n"
    "- If the user asks for paper for printers, set category='Paper' and "
    "compatible_with=null.\n"
    "- keywords should be important words from the query.\n"
    "No prose, no markdown, no code fences. Return JSON only."
)

JSON_OBJECT_REGEX = re.compile(r"\{[\s\S]*\}")


def parse_llm_json(content: str):
    raw = content.strip()
    try:
        return json.loads(raw), raw
    except Exception:
        pass

    if raw.startswith("```"):
        raw_no_fence = raw.strip("`")
        try:
            return json.loads(raw_no_fence), raw
        except Exception:
            match = JSON_OBJECT_REGEX.search(raw_no_fence)
            if match:
                candidate = match.group(0)
                try:
                    return json.loads(candidate), raw
                except Exception:
                    pass

    match = JSON_OBJECT_REGEX.search(raw)
    if match:
        candidate = match.group(0)
        try:
            return json.loads(candidate), raw
        except Exception:
            pass

    return None, raw


def coerce_filters(d: dict):
    out = {
        "category": None,
        "eco_friendly": None,
        "compatible_with": None,
        "keywords": [],
    }
    if not isinstance(d, dict):
        return out

    if isinstance(d.get("category"), str) and d["category"].strip():
        out["category"] = d["category"].strip()

    eco = d.get("eco_friendly")
    if isinstance(eco, bool) or eco is None:
        out["eco_friendly"] = eco

    if isinstance(d.get("compatible_with"), str) and d["compatible_with"].strip():
        out["compatible_with"] = d["compatible_with"].strip()

    kw = d.get("keywords")
    if isinstance(kw, list):
        out["keywords"] = [str(x) for x in kw]

    return out


# -----------------------------
# Call local LLM (Ollama)
# -----------------------------
def call_local_llm(user_query: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": STRICT_SYSTEM_PROMPT},
            {"role": "user", "content": user_query},
        ],
        "stream": False,
    }
    resp = requests.post(OLLAMA_URL, json=payload, timeout=120)
    resp.raise_for_status()
    data = resp.json()
    # Ollama chat API returns { "message": { "role": "...", "content": "..." }, ... }
    content = data.get("message", {}).get("content", "")
    return content


# -----------------------------
# Routes
# -----------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"ok": True})


@app.route("/query", methods=["POST"])
def query():
    payload = request.get_json(silent=True) or {}
    user_input = str(payload.get("query", "")).strip()

    if not user_input:
        return jsonify({"error": "Missing 'query' in request body"}), 400

    try:
        llm_output = call_local_llm(user_input)
    except Exception as e:
        return jsonify({"error": f"Local LLM call failed: {e}"}), 502

    filters_dict, raw = parse_llm_json(llm_output)
    if filters_dict is None:
        return jsonify(
            {"error": "LLM response could not be parsed", "raw": raw}
        ), 400

    # from here on, we assume we have a valid dict
    filters = coerce_filters(filters_dict)
    filtered = catalog.copy()

    # 1) Category filter (exact match on known categories)
    if filters["category"]:
        filtered = filtered[
            filtered["category"].str.lower() == filters["category"].lower()
        ]

    # 2) Eco friendly filter
    if filters["eco_friendly"] is not None:
        filtered = filtered[filtered["eco_friendly"] == filters["eco_friendly"]]

    # 3) compatible_with: use a loose substring match instead of strict equality
    if filters["compatible_with"]:
        filtered = filtered[
            filtered["compatible_with"]
            .fillna("")
            .str.contains(filters["compatible_with"], case=False)
        ]

    # 4) Fallback: if nothing left, fall back to a simple keyword search
    if filtered.empty and filters["keywords"]:
        keywords_text = " ".join(filters["keywords"]).lower()
        # Very simple heuristic: for now, prioritize "paper" in the name
        if "paper" in keywords_text:
            filtered = catalog[
                catalog["name"].str.lower().str.contains("paper")
            ]
        else:
            # generic fallback: any name containing any keyword
            filtered = catalog[
                catalog["name"].str.lower().str.contains(
                    "|".join([k.lower() for k in filters["keywords"]])
                )
            ]

    return jsonify(
        {
            "filters": filters,
            "results": filtered.to_dict(orient="records"),
        }
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5080, debug=True)
