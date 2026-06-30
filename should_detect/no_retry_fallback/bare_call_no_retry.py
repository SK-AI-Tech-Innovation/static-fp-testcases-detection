# ACE-EXPECT: detect
# CATEGORY: should_detect/no_retry_fallback
# LANGUAGE: python
# ISSUE: Single LLM API call with no error handling, retries, or fallback of any kind
# EXPECTED-FINDING: Network/transient errors from the LLM call propagate uncaught and crash the request
# EXPECTED-FIX: Wrap the call with bounded retries and exponential backoff (e.g. tenacity @retry or the SDK's max_retries), and handle transient failures
# SEVERITY-HINT: warning
"""Summarize a support ticket by calling the chat model exactly once with no resilience."""

from anthropic import Anthropic

client = Anthropic()


def summarize_ticket(ticket_text: str) -> str:
    # A single, naked API call: if the network blips or the service returns a
    # transient 5xx / overloaded error, the whole function raises and the caller dies.
    response = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=256,
        messages=[
            {"role": "user", "content": f"Summarize this ticket in one sentence:\n\n{ticket_text}"}
        ],
    )
    return response.content[0].text


if __name__ == "__main__":
    print(summarize_ticket("My invoice shows the wrong amount and support never replied."))
