# ACE-EXPECT: detect
# CATEGORY: should_detect/tool_schema_vague
# LANGUAGE: python
# ISSUE: The tool exposes a single untyped `params` object (additionalProperties open, no field-level properties or descriptions) so the model has no contract to fill it correctly.
# EXPECTED-FINDING: Tool input_schema is a bare generic dict with no described fields; vague schema degrades tool-call accuracy.
# EXPECTED-FIX: Define explicit typed properties with per-field descriptions, mark required fields, and set additionalProperties:false.
# SEVERITY-HINT: warning
"""Customer-records agent whose lookup tool takes an opaque `params` blob."""

import os

from anthropic import Anthropic

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# A single generic object with no described properties — the model is guessing keys.
TOOLS = [
    {
        "name": "lookup_customer",
        "description": "Look up a customer.",
        "input_schema": {
            "type": "object",
            "properties": {
                "params": {"type": "object"},
            },
            "required": ["params"],
        },
    }
]


def run(user_message: str) -> object:
    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1024,
        tools=TOOLS,
        messages=[{"role": "user", "content": user_message}],
    )
    for block in response.content:
        if block.type == "tool_use":
            return block.input  # whatever shape the model invented for `params`
    return next(b.text for b in response.content if b.type == "text")


if __name__ == "__main__":
    print(run("Find the customer with email jane@example.com in the EU region."))
