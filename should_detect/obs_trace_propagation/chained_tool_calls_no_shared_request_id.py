# ACE-EXPECT: detect
# CATEGORY: should_detect/obs_trace_propagation
# LANGUAGE: python
# ISSUE: A chain of tool calls each hits external services with no shared request id
# EXPECTED-FINDING: Each step in the tool chain logs/calls independently with no propagated request id to link them
# EXPECTED-FIX: Create one request_id at chain entry and pass it into every tool call and log statement
# SEVERITY-HINT: suggestion
"""Enrichment pipeline (geocode -> weather -> advise) where each tool call is untraceable across steps."""

import logging

import httpx
from anthropic import Anthropic

logger = logging.getLogger("enrich")
client = Anthropic()


def geocode(city: str) -> dict:
    logger.info("geocode %s", city)  # standalone log, no request id
    return httpx.get("https://geo.example/api", params={"q": city}).json()


def weather(lat: float, lon: float) -> dict:
    logger.info("weather %s,%s", lat, lon)  # cannot be linked to the geocode above
    return httpx.get("https://wx.example/api", params={"lat": lat, "lon": lon}).json()


def advise(city: str) -> str:
    loc = geocode(city)
    wx = weather(loc["lat"], loc["lon"])
    logger.info("advising")  # no correlation id tying the whole chain together
    resp = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=256,
        messages=[{"role": "user", "content": f"Given weather {wx}, what should I wear?"}],
    )
    return resp.content[0].text
