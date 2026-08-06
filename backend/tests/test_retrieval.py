from app.retrieval import Retriever
from app.corpus import DOCS

def test_retrieves_relevant_doc_top():
    r = Retriever(DOCS)
    assert r.search("what is an undercut", k=3)[0]["doc"]["id"] == "d2"

def test_scores_descending():
    hits = Retriever(DOCS).search("tyre degradation", k=5)
    s = [h["score"] for h in hits]
    assert s == sorted(s, reverse=True)
