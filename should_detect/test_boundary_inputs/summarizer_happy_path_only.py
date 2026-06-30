# ACE-EXPECT: detect
# CATEGORY: should_detect/test_boundary_inputs
# LANGUAGE: python
# ISSUE: Summarizer test suite covers only one normal article; no empty, whitespace-only, oversized, special-char, or prompt-injection inputs
# EXPECTED-FINDING: The only test feeds a single well-formed paragraph, so empty/huge/adversarial inputs (which crash or get truncated) are never exercised
# EXPECTED-FIX: Parametrize the test with boundary cases — empty string, whitespace-only, very long input exceeding the context window, special characters, and a prompt-injection payload ("ignore previous instructions")
# SEVERITY-HINT: suggestion
"""Unit test for an article summarizer backed by Claude — happy path only."""

import pytest
from anthropic import Anthropic


def summarize(text: str) -> str:
    """Summarize arbitrary user-supplied text — so input size/content is unbounded."""
    client = Anthropic()
    resp = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=200,
        messages=[{"role": "user", "content": f"Summarize:\n{text}"}],
    )
    return resp.content[0].text


# The ONLY test: one normal, well-formed article. No empty input, no oversized input
# beyond the context window, no special characters, no injection payload.
def test_summary_of_normal_article():
    article = (
        "The city council approved a new budget on Tuesday. "
        "Officials said the plan increases funding for public transit."
    )
    summary = summarize(article)
    assert isinstance(summary, str) and summary
