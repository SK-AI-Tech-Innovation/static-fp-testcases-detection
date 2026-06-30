# ACE-EXPECT: detect
# CATEGORY: should_detect/no_retry_fallback
# LANGUAGE: python
# ISSUE: A production-path LLM call has max_retries explicitly disabled and no fallback, so any transient 429/5xx/network error fails the request outright.
# EXPECTED-FINDING: Production LLM call lacks retry/fallback handling; transient API errors propagate as hard failures.
# EXPECTED-FIX: Rely on the SDK's automatic retries (or set max_retries explicitly) and catch RateLimitError/APIStatusError to fall back or surface a graceful error.
# SEVERITY-HINT: warning
"""Synchronous support-ticket summarizer called on every inbound ticket in production."""

import os

from anthropic import Anthropic

# max_retries=0 disables the SDK's built-in backoff entirely.
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"], max_retries=0)


def summarize_ticket(ticket_body: str) -> str:
    """Return a one-paragraph summary used in the agent dashboard for each ticket."""
    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=400,
        system="Summarize the customer's issue in one short paragraph for a support agent.",
        messages=[{"role": "user", "content": ticket_body}],
    )
    # No try/except, no fallback model, no backoff: a single 429 or 529 drops the ticket.
    return next(b.text for b in response.content if b.type == "text")


def handle_inbound(ticket: dict) -> dict:
    ticket["summary"] = summarize_ticket(ticket["body"])
    return ticket


if __name__ == "__main__":
    print(handle_inbound({"id": 1, "body": "Cannot log in after password reset."}))
