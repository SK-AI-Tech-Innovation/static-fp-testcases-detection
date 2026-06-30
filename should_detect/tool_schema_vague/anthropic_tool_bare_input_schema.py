# ACE-EXPECT: detect
# CATEGORY: should_detect/tool_schema_vague
# LANGUAGE: python
# ISSUE: Anthropic tool defined with a bare input_schema lacking descriptions and constraints
# EXPECTED-FINDING: The Claude tool's input_schema has properties with no descriptions, no enum/constraints, and no "required", so the model lacks guidance on valid arguments
# EXPECTED-FIX: Enrich input_schema with per-property descriptions, enums/constraints where applicable, and a required list (Anthropic recommends detailed tool/parameter descriptions for reliable tool use)
# SEVERITY-HINT: warning
"""Anthropic tool with a minimal, description-free input_schema."""

import anthropic

client = anthropic.Anthropic()

tools = [
    {
        "name": "book_flight",
        "description": "Book a flight.",
        "input_schema": {
            "type": "object",
            "properties": {
                "origin": {"type": "string"},
                "destination": {"type": "string"},
                "date": {"type": "string"},
                "cabin": {"type": "string"},
            },
            # No descriptions, no date format, no cabin enum, no required list.
        },
    }
]


def ask(question: str):
    return client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        tools=tools,
        messages=[{"role": "user", "content": question}],
    )


if __name__ == "__main__":
    print(ask("Book me a flight from SFO to JFK next Tuesday in economy."))
