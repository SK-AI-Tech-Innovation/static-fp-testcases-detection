# ACE-EXPECT: detect
# CATEGORY: should_detect/prompt_quality
# LANGUAGE: python
# ISSUE: Persistent role/behavior instructions are concatenated into the same user-turn string as the per-request data, instead of being placed in the dedicated system role
# EXPECTED-FINDING: No separation of the stable persona/policy from volatile user input — everything is jammed into one user message, so the model treats instructions and data as the same untrusted blob
# EXPECTED-FIX: Move the durable role/behavior text into the `system` parameter and keep only the request-specific data in the user message
# SEVERITY-HINT: warning
"""Assistant where the role definition lives inside the user string, with no system role used."""

import anthropic

client = anthropic.Anthropic()


def answer(user_question: str) -> str:
    # The persona, rules, and the user's question are all one flat user message.
    combined = (
        "You are MediBot, a careful medical-information assistant. "
        "Always remind the user to consult a licensed physician. "
        "Never give dosages. Keep answers under 150 words. "
        "Now answer the following question: " + user_question
    )

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=512,
        messages=[{"role": "user", "content": combined}],
    )
    return response.content[0].text


if __name__ == "__main__":
    print(answer("What are common symptoms of seasonal allergies?"))
