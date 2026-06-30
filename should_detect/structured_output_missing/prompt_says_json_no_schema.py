# ACE-EXPECT: detect
# CATEGORY: should_detect/structured_output_missing
# LANGUAGE: python
# ISSUE: The prompt asks for JSON in natural language but no structured-output / schema mechanism is used
# EXPECTED-FINDING: Reliance on a "respond only in JSON" instruction with response_format defaulting to free text and no json_schema, so valid JSON is not guaranteed
# EXPECTED-FIX: Enforce the shape with response_format={"type":"json_schema","json_schema":{...}} (or beta.parse with a Pydantic text_format), instead of trusting the prompt
# SEVERITY-HINT: warning
"""Ask the model for JSON via the prompt only, then json.loads the reply."""

import json

from openai import OpenAI

client = OpenAI()


def summarize_ticket(ticket: str) -> dict:
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a support triage bot. Respond ONLY with a JSON object that has "
                    "the keys priority, category, and summary. Do not include any other text."
                ),
            },
            {"role": "user", "content": ticket},
        ],
    )

    # The only thing standing between this and a crash is the prompt wording.
    return json.loads(resp.choices[0].message.content)


if __name__ == "__main__":
    print(summarize_ticket("The export button has been spinning forever since the update."))
