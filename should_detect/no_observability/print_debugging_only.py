# ACE-EXPECT: detect
# CATEGORY: should_detect/no_observability
# LANGUAGE: python
# ISSUE: The LLM service relies on bare print() statements for all diagnostics, which cannot be levelled, filtered, structured, or shipped to a log aggregator in production
# EXPECTED-FINDING: bare print() used for diagnostics around LLM calls instead of structured logging
# EXPECTED-FIX: use the logging module (or structlog) with levels and structured key/value fields so logs are filterable and shippable to an aggregator
# SEVERITY-HINT: suggestion
"""Classifies emails and prints debug info instead of logging it."""

from anthropic import Anthropic

client = Anthropic()


def classify(email_body: str) -> str:
    print("DEBUG: starting classification, length=", len(email_body))
    resp = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=20,
        messages=[
            {
                "role": "user",
                "content": f"Classify as spam/ham, one word:\n{email_body}",
            }
        ],
    )
    label = resp.content[0].text.strip()
    print("DEBUG: got label", label)
    if label not in ("spam", "ham"):
        print("WARNING: unexpected label", label)
    return label


if __name__ == "__main__":
    print(classify("You won a prize, click here"))
