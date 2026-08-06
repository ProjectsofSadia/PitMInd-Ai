# PitMind AI
An AI race-engineering assistant: ask race-engineering questions in natural language and get
data-grounded, source-cited answers.

## What it does
- **Retrieval** - TF-IDF vector index + cosine similarity over a motorsport knowledge corpus (the R in RAG).
- **Grounded answers** - returns an answer built from retrieved passages, always with its sources.
- **Responsible AI** - abstains ("I don't have a grounded answer") when retrieval is not confident,
  instead of guessing - a hallucination guard.
- **Response validation** - a grounded answer must cite at least one source or it's rejected.
- **LLM-optional** - works fully without an LLM (extractive grounded answer); pass an `llm` callable
  and it narrates strictly from the retrieved context via a documented, guard-railed prompt.

## Measured results (reproducible - run the tests)
Retrieval evaluated on a 10-query labeled gold set over the sample corpus (`GET /evaluate`):
- **precision@1, recall@k, and MRR** are computed by running retrieval, not asserted.
- On this small, clean corpus retrieval scores at the top of the range; the value is the
  **evaluation harness** - the same metrics hold up as the corpus grows.

## Honest limitations
- Retrieval is **lexical (TF-IDF)**: it can be fooled by a shared rare word (e.g. an off-domain query
  containing "best" can match a passage about "best sectors"). Genuinely off-domain queries with no
  lexical overlap score 0 and correctly abstain. Dense embeddings (sentence-transformers) are the fix - see roadmap.
- The LLM narration layer is wired but not called here (no API key in this environment); the assistant
  is fully functional without it.

## Run the full app
```bash
cd backend
python -m pip install -r requirements.txt
python -m pytest -q                       # 7 passed
python -m uvicorn app.main:app --reload   # API + docs at http://localhost:8000/docs
```
Then open **frontend/index.html** in your browser - a chat UI that asks the assistant,
shows the grounded answer with its sources, and displays the retrieval-eval metrics.
Docker: `docker build -t pitmind backend && docker run -p 8000:8000 pitmind`.

## Structure
```
backend/   FastAPI API, TF-IDF retrieval, assistant, LLM adapter, ingestion, tests
frontend/  index.html  - chat web app (no build step)
backend/Dockerfile
```

## Real data (Jolpica/Ergast - no scraping) + LLM
Base corpus is knowledge docs; add REAL race results:
```bash
python -m pip install httpx
python -m app.ingest --year 2024 --rounds 1 2 3   # -> data/corpus.json (auto-loaded)
```
Enable LLM narration (optional) by setting a key - the assistant then narrates strictly
from retrieved context; without a key it returns the deterministic grounded answer:
```bash
setx ANTHROPIC_API_KEY "sk-..."      # or OPENAI_API_KEY
python -m pip install anthropic       # or openai
```

## Tech
Python, FastAPI, scikit-learn (TF-IDF retrieval), pandas, httpx. LLM-ready (OpenAI/Claude via
app/llm.py); FAISS/Chroma are drop-in retrieval backends at scale.

## Roadmap
- Dense embeddings (sentence-transformers) + FAISS/Chroma; ingest real public race reports;
  LLM narration with faithfulness / hallucination-rate evaluation and citation checking.
