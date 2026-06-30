# ACE-EXPECT: detect
# CATEGORY: should_detect/prompt_context_hierarchy
# LANGUAGE: python
# ISSUE: The system message pastes raw application logs first and states the key safety constraint only at the end
# EXPECTED-FINDING: The binding constraint ("never invent log lines, only reference timestamps present above") sits after a large log dump, where it is most likely to be ignored
# EXPECTED-FIX: Lead the system message with the role and the non-negotiable constraints, then append the logs as clearly delimited reference data
# SEVERITY-HINT: warning
"""Incident-analysis assistant whose system prompt embeds logs then constraints."""

from openai import OpenAI

client = OpenAI()


def analyze_incident(logs: str, user_question: str) -> str:
    system_msg = (
        "You are an SRE assistant. Here are the recent logs:\n\n"
        f"{logs}\n\n"
        # The hard constraint is the last thing in a long system message.
        "IMPORTANT: Only reference timestamps and error codes that literally appear "
        "in the logs above. Never invent log lines. If the logs do not explain the "
        "incident, say so explicitly instead of guessing."
    )
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_question},
        ],
    )
    return resp.choices[0].message.content
