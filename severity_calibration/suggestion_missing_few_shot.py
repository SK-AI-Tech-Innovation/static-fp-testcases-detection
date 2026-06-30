# ACE-EXPECT: detect
# CATEGORY: should_detect/prompt_few_shot
# LANGUAGE: python
# ISSUE: A complex, format-sensitive extraction prompt gives only an abstract instruction with zero few-shot examples to anchor the output shape — a quality nicety, not a correctness or security risk.
# EXPECTED-FINDING: Complex extraction prompt has no few-shot examples; output format/edge-case handling is under-specified.
# EXPECTED-FIX: Add 2-3 input/output exemplars (as alternating user/assistant turns or in the prompt) covering the tricky cases.
# SEVERITY-HINT: suggestion
"""Extract structured clinical-trial criteria from prose with an instruction-only prompt."""

import os

from anthropic import Anthropic

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# A genuinely hard extraction task, but the model is given no exemplars to learn the
# expected shape, units, or how to handle compound/negated criteria.
SYSTEM = (
    "Extract eligibility criteria from the trial description. For each criterion, "
    "output its type (inclusion or exclusion), the measured variable, the comparator, "
    "the threshold value, and the unit. Combine compound criteria correctly and "
    "preserve negations. Output one criterion per line."
)


def extract_criteria(description: str) -> str:
    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1024,
        system=SYSTEM,
        messages=[{"role": "user", "content": description}],
    )
    return next(b.text for b in response.content if b.type == "text")


if __name__ == "__main__":
    print(
        extract_criteria(
            "Adults aged 18-65 with HbA1c above 7.0% are eligible, "
            "but patients with eGFR below 30 mL/min are excluded."
        )
    )
