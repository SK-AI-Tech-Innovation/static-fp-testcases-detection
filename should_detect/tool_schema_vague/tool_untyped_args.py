# ACE-EXPECT: detect
# CATEGORY: should_detect/tool_schema_vague
# LANGUAGE: python
# ISSUE: Tool parameters are declared without JSON Schema types
# EXPECTED-FINDING: Properties in the parameters schema have no "type" (and no description/constraints), leaving argument formats unspecified for the model
# EXPECTED-FIX: Give every parameter an explicit type plus description and constraints (e.g. integer with minimum, string with format) so arguments are well-defined
# SEVERITY-HINT: warning
"""Calendar tool whose parameters declare no types at all."""

from openai import OpenAI

client = OpenAI()

tools = [
    {
        "type": "function",
        "function": {
            "name": "create_event",
            "description": "Create a calendar event for the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    # No "type" on any of these -> model can't tell string from number/bool.
                    "title": {},
                    "start_time": {},
                    "duration_minutes": {},
                    "all_day": {},
                },
                "required": ["title", "start_time"],
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
    print(ask("Schedule a 30 minute sync tomorrow at 2pm called Roadmap review."))
