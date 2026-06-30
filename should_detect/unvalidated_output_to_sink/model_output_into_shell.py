# ACE-EXPECT: detect
# CATEGORY: should_detect/unvalidated_output_to_sink
# LANGUAGE: python
# ISSUE: LLM output is passed to subprocess with shell=True and executed as a command with no validation or allowlist
# EXPECTED-FINDING: The model's free-text reply is run via subprocess.run(..., shell=True), so whatever string the model produces is executed by the shell unchecked
# EXPECTED-FIX: Constrain the model to choose an action from an allowlist (validated enum), then map it to a fixed argv list run without shell=True; never execute raw model text
# SEVERITY-HINT: critical
"""LLM output executed as a shell command with no validation."""

import subprocess

from openai import OpenAI

client = OpenAI()


def run_devops_task(request: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Output the single shell command that fulfills the request.",
            },
            {"role": "user", "content": request},
        ],
    )
    command = resp.choices[0].message.content

    # Raw model output handed to the shell — no allowlist, no argv splitting.
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout


if __name__ == "__main__":
    print(run_devops_task("show disk usage"))
