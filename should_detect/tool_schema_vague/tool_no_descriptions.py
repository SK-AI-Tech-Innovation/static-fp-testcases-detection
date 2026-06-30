# ACE-EXPECT: detect
# CATEGORY: should_detect/tool_schema_vague
# LANGUAGE: python
# ISSUE: Tool/function schema has no description for the function or its parameters
# EXPECTED-FINDING: The OpenAI function tool defines name and parameters but provides no "description" for the tool or its properties, so the model has no guidance on when/how to call it
# EXPECTED-FIX: Add a clear tool-level description and per-property descriptions (what each field means, units, format) so the model can call the tool correctly
# SEVERITY-HINT: warning
"""Define a weather tool with zero descriptions on the function or its params."""

from openai import OpenAI

client = OpenAI()

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"},
                    "unit": {"type": "string"},
                },
                "required": ["location"],
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
    print(ask("What's the weather in Seoul right now?"))
