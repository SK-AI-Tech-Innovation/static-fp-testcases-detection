# ACE-EXPECT: detect
# CATEGORY: should_detect/prompt_quality
# LANGUAGE: python
# ISSUE: The instruction is an underspecified "analyze this" with no stated goal, evaluation criteria, audience, or output specification
# EXPECTED-FINDING: Vague task wording ("analyze this data") that gives the model no criteria for what a good answer looks like, leading to unfocused, non-deterministic output
# EXPECTED-FIX: Specify the analysis goal, the criteria/dimensions to evaluate, the target audience, and the expected output shape
# SEVERITY-HINT: warning
"""Data analyzer prompt that just says 'analyze this' with no criteria or output spec."""

import anthropic

client = anthropic.Anthropic()


def analyze(csv_data: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                # No goal, no metrics of interest, no audience, no output format.
                "content": f"Analyze this:\n\n{csv_data}",
            }
        ],
    )
    return response.content[0].text


if __name__ == "__main__":
    print(analyze("date,revenue,churn\n2026-01,1000,0.05\n2026-02,1200,0.04\n"))
