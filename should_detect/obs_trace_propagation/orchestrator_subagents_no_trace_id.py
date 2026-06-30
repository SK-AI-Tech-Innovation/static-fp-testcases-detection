# ACE-EXPECT: detect
# CATEGORY: should_detect/obs_trace_propagation
# LANGUAGE: python
# ISSUE: Orchestrator fans out to three sub-agents and logs each step, but no trace_id/correlation id is propagated or logged
# EXPECTED-FINDING: Each sub-agent logs independently with no shared correlation id, so a single request cannot be traced across the planner/searcher/writer agents
# EXPECTED-FIX: Generate a trace_id at the orchestrator and thread it through every sub-agent call and bind it to every log line (e.g. structlog contextvars or a trace_id field)
# SEVERITY-HINT: suggestion
"""Research orchestrator that delegates to planner/searcher/writer agents, logging each
hop but with no shared trace context — log lines from concurrent requests interleave
with nothing to correlate them."""

import logging

from openai import OpenAI

logger = logging.getLogger("research")
client = OpenAI()


def _agent(role: str, prompt: str) -> str:
    # logs the call, but the log line carries NO request/trace id
    logger.info("sub-agent start role=%s", role)
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": role}, {"role": "user", "content": prompt}],
    )
    logger.info("sub-agent done role=%s tokens=%s", role, resp.usage.total_tokens)
    return resp.choices[0].message.content


def planner(topic: str) -> str:
    return _agent("You are a planner.", f"Outline a report on {topic}")


def searcher(outline: str) -> str:
    return _agent("You are a researcher.", f"Find facts for:\n{outline}")


def writer(outline: str, facts: str) -> str:
    return _agent("You are a writer.", f"Write the report.\nOutline:{outline}\nFacts:{facts}")


def run(topic: str) -> str:
    # three nested agent calls; logs exist but none carry a request/trace id, so the
    # lines for one user's request cannot be separated from another's in production logs
    logger.info("research run start topic=%s", topic)
    outline = planner(topic)
    facts = searcher(outline)
    report = writer(outline, facts)
    logger.info("research run done")
    return report
