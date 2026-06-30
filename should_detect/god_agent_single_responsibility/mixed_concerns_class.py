# ACE-EXPECT: detect
# CATEGORY: should_detect/god_agent_single_responsibility
# LANGUAGE: python
# ISSUE: One class owns HTTP fetching, DB persistence, LLM calls, prompt templating, caching, and email delivery — a god class with many unrelated responsibilities
# EXPECTED-FINDING: SupportAgent bundles transport, persistence, prompt construction, model invocation, caching, and notification, so it cannot be tested or reused per concern and changes ripple across unrelated features
# EXPECTED-FIX: Split responsibilities into collaborators (HttpClient, TicketRepository, PromptBuilder, LlmClient, Cache, Notifier) injected into a thin coordinator following single-responsibility
# SEVERITY-HINT: warning
"""A god class mixing fetching, persistence, LLM, caching, and notification concerns."""

import sqlite3

import requests
from openai import OpenAI


class SupportAgent:
    def __init__(self) -> None:
        self.client = OpenAI()
        self.db = sqlite3.connect("tickets.db")
        self.cache: dict[str, str] = {}

    def fetch_ticket(self, ticket_id: str) -> dict:
        return requests.get(f"https://api.example.com/tickets/{ticket_id}").json()

    def save_reply(self, ticket_id: str, reply: str) -> None:
        self.db.execute(
            "INSERT INTO replies (id, body) VALUES (?, ?)", (ticket_id, reply)
        )
        self.db.commit()

    def build_prompt(self, ticket: dict) -> str:
        return f"Customer says: {ticket['body']}\nWrite a helpful reply."

    def call_model(self, prompt: str) -> str:
        if prompt in self.cache:
            return self.cache[prompt]
        resp = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
        )
        out = resp.choices[0].message.content
        self.cache[prompt] = out
        return out

    def send_email(self, ticket: dict, reply: str) -> None:
        requests.post(
            "https://api.example.com/email",
            json={"to": ticket["email"], "body": reply},
        )

    def handle(self, ticket_id: str) -> None:
        ticket = self.fetch_ticket(ticket_id)
        prompt = self.build_prompt(ticket)
        reply = self.call_model(prompt)
        self.save_reply(ticket_id, reply)
        self.send_email(ticket, reply)


if __name__ == "__main__":
    SupportAgent().handle("T-1001")
