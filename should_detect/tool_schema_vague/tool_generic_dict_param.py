# ACE-EXPECT: detect
# CATEGORY: should_detect/tool_schema_vague
# LANGUAGE: python
# ISSUE: A tool accepts a free-form object/dict parameter with no defined properties
# EXPECTED-FINDING: The "filters" parameter is typed as an object with no properties (an opaque blob), giving the model no schema for what keys/values are valid
# EXPECTED-FIX: Replace the generic object with an explicit properties schema (named fields, types, enums, constraints, descriptions) so the model produces well-formed arguments
# SEVERITY-HINT: warning
"""Search tool whose 'filters' argument is an untyped open object."""

from openai import OpenAI

client = OpenAI()

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": "Search the product catalog and return matching items.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Free-text search query for product name or keywords.",
                    },
                    # Opaque: model has no idea what keys go here.
                    "filters": {
                        "type": "object",
                        "description": "Optional filters to narrow the search.",
                    },
                },
                "required": ["query"],
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
    print(ask("Find red running shoes under $80 in size 10."))
