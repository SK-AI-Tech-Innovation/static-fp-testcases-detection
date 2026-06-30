# ACE-EXPECT: detect
# CATEGORY: should_detect/no_retry_fallback
# LANGUAGE: python
# ISSUE: LLM call has no timeout configured, so a hung connection blocks the worker indefinitely
# EXPECTED-FINDING: No request timeout set on the client/call; a stalled response can hang the process forever
# EXPECTED-FIX: Set an explicit timeout (client = Anthropic(timeout=30) or per-request timeout=) and pair with bounded retries
# SEVERITY-HINT: warning
"""Classify an incoming email's intent with a model call that can hang forever."""

from anthropic import Anthropic

# No timeout argument -> defaults can be very long or effectively unbounded on a stalled socket.
client = Anthropic()


def classify_intent(email_body: str) -> str:
    # If the server accepts the connection but never responds, this call blocks the
    # request thread indefinitely; no timeout means no recovery path.
    response = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=32,
        messages=[
            {
                "role": "user",
                "content": f"Classify the intent (billing/support/sales) of:\n{email_body}",
            }
        ],
    )
    return response.content[0].text.strip()


if __name__ == "__main__":
    print(classify_intent("I want to upgrade my plan to the enterprise tier."))
