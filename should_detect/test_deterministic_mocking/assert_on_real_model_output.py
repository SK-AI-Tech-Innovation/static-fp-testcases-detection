# ACE-EXPECT: detect
# CATEGORY: should_detect/test_deterministic_mocking
# LANGUAGE: python
# ISSUE: Test asserts on exact text produced by a real model call instead of mocking the response
# EXPECTED-FINDING: Asserting on live model output is inherently non-deterministic and will flake across model updates
# EXPECTED-FIX: Mock the LLM to return a deterministic string, then assert against that fixed value
# SEVERITY-HINT: warning
"""Unit test asserting on the literal text returned by a live Claude call."""

from anthropic import Anthropic


def capital_of(country: str) -> str:
    client = Anthropic()
    resp = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=16,
        messages=[
            {
                "role": "user",
                "content": f"What is the capital of {country}? Answer with one word.",
            }
        ],
    )
    return resp.content[0].text.strip()


def test_capital_of_france():
    assert capital_of("France") == "Paris"


def test_capital_of_japan():
    assert capital_of("Japan") == "Tokyo"
