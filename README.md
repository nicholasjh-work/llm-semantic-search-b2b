#  LLM Semantic Search for B2B eCommerce

This project demonstrates a **local AI-powered semantic search system** that interprets natural language queries and maps them to structured product filters — designed for a **B2B office-supplies digital catalog**.

Built for **Mac M4**, this system runs **entirely offline** using [Ollama](https://ollama.ai) and a fine-tuned **Llama 3.1 8B** model.  
It integrates with a **Flask backend** that parses search intent, applies business logic, and filters results from a simulated product dataset.

---

###  Key Features
- Local **LLM inference** via Ollama (no external API required)
- **Flask-based backend** for clean and modular integration
- **Semantic understanding** of unstructured product queries
- **Structured JSON output** for B2B product catalog search
- Built and optimized for **Apple Silicon (M4, 16GB)**

---

###  Tech Stack
| Layer | Technology |
|-------|-------------|
| LLM Engine | Ollama (Llama 3.1:8B Q4) |
| Backend | Flask, Pandas |
| Deployment | Localhost (Mac M4) |
| Language | Python 3.11 |
| Architecture | Semantic Search via JSON filters |

---

###  How It Works
1. User enters a natural-language query such as  
   _“eco-friendly printer paper under $30”_
2. The Flask API sends it to the **local Ollama LLM**
3. The model interprets the query and extracts structured filters (category, price, eco_friendly, etc.)
4. The backend applies those filters to a mock Staples-style product catalog
5. Returns semantic results as structured JSON

---

###  Run Backend Locally

```bash
# Start Ollama
ollama serve
ollama pull llama3.1:8b

# Run backend
cd backend
source ven/bin/activate
python app.py
