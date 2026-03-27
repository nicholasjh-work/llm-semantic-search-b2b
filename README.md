<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/nh-logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/nh-logo-light.svg">
    <img alt="NH" src="assets/nh-logo-dark.svg" width="80">
  </picture>
</p>

<h1 align="center">LLM Semantic Search for B2B eCommerce</h1>
<p align="center">
  <strong>Local AI-powered semantic search that maps natural language to structured product filters</strong>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="License"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Ollama-000000?style=flat&logo=ollama&logoColor=white" alt="Ollama">
  <img src="https://img.shields.io/badge/Llama_3.1-0467DF?style=flat&logo=meta&logoColor=white" alt="Llama 3.1">
  <img src="https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white" alt="Pandas">
</p>

---

Designed for a B2B office-supplies digital catalog. Runs entirely offline using [Ollama](https://ollama.ai) and a fine-tuned Llama 3.1 8B model. The Flask backend parses search intent, applies business logic, and filters results from a simulated product dataset.

Built and optimized for Apple Silicon (M4, 16GB).

---

### Key features

- Local LLM inference via Ollama (no external API required)
- Flask-based backend for clean and modular integration
- Semantic understanding of unstructured product queries
- Structured JSON output for B2B product catalog search

---

### How it works

1. User enters a natural-language query such as _"eco-friendly printer paper under $30"_
2. The Flask API sends it to the local Ollama LLM
3. The model interprets the query and extracts structured filters (category, price, eco_friendly, etc.)
4. The backend applies those filters to a mock Staples-style product catalog
5. Returns semantic results as structured JSON

---

### Run locally

```bash
# Start Ollama
ollama serve
ollama pull llama3.1:8b

# Run backend
cd backend
source venv/bin/activate
python app.py
```

---

### Project structure

```
llm-semantic-search-b2b/
├── assets/
│   ├── nh-logo-dark.svg
│   └── nh-logo-light.svg
├── backend/
│   ├── app.py
│   ├── venv/
│   └── ...
├── README.md
├── requirements.txt
└── LICENSE
```

---

### Related repos

- [subscription-financial-model](https://github.com/nicholasjh-work/subscription-financial-model) - Churn, retention, and revenue analytics (dbt + Streamlit)
- [feature-adoption-retention](https://github.com/nicholasjh-work/feature-adoption-retention) - Feature engagement and retention cohorts (dbt + Snowflake)
- [llm-text-to-sql-finance](https://github.com/nicholasjh-work/llm-text-to-sql-finance) - Governed NL-to-SQL for finance teams

---

<p align="center">
  <a href="https://linkedin.com/in/nicholashidalgo"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>&nbsp;
  <a href="https://nicholashidalgo.com"><img src="https://img.shields.io/badge/Website-000000?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Website"></a>&nbsp;
  <a href="mailto:analytics@nicholashidalgo.com"><img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"></a>
</p>
