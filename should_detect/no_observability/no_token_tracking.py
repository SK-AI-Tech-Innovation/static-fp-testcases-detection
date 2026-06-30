# ACE-EXPECT: detect
# CATEGORY: should_detect/no_observability
# LANGUAGE: python
# ISSUE: LLM calls are made in a loop but the usage data returned by the API is never read, so token consumption is completely invisible
# EXPECTED-FINDING: response.usage (input/output token counts) is ignored on every call; there is no accumulation or reporting of token usage
# EXPECTED-FIX: read response.usage.input_tokens / output_tokens after each call and aggregate them (or emit them to a metrics/logging sink) so token consumption is tracked
# SEVERITY-HINT: warning
"""Batch-summarizes support tickets but never inspects token usage."""

from anthropic import Anthropic

client = Anthropic()


def summarize_tickets(tickets: list[str]) -> list[str]:
    summaries = []
    for ticket in tickets:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=300,
            messages=[
                {
                    "role": "user",
                    "content": f"Summarize this support ticket in one sentence:\n\n{ticket}",
                }
            ],
        )
        # We only ever look at the text. response.usage is right there and discarded.
        summaries.append(response.content[0].text)
    return summaries


if __name__ == "__main__":
    open_tickets = ["My login fails", "Refund not received", "App crashes on startup"]
    for s in summarize_tickets(open_tickets):
        print(s)
