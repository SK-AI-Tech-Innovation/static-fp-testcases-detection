# ACE-EXPECT: detect
# CATEGORY: should_detect/tool_schema_vague
# LANGUAGE: python
# ISSUE: A parameter with a fixed set of valid values is typed as a free string with no enum
# EXPECTED-FINDING: The "priority" and "status" params accept any string instead of constraining to known values, inviting invalid/hallucinated categories
# EXPECTED-FIX: Constrain such fields with an "enum" of the allowed values (and describe each) so the model can only choose valid categories
# SEVERITY-HINT: warning
"""Ticket-creation tool where categorical fields are unconstrained strings."""

from openai import OpenAI

client = OpenAI()

tools = [
    {
        "type": "function",
        "function": {
            "name": "create_ticket",
            "description": "Open a new support ticket in the tracker.",
            "parameters": {
                "type": "object",
                "properties": {
                    "summary": {
                        "type": "string",
                        "description": "Short summary of the issue.",
                    },
                    # Should be an enum: low|medium|high|urgent.
                    "priority": {
                        "type": "string",
                        "description": "Priority of the ticket.",
                    },
                    # Should be an enum: open|in_progress|resolved|closed.
                    "status": {
                        "type": "string",
                        "description": "Initial status of the ticket.",
                    },
                },
                "required": ["summary", "priority"],
            },
        },
    }
]


def ask(question: str):
    return client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": question}],
        tools=tools,
    )


if __name__ == "__main__":
    print(ask("Open a high priority ticket: checkout page returns a 500 error."))
