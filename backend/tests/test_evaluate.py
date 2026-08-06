from app.evaluate import evaluate

def test_retrieval_metrics_reasonable():
    m = evaluate()
    assert 0 <= m["precision_at_1"] <= 1
    assert m["recall_at_k"] >= m["precision_at_1"]     # recall@k >= precision@1
    assert m["mrr"] > 0.5                               # retrieval is actually good
