# ACE-EXPECT: detect
# CATEGORY: should_detect/unvalidated_output_to_sink
# LANGUAGE: python
# ISSUE: A filesystem path produced by the LLM is opened/read directly with no validation or confinement to an allowed directory
# EXPECTED-FINDING: The model's free-text reply is used as a path passed straight to open(), so the model can name any path (traversal, absolute, outside the data dir) and it is read unchecked
# EXPECTED-FIX: Validate the model output against an allowlist or resolve-and-confine it to a base directory (os.path.realpath under a known root, reject traversal) before opening
# SEVERITY-HINT: critical
"""Opening a file at a path taken directly from LLM output."""

from openai import OpenAI

client = OpenAI()


def load_referenced_doc(user_request: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Return the file path of the document the user is asking about.",
            },
            {"role": "user", "content": user_request},
        ],
    )
    path = resp.choices[0].message.content.strip()

    # Model-chosen path opened with no validation or base-directory confinement.
    with open(path) as fh:
        return fh.read()


if __name__ == "__main__":
    print(load_referenced_doc("show me the onboarding guide"))
