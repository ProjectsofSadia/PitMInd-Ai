"""PitMind retrieval — TF-IDF vector index + cosine similarity (real retrieval).

This is the R in RAG: embed the corpus, retrieve the top-k most relevant
documents for a query. FAISS is a drop-in for scale; cosine over TF-IDF is
exact and dependency-light for this corpus size.
"""
from __future__ import annotations
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Retriever:
    def __init__(self, docs):
        self.docs = docs
        self.vec = TfidfVectorizer(stop_words="english")
        self.matrix = self.vec.fit_transform([d["title"] + ". " + d["text"] for d in docs])

    def search(self, query: str, k: int = 3):
        q = self.vec.transform([query])
        sims = cosine_similarity(q, self.matrix)[0]
        ranked = sorted(range(len(self.docs)), key=lambda i: -sims[i])[:k]
        return [{"doc": self.docs[i], "score": round(float(sims[i]), 3)} for i in ranked]
