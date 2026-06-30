# ACE-EXPECT: detect
# CATEGORY: should_detect/test_deterministic_mocking
# LANGUAGE: python
# ISSUE: Unit test invokes the real OpenAI API instead of mocking it with a fixed response
# EXPECTED-FINDING: Test makes a live network/LLM call making it flaky, slow, costly, and non-deterministic
# EXPECTED-FIX: Patch the client with unittest.mock and return a canned completion object
# SEVERITY-HINT: warning
"""Unit test for a tagline generator that hits the live OpenAI endpoint."""

from openai import OpenAI


def make_tagline(product: str) -> str:
    client = OpenAI()
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=20,
        messages=[{"role": "user", "content": f"Write a short tagline for {product}."}],
    )
    return resp.choices[0].message.content.strip()


def test_make_tagline_returns_text():
    result = make_tagline("a reusable water bottle")
    assert isinstance(result, str)
    assert len(result) > 0
