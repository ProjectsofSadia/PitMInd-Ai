"""PitMind retrieval evaluation — real, reproducible metrics on a labeled set.

Small gold set (query -> relevant doc id). Reports precision@1, recall@k, and
MRR. These are measured by running retrieval, not asserted.
"""
from __future__ import annotations
from app.retrieval import Retriever
from app.corpus import DOCS

GOLD = [
    ("what is an undercut", "d2"),
    ("how do tyres degrade", "d1"),
    ("explain stint analysis", "d4"),
    ("how is lap time consistency measured", "d5"),
    ("what is the sum of best sectors", "d6"),
    ("when should I pit under a safety car", "d11"),
    ("how does fuel load affect lap time", "d10"),
    ("one stop versus two stop", "d15"),
    ("what is dirty air", "d9"),
    ("how to choose tyre compound", "d8"),
]


def evaluate(k: int = 3) -> dict:
    r = Retriever(DOCS)
    p_at_1 = hits_at_k = 0
    rr_sum = 0.0
    for query, gold in GOLD:
        ranked = [h["doc"]["id"] for h in r.search(query, k=k)]
        if ranked and ranked[0] == gold:
            p_at_1 += 1
        if gold in ranked:
            hits_at_k += 1
            rr_sum += 1.0 / (ranked.index(gold) + 1)
    n = len(GOLD)
    return {"queries": n, "k": k,
            "precision_at_1": round(p_at_1 / n, 3),
            "recall_at_k": round(hits_at_k / n, 3),
            "mrr": round(rr_sum / n, 3)}
