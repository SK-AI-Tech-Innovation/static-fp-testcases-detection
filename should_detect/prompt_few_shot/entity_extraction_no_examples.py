# ACE-EXPECT: detect
# CATEGORY: should_detect/prompt_few_shot
# LANGUAGE: python
# ISSUE: A structured entity-extraction-to-JSON prompt provides zero few-shot examples, leaving the output shape unanchored
# EXPECTED-FINDING: A complex extraction task asks for JSON with specific keys but shows no example, so the model's field names, nesting, and null handling are inconsistent across inputs
# EXPECTED-FIX: Add 2-3 few-shot input/output examples (or a JSON schema / structured-output mode) that pin the exact format
# SEVERITY-HINT: suggestion
"""Extract contact entities from free text into JSON via Anthropic."""

import json

from anthropic import Anthropic

client = Anthropic()


def extract_contacts(text: str) -> dict:
    prompt = (
        "Extract all people mentioned in the text below into JSON. For each person "
        "include their name, role, organization, email, and phone if present. "
        "Return a JSON object with a 'people' array.\n\n"
        f"Text:\n{text}"
    )
    # No examples anchor the schema — keys/nesting/nulls will vary run to run.
    resp = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return json.loads(resp.content[0].text)
