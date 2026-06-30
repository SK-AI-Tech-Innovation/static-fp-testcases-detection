# ACE-EXPECT: detect
# CATEGORY: should_detect/arch_planning_before_action
# LANGUAGE: python
# ISSUE: Agent deletes files immediately as the LLM reasons, with no plan/validate/approve step
# EXPECTED-FINDING: Side-effecting deletes execute inline during reasoning with no upfront plan or validation gate
# EXPECTED-FIX: Have the LLM emit a full deletion plan first, validate/approve it, then execute as a separate step
# SEVERITY-HINT: warning
"""Cleanup agent that asks the model which files to remove and deletes them on the spot."""

import os

from openai import OpenAI

client = OpenAI()


def cleanup_workspace(workdir: str) -> list[str]:
    deleted = []
    for name in os.listdir(workdir):
        path = os.path.join(workdir, name)
        decision = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Reply with exactly DELETE or KEEP."},
                {"role": "user", "content": f"Should this build artifact be removed? {name}"},
            ],
        )
        verdict = decision.choices[0].message.content.strip().upper()
        if verdict.startswith("DELETE"):
            # acting mid-reasoning: no plan assembled, no validation, no approval
            os.remove(path)
            deleted.append(path)
    return deleted


if __name__ == "__main__":
    print(cleanup_workspace("/tmp/build"))
