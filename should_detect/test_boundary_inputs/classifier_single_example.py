# ACE-EXPECT: detect
# CATEGORY: should_detect/test_boundary_inputs
# LANGUAGE: python
# ISSUE: Sentiment classifier test asserts on one positive example only; no neutral/empty/long/adversarial inputs
# EXPECTED-FINDING: A single example cannot reveal misclassification on boundary or hostile inputs
# EXPECTED-FIX: Parametrize with empty text, neutral text, emoji-only, and injection ("ignore previous") inputs
# SEVERITY-HINT: suggestion
"""Tests for a sentiment classifier built on Claude."""

import pytest
from anthropic import Anthropic


def classify_sentiment(text: str) -> str:
    client = Anthropic()
    resp = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=8,
        messages=[
            {
                "role": "user",
                "content": f"Reply with exactly one word, positive or negative:\n{text}",
            }
        ],
    )
    return resp.content[0].text.strip().lower()


def test_positive_review_is_positive():
    label = classify_sentiment("I absolutely loved this product, it works great!")
    assert label == "positive"
