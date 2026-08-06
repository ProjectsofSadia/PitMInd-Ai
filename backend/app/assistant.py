"""PitMind assistant — grounded NL answers over the corpus.

Compute-then-narrate + responsible AI: retrieve, and only answer when retrieval
is confident; otherwise abstain (guards against hallucination). Works fully
WITHOUT an LLM (extractive grounded answer); an LLM can narrate the same context
via prompts.build_prompt. Every answer carries its sources.
"""
from __future__ import annotations
from app.retrieval import Retriever
from app.corpus import load_corpus
from app import prompts

MIN_SCORE = 0.08          # abstain threshold (responsible AI)
_R = Retriever(load_corpus())


def answer(question: str, k: int = 3, llm=None) -> dict:
    hits = _R.search(question, k=k)
    top = hits[0] if hits else None
    if not top or top["score"] < MIN_SCORE:
        return {"grounded": False, "answer": "I don't have a grounded answer for that in the current sources.",
                "sources": [], "retrieval": hits}
    sources = [{"title": h["doc"]["title"], "score": h["score"]} for h in hits if h["score"] >= MIN_SCORE]
    if llm is not None:                                     # optional LLM narration over grounded context
        text = llm(prompts.build_prompt(question, hits))
    else:                                                   # deterministic extractive grounded answer
        text = top["doc"]["text"]
    return {"grounded": True, "answer": text, "sources": sources, "retrieval": hits}


def validate(result: dict) -> bool:
    """Response validation: a grounded answer must cite at least one source."""
    return (not result["grounded"]) or len(result["sources"]) >= 1


def report(question: str) -> str:
    """Engineering-report style structured output for a question."""
    r = answer(question)
    if not r["grounded"]:
        return r["answer"]
    cites = ", ".join(s["title"] for s in r["sources"])
    return f"Question: {question}\nAnswer: {r['answer']}\nSources: {cites}"
