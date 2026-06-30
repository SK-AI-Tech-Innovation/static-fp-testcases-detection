# ACE-EXPECT: detect
# CATEGORY: should_detect/unvalidated_output_to_sink
# LANGUAGE: python
# ISSUE: Model output is passed as a shell command string to subprocess with shell=True (and os.system).
# EXPECTED-FINDING: LLM-generated text flows into a shell sink (subprocess shell=True / os.system) — command injection / arbitrary command execution.
# EXPECTED-FIX: Do not let the model produce raw shell strings; expose a typed tool whose allowed actions map to argv lists run with shell=False, validated against an allowlist.
# SEVERITY-HINT: critical
"""DevOps assistant that turns a natural-language request into a shell command and runs it."""

import os
import subprocess

from anthropic import Anthropic

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def run_ops_request(request: str) -> str:
    """Ask the model for the shell command that fulfills the request, then execute it in a shell."""
    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=256,
        system=(
            "You are an SRE helper. Reply with ONLY the single shell command "
            "that accomplishes the user's request. No explanation."
        ),
        messages=[{"role": "user", "content": request}],
    )

    command = next(b.text for b in response.content if b.type == "text").strip()

    # The model's text is interpreted by /bin/sh — full command injection surface.
    completed = subprocess.run(  # noqa: S602 - planted anti-pattern
        command, shell=True, capture_output=True, text=True
    )
    os.system(command)  # noqa: S605 - second shell sink, same untrusted input
    return completed.stdout


if __name__ == "__main__":
    print(run_ops_request("show disk usage of the current directory"))
