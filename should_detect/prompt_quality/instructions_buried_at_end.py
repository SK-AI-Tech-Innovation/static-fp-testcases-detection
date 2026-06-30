# ACE-EXPECT: detect
# CATEGORY: should_detect/prompt_quality
# LANGUAGE: python
# ISSUE: The actual task instruction is placed AFTER a very large data blob, so it is easy for the model to lose track of (and for long inputs, attention to a trailing instruction degrades)
# EXPECTED-FINDING: Key instruction positioned at the very end of the prompt, downstream of a large pasted data payload, instead of up front before the data
# EXPECTED-FIX: Put the instruction first (state the task and output format before the data), and clearly fence the data block so the instruction is not buried
# SEVERITY-HINT: warning
"""Classifier that dumps a huge transcript first and only states the task on the last line."""

import anthropic

client = anthropic.Anthropic()


def classify_ticket(transcript: str) -> str:
    # The model reads thousands of tokens of data before ever learning what to do with it.
    prompt = (
        transcript  # large support-call transcript pasted directly, often 5-10k tokens
        + "\n\n"
        + "Given everything above, classify the customer's sentiment as "
        "POSITIVE, NEGATIVE, or NEUTRAL and respond with only that one word."
    )

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=16,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text.strip()


if __name__ == "__main__":
    huge_transcript = "Agent: Hello...\nCustomer: ...\n" * 500
    print(classify_ticket(huge_transcript))
