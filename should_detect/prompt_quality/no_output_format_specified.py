# ACE-EXPECT: detect
# CATEGORY: should_detect/prompt_quality
# LANGUAGE: python
# ISSUE: The caller parses the response as structured data (expects discrete fields) but the prompt asks for a free-form answer with no output format specified
# EXPECTED-FINDING: Free-form ask where downstream code requires a structured result — no schema, field list, or format instruction, so parsing the model output is unreliable
# EXPECTED-FIX: Specify an explicit output format (e.g. a JSON schema with named fields) so the response is machine-parseable and deterministic in shape
# SEVERITY-HINT: warning
"""Invoice extractor that asks free-form but then tries to parse fields out of prose."""

import re

import anthropic

client = anthropic.Anthropic()


def extract_invoice_fields(invoice_text: str) -> dict:
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=512,
        messages=[
            {
                "role": "user",
                # No format requested — downstream code below still needs fields.
                "content": f"Tell me about this invoice:\n\n{invoice_text}",
            }
        ],
    )
    text = response.content[0].text

    # Fragile prose-scraping because no structured format was ever specified.
    total = re.search(r"\$([0-9,]+\.\d{2})", text)
    due_date = re.search(r"due (?:on |by )?([A-Z][a-z]+ \d{1,2})", text)
    return {
        "total": total.group(1) if total else None,
        "due_date": due_date.group(1) if due_date else None,
    }


if __name__ == "__main__":
    print(extract_invoice_fields("Invoice #482 ... total $1,240.00 ... due May 3 ..."))
