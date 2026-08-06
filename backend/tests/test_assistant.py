from app import assistant

def test_grounded_answer_has_sources():
    r = assistant.answer("explain the undercut")
    assert r["grounded"] and r["sources"] and assistant.validate(r)

def test_abstains_when_irrelevant():
    r = assistant.answer("what is the capital of France")
    assert r["grounded"] is False and r["sources"] == []

def test_llm_hook_used_when_provided():
    r = assistant.answer("what is an undercut", llm=lambda prompt: "NARRATED")
    assert r["answer"] == "NARRATED" and r["grounded"]
