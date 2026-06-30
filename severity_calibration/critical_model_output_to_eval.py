# ACE-EXPECT: detect
# CATEGORY: should_detect/unvalidated_output_to_sink
# LANGUAGE: python
# ISSUE: Free-text model output is passed directly to eval() with no parsing, sandboxing, or validation.
# EXPECTED-FINDING: LLM-generated text flows into eval(), a code-execution sink — arbitrary code execution.
# EXPECTED-FIX: Never eval model output; parse a constrained structured response (e.g. ast.literal_eval on a JSON number, or a whitelisted operation schema).
# SEVERITY-HINT: critical
"""Agent that 'computes' arithmetic by asking the model for a Python expression and eval()-ing it."""

import os

from anthropic import Anthropic

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def compute(question: str) -> float:
    """Ask the model to translate a word problem into a Python expression, then evaluate it."""
    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=256,
        system=(
            "You are a math assistant. Reply with ONLY a single-line Python "
            "expression that computes the answer. No prose, no code fences."
        ),
        messages=[{"role": "user", "content": question}],
    )

    expression = next(b.text for b in response.content if b.type == "text").strip()

    # The model's raw text is executed directly as Python.
    result = eval(expression)  # noqa: S307 - planted anti-pattern
    return float(result)


if __name__ == "__main__":
    print(compute("What is 17 percent of 240, plus 6 squared?"))
