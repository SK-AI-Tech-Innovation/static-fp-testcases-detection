# ACE-EXPECT: detect
# CATEGORY: should_detect/prompt_quality
# LANGUAGE: python
# ISSUE: User-supplied text is concatenated directly into the instruction line with no delimiter or fence, so the boundary between the instruction and the data is ambiguous to the model
# EXPECTED-FINDING: Raw user input interpolated inline with the instruction and no separator/fence, making it unclear where the directive ends and the data begins (clarity problem, not framed as security)
# EXPECTED-FIX: Place the user content in a clearly fenced/delimited block (e.g. triple backticks or an XML-style <user_input> tag) and reference it by name in the instruction
# SEVERITY-HINT: warning
"""Translator that splices unfenced user text straight into the instruction sentence."""

import anthropic

client = anthropic.Anthropic()


def translate_to_french(user_text: str) -> str:
    # No delimiter: instruction and data run together as one ambiguous sentence.
    prompt = "Translate the following sentence into French: " + user_text

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


if __name__ == "__main__":
    print(translate_to_french("The meeting is scheduled for tomorrow at noon."))
