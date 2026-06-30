# ACE-EXPECT: detect
# CATEGORY: should_detect/structured_output_missing
# LANGUAGE: python
# ISSUE: Model output is parsed as free text via json.loads on raw message content with no schema enforcement
# EXPECTED-FINDING: resp.choices[0].message.content is passed directly to json.loads, relying on the prompt alone to produce valid JSON
# EXPECTED-FIX: Use schema-enforced structured output (OpenAI client.beta.chat.completions.parse with response_format=PydanticModel, or response_format={"type":"json_schema",...}) so the SDK returns a validated object
# SEVERITY-HINT: warning
"""Extract invoice fields from an email body using an LLM and json.loads."""

import json

from openai import OpenAI

client = OpenAI()


def extract_invoice(email_body: str) -> dict:
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Extract the invoice number, vendor, and total. Return JSON.",
            },
            {"role": "user", "content": email_body},
        ],
    )

    # Treats the model's free-text reply as if it were guaranteed valid JSON.
    invoice = json.loads(resp.choices[0].message.content)
    return invoice


if __name__ == "__main__":
    print(extract_invoice("Invoice #A-1029 from Acme Corp, total due $4,200."))
