# ACE-EXPECT: detect
# CATEGORY: should_detect/test_eval_rubric
# LANGUAGE: python
# ISSUE: Evaluation compares free-form LLM output to a single golden string with ==; no rubric or partial credit
# EXPECTED-FINDING: Exact-match against one reference penalizes valid paraphrases and yields a brittle, all-or-nothing score
# EXPECTED-FIX: Use a rubric with semantic similarity or LLM-judge scoring across multiple acceptable references
# SEVERITY-HINT: suggestion
"""Eval for a paraphrase tool comparing output to a single expected string."""

from anthropic import Anthropic

CASES = [
    ("Make this polite: send me the file", "Could you please send me the file?"),
    ("Make this polite: give me a refund", "Could I please request a refund?"),
]


def rewrite(instruction: str) -> str:
    client = Anthropic()
    resp = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=64,
        messages=[{"role": "user", "content": instruction}],
    )
    return resp.content[0].text.strip()


def test_eval_exact_match():
    for instruction, expected in CASES:
        assert rewrite(instruction) == expected
