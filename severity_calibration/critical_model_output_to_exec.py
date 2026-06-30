# ACE-EXPECT: detect
# CATEGORY: should_detect/unvalidated_output_to_sink
# LANGUAGE: python
# ISSUE: Model-generated code is passed straight to exec() so the agent can "self-extend" at runtime.
# EXPECTED-FINDING: LLM output flows into exec(), a code-execution sink — arbitrary code execution in-process.
# EXPECTED-FIX: Run generated code only in an isolated sandbox (subprocess in a container, the code-execution server tool, or a restricted interpreter); never exec() in the host process.
# SEVERITY-HINT: critical
"""A 'tool-writing' agent: the model emits a Python function body that exec() installs into the process."""

import os

from anthropic import Anthropic

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def build_and_run_tool(task: str, payload: dict) -> object:
    """Have the model write a transform function, then exec() it and call it on payload."""
    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1024,
        system=(
            "Write a Python function named `transform(data: dict) -> object` that "
            "performs the requested task. Output only the function source, no fences."
        ),
        messages=[{"role": "user", "content": task}],
    )

    source = next(b.text for b in response.content if b.type == "text")

    namespace: dict = {}
    # Model output executed in-process; `transform` is then invoked on real data.
    exec(source, namespace)  # noqa: S102 - planted anti-pattern
    return namespace["transform"](payload)


if __name__ == "__main__":
    print(build_and_run_tool("Sum all integer values in the dict.", {"a": 1, "b": 2, "c": 3}))
