# ACE-EXPECT: detect
# CATEGORY: should_detect/test_eval_rubric
# LANGUAGE: python
# ISSUE: Evaluation checks only that the output parses as JSON; no rubric on field correctness or completeness
# EXPECTED-FINDING: Valid JSON syntax says nothing about whether the extracted values are accurate or complete
# EXPECTED-FIX: Score parsed fields against gold values with explicit accuracy/completeness metrics and a threshold
# SEVERITY-HINT: suggestion
"""Eval for a resume parser that only verifies the response is parseable JSON."""

import json

from openai import OpenAI

RESUMES = [
    "Jane Doe — Senior Engineer at Acme (2019-2024). Skills: Python, Go.",
    "John Smith. Data Scientist, BetaCorp. MSc Statistics. Email: js@beta.io",
]


def parse_resume(text: str) -> str:
    client = OpenAI()
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "Extract name, role, skills as JSON."},
            {"role": "user", "content": text},
        ],
    )
    return resp.choices[0].message.content


def test_eval_outputs_are_json():
    for resume in RESUMES:
        raw = parse_resume(resume)
        parsed = json.loads(raw)
        assert isinstance(parsed, dict)
