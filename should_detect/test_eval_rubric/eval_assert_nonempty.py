# ACE-EXPECT: detect
# CATEGORY: should_detect/test_eval_rubric
# LANGUAGE: python
# ISSUE: Evaluation only asserts the output is non-empty; no rubric, metrics, or quality scoring
# EXPECTED-FINDING: A len>0 check tells nothing about factual accuracy, completeness, or relevance of the answer
# EXPECTED-FIX: Define a rubric (accuracy/completeness/format) and score each output against explicit criteria
# SEVERITY-HINT: suggestion
"""Evaluation harness for a QA assistant that merely checks the answer is non-empty."""

from anthropic import Anthropic

QUESTIONS = [
    "What year did the Apollo 11 mission land on the moon?",
    "Who wrote the novel 'Pride and Prejudice'?",
    "What is the chemical symbol for gold?",
]


def answer(question: str) -> str:
    client = Anthropic()
    resp = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=64,
        messages=[{"role": "user", "content": question}],
    )
    return resp.content[0].text.strip()


def test_eval_answers_present():
    for q in QUESTIONS:
        out = answer(q)
        assert len(out) > 0
