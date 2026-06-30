# ACE-EXPECT: detect
# CATEGORY: should_detect/token_budget_unbounded
# LANGUAGE: python
# ISSUE: Generation call sets no output cap, allowing unboundedly long (and expensive) completions
# EXPECTED-FINDING: No max output-token limit is set, so the model can emit a very long response, inflating cost and latency unpredictably
# EXPECTED-FIX: Set an explicit output cap sized to the task (max_tokens for Anthropic / max_output_tokens for others) to bound cost and latency
# SEVERITY-HINT: suggestion
"""Generate a short tagline but place no cap on the output length."""

from openai import OpenAI

client = OpenAI()


def make_tagline(brand: str) -> str:
    # The task only needs a one-line tagline, but no max output-token limit is set.
    # The model is free to ramble for hundreds of tokens, making cost and latency
    # unpredictable for what should be a tiny, bounded response.
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Write a catchy one-line tagline for {brand}."}],
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    print(make_tagline("AeroBottle"))
