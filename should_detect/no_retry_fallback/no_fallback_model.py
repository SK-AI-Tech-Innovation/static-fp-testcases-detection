# ACE-EXPECT: detect
# CATEGORY: should_detect/no_retry_fallback
# LANGUAGE: python
# ISSUE: A single primary model is a hard dependency with no fallback when it is unavailable/overloaded
# EXPECTED-FINDING: When the primary model errors or is overloaded, the feature has no degraded path and fails outright
# EXPECTED-FIX: Add a fallback model/provider (e.g. LangChain with_fallbacks, or try primary then a secondary model) so the feature degrades gracefully
# SEVERITY-HINT: warning
"""Generate a product description using only one model, with no fallback if it is down."""

from anthropic import Anthropic, APIStatusError

client = Anthropic()

PRIMARY_MODEL = "claude-opus-4-20250514"


def generate_description(product_name: str, features: list[str]) -> str:
    prompt = f"Write a marketing description for {product_name}. Features: {', '.join(features)}."
    try:
        response = client.messages.create(
            model=PRIMARY_MODEL,
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text
    except APIStatusError:
        # The "handling" just re-raises: if the primary model is overloaded there is
        # no secondary model to fall back to, so the whole feature is unavailable.
        raise


if __name__ == "__main__":
    print(generate_description("AeroBottle", ["insulated", "leak-proof", "1L"]))
