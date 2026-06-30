# ACE-EXPECT: detect
# CATEGORY: should_detect/prompt_few_shot
# LANGUAGE: python
# ISSUE: An aspect-based sentiment classification prompt has zero few-shot examples for a multi-field structured output
# EXPECTED-FINDING: The task asks for per-aspect sentiment with a fixed label set and JSON shape but gives no example, so aspect granularity and label wording drift
# EXPECTED-FIX: Provide 2-3 labeled examples showing the exact aspects, allowed labels, and JSON structure expected
# SEVERITY-HINT: suggestion
"""Aspect-based sentiment analysis of product reviews via OpenAI."""

from openai import OpenAI

client = OpenAI()

ASPECTS = ["price", "quality", "shipping", "support"]


def analyze_review(review: str) -> str:
    prompt = (
        "Perform aspect-based sentiment analysis on the product review. "
        f"For each of these aspects — {', '.join(ASPECTS)} — assign a sentiment of "
        "positive, negative, neutral, or not_mentioned, and extract the supporting "
        "phrase. Return JSON.\n\n"
        f"Review: {review}"
    )
    # No worked example, so the model improvises the JSON layout and phrasing.
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content
