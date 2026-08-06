"""PitMind AI API — grounded race-engineering assistant."""
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app import assistant, evaluate
from app.llm import make_llm
_LLM = make_llm()
from app.corpus import DOCS

app = FastAPI(title="PitMind AI", version="1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
def health(): return {"ok": True, "documents": len(DOCS), "llm": _LLM is not None}

class Ask(BaseModel):
    question: str

@app.post("/ask")
def ask(body: Ask): return assistant.answer(body.question, llm=_LLM)

@app.post("/report")
def report(body: Ask): return {"report": assistant.report(body.question)}

@app.get("/evaluate")
def evaluate_retrieval(): return evaluate.evaluate()
