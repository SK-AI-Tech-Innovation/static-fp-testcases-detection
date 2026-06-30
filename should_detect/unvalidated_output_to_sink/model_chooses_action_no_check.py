# ACE-EXPECT: detect
# CATEGORY: should_detect/unvalidated_output_to_sink
# LANGUAGE: python
# ISSUE: An action dispatcher uses getattr on a raw model-chosen string to select and invoke a method, with no allowlist of permitted actions
# EXPECTED-FINDING: The model's free-text action name is fed to getattr(handler, action) and called directly, so any attribute the model names is invoked with no allowlist or membership check
# EXPECTED-FIX: Validate the model's action against an explicit allowlist (set/enum of permitted actions) and dispatch via a fixed mapping; reject or default on unknown values rather than reflecting on raw text
# SEVERITY-HINT: critical
"""Dispatch on a raw model-chosen action string via getattr, with no allowlist."""

from openai import OpenAI

client = OpenAI()


class AccountHandler:
    def view_balance(self) -> str:
        return "balance: $100"

    def freeze_account(self) -> str:
        return "account frozen"

    def close_account(self) -> str:
        return "account closed"


def route(user_request: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Reply with the method name to call."},
            {"role": "user", "content": user_request},
        ],
    )
    action = resp.choices[0].message.content.strip()

    handler = AccountHandler()
    # Whatever string the model returns is reflected into a method call — no allowlist.
    method = getattr(handler, action)
    return method()


if __name__ == "__main__":
    print(route("I want to see my balance"))
