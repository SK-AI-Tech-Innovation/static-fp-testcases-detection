# ACE-EXPECT: detect
# CATEGORY: should_detect/no_observability
# LANGUAGE: python
# ISSUE: A multi-step agent (plan -> tool call -> synthesize) runs several LLM calls with no spans/traces, so when a step misbehaves there is no way to see inputs/outputs or timing of each step
# EXPECTED-FINDING: a multi-step LLM workflow with zero tracing instrumentation; intermediate steps are not captured as spans
# EXPECTED-FIX: wrap each step in tracing spans using an LLM observability tool (e.g. LangSmith, OpenTelemetry GenAI, Langfuse) so each step's input/output/latency is recorded
# SEVERITY-HINT: warning
"""A three-step research agent with no tracing whatsoever."""

import json

from anthropic import Anthropic

client = Anthropic()


def _call(prompt: str) -> str:
    resp = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=600,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text


def run_agent(question: str) -> str:
    # Step 1: plan
    plan = _call(f"Break this question into 3 search queries as a JSON list:\n{question}")
    queries = json.loads(plan)

    # Step 2: fan out "searches" (each its own LLM call) - untraced
    findings = []
    for q in queries:
        findings.append(_call(f"Answer concisely: {q}"))

    # Step 3: synthesize - untraced
    joined = "\n".join(findings)
    return _call(f"Synthesize a final answer to '{question}' from:\n{joined}")


if __name__ == "__main__":
    print(run_agent("What caused the 2024 outage and how was it fixed?"))
