# LLM Semantic Search Demo (Local)

- Backend: Flask + Pandas
- Local LLM: Ollama (llama3.1:8b) on Mac M4
- Purpose: Map natural-language product queries to structured filters for a B2B office-supplies catalog.

## Run backend

```bash
# 1) start ollama
ollama serve
ollama pull llama3.1:8b

# 2) backend
cd backend
source ven/bin/activate
python app.py

