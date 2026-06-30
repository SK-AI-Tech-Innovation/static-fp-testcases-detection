# ACE-EXPECT: detect
# CATEGORY: should_detect/structured_output_missing
# LANGUAGE: python
# ISSUE: json.loads() is called directly on free-text model output with no schema enforcement, no parse-failure handling, and downstream code assumes specific keys.
# EXPECTED-FINDING: Structured data is extracted by json.loads() on unconstrained text — reliability-critical: any format drift (prose, code fences, missing keys) raises and breaks the pipeline.
# EXPECTED-FIX: Use the structured-output API (output_config.format / messages.parse with a schema), or validate against a Pydantic model with explicit parse-error handling.
# SEVERITY-HINT: critical
"""Extract structured invoice fields from text by json.loads-ing the model's reply."""

import json
import os

from anthropic import Anthropic

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def extract_invoice(document_text: str) -> dict:
    """Pull vendor, total, and due_date out of an invoice as a dict."""
    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=512,
        system="Extract the invoice fields and return them as JSON: vendor, total, due_date.",
        messages=[{"role": "user", "content": document_text}],
    )

    raw = next(b.text for b in response.content if b.type == "text")

    # No schema, no try/except: a code fence, a leading sentence, or a renamed
    # key silently breaks parsing or KeyErrors downstream.
    data = json.loads(raw)
    return {
        "vendor": data["vendor"],
        "total": float(data["total"]),
        "due_date": data["due_date"],
    }


if __name__ == "__main__":
    print(extract_invoice("ACME Corp invoice, total $4,200.00, due 2026-07-15"))
