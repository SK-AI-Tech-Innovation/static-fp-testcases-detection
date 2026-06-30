# ACE-EXPECT: detect
# CATEGORY: should_detect/structured_output_missing
# LANGUAGE: python
# ISSUE: Model text output is turned into a Python object with ast.literal_eval instead of a validated schema
# EXPECTED-FINDING: ast.literal_eval is run on resp.choices[0].message.content to materialize a dict/list from free-text model output, with no schema or validation
# EXPECTED-FIX: Use schema-enforced structured output (response_format json_schema / Pydantic parse) plus validation, rather than eval-style parsing of model text
# SEVERITY-HINT: warning
"""Use ast.literal_eval to turn an LLM's text into a Python list of tags."""

import ast

from openai import OpenAI

client = OpenAI()


def suggest_tags(article: str) -> list:
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Return a Python list literal of 3-5 topic tags, e.g. ['ai', 'health'].",
            },
            {"role": "user", "content": article},
        ],
    )

    text = resp.choices[0].message.content.strip()

    # literal_eval on model output: shape and types are entirely unguaranteed.
    tags = ast.literal_eval(text)
    return tags


if __name__ == "__main__":
    print(suggest_tags("A new study links gut bacteria to improved sleep quality."))
