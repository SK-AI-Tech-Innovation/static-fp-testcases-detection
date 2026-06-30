# ACE-EXPECT: detect
# CATEGORY: should_detect/tool_schema_vague
# LANGUAGE: python
# ISSUE: Tool schema marks no parameters as required even though the function cannot work without them
# EXPECTED-FINDING: The schema omits the "required" array, so essential params (to, amount) are treated as optional and the model may emit a call missing them
# EXPECTED-FIX: Declare the mandatory parameters in a "required" list (and add per-field constraints) so the model must supply them
# SEVERITY-HINT: warning
"""Money-transfer tool that declares no required parameters."""

from openai import OpenAI

client = OpenAI()

tools = [
    {
        "type": "function",
        "function": {
            "name": "transfer_funds",
            "description": "Transfer money from the user's account to a recipient.",
            "parameters": {
                "type": "object",
                "properties": {
                    "to_account": {
                        "type": "string",
                        "description": "Destination account number.",
                    },
                    "amount": {
                        "type": "number",
                        "description": "Amount to transfer in USD.",
                    },
                    "memo": {
                        "type": "string",
                        "description": "Optional note shown on the statement.",
                    },
                },
                # No "required": both to_account and amount are essential but optional here.
            },
        },
    }
]


def ask(question: str):
    return client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": question}],
        tools=tools,
    )


if __name__ == "__main__":
    print(ask("Send $250 to account 4471902."))
