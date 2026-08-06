"""Optional LLM narration adapter (responsible-AI, grounded).

Returns a callable llm(prompt)->str using OpenAI or Anthropic if a key is in the
environment, else None (assistant then returns the deterministic grounded answer).
No key, no network needed for the app to work.
"""
from __future__ import annotations
import os


def make_llm():
    if os.environ.get("ANTHROPIC_API_KEY"):
        try:
            import anthropic
            client = anthropic.Anthropic()
            def _llm(prompt: str) -> str:
                m = client.messages.create(model="claude-3-5-sonnet-latest",
                    max_tokens=400, messages=[{"role": "user", "content": prompt}])
                return m.content[0].text
            return _llm
        except Exception:
            return None
    if os.environ.get("OPENAI_API_KEY"):
        try:
            from openai import OpenAI
            client = OpenAI()
            def _llm(prompt: str) -> str:
                r = client.chat.completions.create(model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}])
                return r.choices[0].message.content
            return _llm
        except Exception:
            return None
    return None
