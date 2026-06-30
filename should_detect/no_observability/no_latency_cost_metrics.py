# ACE-EXPECT: detect
# CATEGORY: should_detect/no_observability
# LANGUAGE: python
# ISSUE: A production HTTP endpoint serves LLM completions but emits no latency or cost metrics, so there is no way to monitor p95 latency or spend per request
# EXPECTED-FINDING: an LLM-serving endpoint with no measurement of per-request latency or estimated cost (no timing, no token->cost calculation, no metrics emission)
# EXPECTED-FIX: measure request latency (e.g. time.perf_counter around the call) and compute cost from usage * model pricing, then emit both to a metrics backend (Prometheus/StatsD/OpenTelemetry)
# SEVERITY-HINT: warning
"""FastAPI endpoint that answers questions with no latency/cost instrumentation."""

from anthropic import Anthropic
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
client = Anthropic()


class Query(BaseModel):
    question: str


@app.post("/answer")
def answer(query: Query) -> dict:
    # No timing, no cost accounting - we just call and return.
    resp = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=500,
        messages=[{"role": "user", "content": query.question}],
    )
    return {"answer": resp.content[0].text}
