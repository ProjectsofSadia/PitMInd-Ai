"""Prompt templates for the optional LLM narration layer (prompt-engineering artifact).

The assistant is grounded: the LLM may ONLY use retrieved context and must
abstain when the context does not answer the question (responsible-AI guardrail).
"""
SYSTEM = (
    "You are a Formula 1 race-engineering assistant. Answer ONLY from the provided "
    "context passages. If the context does not contain the answer, say you don't have "
    "a grounded answer. Never invent numbers, results, or facts. Cite the passage titles used."
)

def build_prompt(question: str, passages: list) -> str:
    ctx = "\n\n".join(f"[{p['doc']['title']}] {p['doc']['text']}" for p in passages)
    return f"{SYSTEM}\n\nContext:\n{ctx}\n\nQuestion: {question}\n\nGrounded answer:"
