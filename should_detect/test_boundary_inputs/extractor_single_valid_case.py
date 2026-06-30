# ACE-EXPECT: detect
# CATEGORY: should_detect/test_boundary_inputs
# LANGUAGE: python
# ISSUE: Field-extractor test has a single well-formed input; missing empty/malformed/oversized/special-char cases
# EXPECTED-FINDING: Only one valid extraction case is asserted, so failure modes on bad input go untested
# EXPECTED-FIX: Add cases for missing fields, garbled text, huge documents, and unicode/control characters
# SEVERITY-HINT: suggestion
"""Tests for an invoice field extractor using the OpenAI structured output API."""

import json

import pytest
from openai import OpenAI


def extract_invoice(doc: str) -> dict:
    client = OpenAI()
    resp = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "Extract invoice_number and total as JSON."},
            {"role": "user", "content": doc},
        ],
    )
    return json.loads(resp.choices[0].message.content)


@pytest.fixture
def extracted():
    document = "Invoice #INV-2024-0091\nTotal Due: $1,250.00\nDate: 2024-03-11"
    return extract_invoice(document)


def test_invoice_number_extracted(extracted):
    assert extracted["invoice_number"] == "INV-2024-0091"


def test_total_extracted(extracted):
    assert "1,250" in str(extracted["total"]) or "1250" in str(extracted["total"])
