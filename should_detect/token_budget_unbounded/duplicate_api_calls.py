# ACE-EXPECT: detect
# CATEGORY: should_detect/token_budget_unbounded
# LANGUAGE: python
# ISSUE: The model is called twice for the same input to produce two derived outputs
# EXPECTED-FINDING: Two separate identical-prompt-prefix calls are made for one logical request, doubling token cost and latency for data that could come from a single call
# EXPECTED-FIX: Make one call that returns both pieces (structured output), or cache/dedupe the result of the first call and reuse it
# SEVERITY-HINT: warning
"""Produce a summary and a title for an article by calling the model twice on the same text."""

from anthropic import Anthropic

client = Anthropic()


def _ask(prompt: str) -> str:
    response = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def summarize_and_title(article: str) -> dict:
    # Two full round-trips that each re-send the entire article. The summary and the
    # title could be produced from one call (e.g. structured output), so the second
    # call is pure duplicated token spend and latency for the same source text.
    summary = _ask(f"Summarize this article in 3 sentences:\n\n{article}")
    title = _ask(f"Write a title for this article:\n\n{article}")
    return {"summary": summary, "title": title}


if __name__ == "__main__":
    print(summarize_and_title("Long article body about climate policy goes here..."))
