# ACE-EXPECT: detect
# CATEGORY: should_detect/nonstandard_implementation
# LANGUAGE: python
# ISSUE: Structured output is coerced by begging the model to "return only JSON" in the prompt and then hand-parsing with string slicing + json.loads, which breaks on prose, code fences, or trailing text
# EXPECTED-FINDING: JSON output requested via prompt wording and parsed by stripping/locating braces instead of using a schema-enforced structured-output mechanism
# EXPECTED-FIX: enforce structure with tool/function calling or a typed schema (e.g. Anthropic tool input_schema, or instructor/Pydantic) so the model returns validated structured data
# SEVERITY-HINT: warning
"""Extracts contact info by asking for JSON in the prompt and brittle-parsing it."""

import json

from anthropic import Anthropic

client = Anthropic()


def extract_contact(text: str) -> dict:
    prompt = (
        "Extract the contact details. Return ONLY valid JSON with keys "
        '"name", "email", "phone". No explanation, no markdown.\n\n' + text
    )
    resp = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = resp.content[0].text

    # Brittle hand-parsing: try to locate the JSON object in the text.
    start = raw.find("{")
    end = raw.rfind("}")
    snippet = raw[start : end + 1]
    return json.loads(snippet)


if __name__ == "__main__":
    print(extract_contact("Reach Jane Doe at jane@x.com or 555-0100."))
