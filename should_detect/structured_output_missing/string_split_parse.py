# ACE-EXPECT: detect
# CATEGORY: should_detect/structured_output_missing
# LANGUAGE: python
# ISSUE: Model output is parsed by splitting strings on a delimiter instead of using a schema
# EXPECTED-FINDING: The reply is prompted to be pipe-delimited and parsed with str.split("|"), with no structured-output enforcement
# EXPECTED-FIX: Use schema-enforced structured output (response_format json_schema / Pydantic) so fields are returned as a validated object rather than positional split() tokens
# SEVERITY-HINT: warning
"""Parse a delimited LLM response for a contact record with str.split."""

from openai import OpenAI

client = OpenAI()


def parse_contact(raw_text: str) -> dict:
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Extract the contact as 'name|email|company', one line, no extra words.",
            },
            {"role": "user", "content": raw_text},
        ],
    )

    line = resp.choices[0].message.content.strip()

    # Positional parsing breaks the moment the model adds spacing, labels, or a stray pipe.
    name, email, company = line.split("|")
    return {"name": name, "email": email, "company": company}


if __name__ == "__main__":
    print(parse_contact("Reach out to Dana Lee at dana@globex.io, she works at Globex."))
