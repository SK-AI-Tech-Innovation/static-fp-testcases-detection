# ACE-EXPECT: detect
# CATEGORY: should_detect/token_budget_unbounded
# LANGUAGE: python
# ISSUE: Conversation history grows without bound; every turn resends the full transcript
# EXPECTED-FINDING: messages list is appended to forever and never trimmed/summarized, so token usage (and cost/latency) grows linearly with turns until the context window is exceeded
# EXPECTED-FIX: Cap history (sliding window of last N turns), summarize older turns, or trim by token budget before each call
# SEVERITY-HINT: warning
"""A chatbot that keeps appending to the message list and never trims it."""

from anthropic import Anthropic

client = Anthropic()


class ChatSession:
    def __init__(self) -> None:
        self.messages: list[dict] = []

    def send(self, user_text: str) -> str:
        self.messages.append({"role": "user", "content": user_text})
        # Every call resends the ENTIRE accumulated history. After many turns this
        # blows the token budget: cost and latency climb with each message and the
        # request eventually exceeds the model's context window.
        response = client.messages.create(
            model="claude-opus-4-20250514",
            max_tokens=512,
            messages=self.messages,
        )
        reply = response.content[0].text
        self.messages.append({"role": "assistant", "content": reply})
        return reply


if __name__ == "__main__":
    session = ChatSession()
    for i in range(1000):
        session.send(f"Tell me fact number {i}.")
