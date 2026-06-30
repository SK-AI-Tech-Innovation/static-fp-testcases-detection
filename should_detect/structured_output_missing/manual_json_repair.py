# ACE-EXPECT: detect
# CATEGORY: should_detect/structured_output_missing
# LANGUAGE: python
# ISSUE: Free-text model output is manually "repaired" (strip code fences, fix quotes) before json.loads
# EXPECTED-FINDING: Ad-hoc cleanup of the model reply (removing ```json fences, swapping quotes) to coax it into parseable JSON, signalling the absence of schema-enforced output
# EXPECTED-FIX: Use schema-enforced structured output (response_format json_schema / parse) so the SDK returns valid JSON and the repair heuristics become unnecessary
# SEVERITY-HINT: warning
"""Strip markdown fences and patch quotes to salvage JSON from an LLM reply."""

import json

from openai import OpenAI

client = OpenAI()


def repair_and_load(raw: str) -> dict:
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[len("json"):]
    cleaned = cleaned.strip().replace("'", '"').rstrip(",")
    return json.loads(cleaned)


def extract_entities(document: str) -> dict:
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Extract people and orgs as JSON."},
            {"role": "user", "content": document},
        ],
    )
    # Whole helper exists only because output shape is not enforced.
    return repair_and_load(resp.choices[0].message.content)


if __name__ == "__main__":
    print(extract_entities("Tim Cook met with the European Commission in Brussels."))
