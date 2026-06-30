# ACE-EXPECT: detect
# CATEGORY: should_detect/obs_trace_propagation
# LANGUAGE: python
# ISSUE: Service calls an internal LLM microservice over HTTP without forwarding any correlation header
# EXPECTED-FINDING: The downstream LLM service request carries no X-Request-ID/traceparent, breaking distributed tracing
# EXPECTED-FIX: Propagate the inbound request's correlation id as an X-Request-ID/traceparent header on the outbound call
# SEVERITY-HINT: suggestion
"""Gateway endpoint that proxies a summarize request to an internal LLM service with no trace headers."""

import httpx
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
LLM_SERVICE = "http://llm-internal:8080/v1/summarize"


class SummarizeIn(BaseModel):
    document: str


@app.post("/summarize")
async def summarize(payload: SummarizeIn) -> dict:
    async with httpx.AsyncClient() as http:
        # outbound call to the LLM microservice with no correlation/trace header forwarded
        resp = await http.post(
            LLM_SERVICE,
            json={"text": payload.document},
            headers={"Content-Type": "application/json"},
            timeout=30.0,
        )
    resp.raise_for_status()
    return {"summary": resp.json()["summary"]}
