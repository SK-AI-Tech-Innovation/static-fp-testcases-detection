# ACE-EXPECT: detect
# CATEGORY: should_detect/prompt_few_shot
# LANGUAGE: python
# ISSUE: A tone-rewrite (format-conversion) prompt defines a target style in prose but gives zero before/after examples
# EXPECTED-FINDING: The rewrite task specifies a brand voice with several rules but shows no example pair, so the model's interpretation of "tone" and how much it edits varies widely
# EXPECTED-FIX: Add 2-3 before/after example pairs demonstrating the exact target tone, length change, and what to preserve
# SEVERITY-HINT: suggestion
"""Rewrite customer messages into the company's support voice via OpenAI."""

from openai import OpenAI

client = OpenAI()


def rewrite_to_brand_voice(draft: str) -> str:
    prompt = (
        "Rewrite the support reply below in our brand voice: warm, concise, "
        "professional, no jargon, always open with empathy and close with a clear "
        "next step. Keep all factual details unchanged. Do not add new promises.\n\n"
        f"Draft reply:\n{draft}"
    )
    # No before/after exemplars, so 'brand voice' and edit aggressiveness drift.
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content
