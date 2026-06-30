# ACE-EXPECT: detect
# CATEGORY: should_detect/test_eval_rubric
# LANGUAGE: python
# ISSUE: Evaluation just prints model outputs for a human to eyeball; no scoring rubric or pass predicate
# EXPECTED-FINDING: Manual visual inspection is unrepeatable and provides no measurable quality signal
# EXPECTED-FIX: Replace printing with scored metrics (e.g., LLM-judge rubric) and an automated pass/fail threshold
# SEVERITY-HINT: suggestion
"""Eval script for a code-explainer that prints outputs for manual inspection."""

from openai import OpenAI

SNIPPETS = [
    "def add(a, b):\n    return a + b",
    "for i in range(10):\n    print(i * i)",
    "x = [n for n in nums if n % 2 == 0]",
]


def explain(code: str) -> str:
    client = OpenAI()
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": f"Explain this code:\n{code}"}],
    )
    return resp.choices[0].message.content


def run_eval() -> None:
    for snippet in SNIPPETS:
        print("=== INPUT ===")
        print(snippet)
        print("=== EXPLANATION ===")
        print(explain(snippet))
        print()


if __name__ == "__main__":
    run_eval()
