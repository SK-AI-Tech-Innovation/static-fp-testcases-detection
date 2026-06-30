# ACE-EXPECT: detect
# CATEGORY: should_detect/tool_error_semantics
# LANGUAGE: python
# ISSUE: A weather tool lets requests.HTTPError propagate uncaught instead of returning a structured error to the LLM
# EXPECTED-FINDING: A 404/429/500 from the upstream API raises an unhandled HTTPError, crashing the agent turn rather than giving the model a recoverable error it can act on
# EXPECTED-FIX: Catch HTTP/connection errors and return a structured object (error_code, message, recoverable, suggestion) so the model can retry or ask the user
# SEVERITY-HINT: warning
"""A get_weather tool backed by an HTTP API, used by an agent's tool layer."""

import requests

BASE_URL = "https://api.example-weather.com/v1/current"


def get_weather(city: str) -> dict:
    """Return current weather for a city as a dict of {temp_c, conditions}."""
    resp = requests.get(BASE_URL, params={"q": city}, timeout=10)
    # raise_for_status() throws HTTPError on 4xx/5xx and nothing catches it here.
    resp.raise_for_status()
    body = resp.json()
    return {
        "city": city,
        "temp_c": body["temperature_celsius"],
        "conditions": body["conditions"],
    }


def run_tool(tool_name: str, **kwargs: str) -> dict:
    """Tool dispatcher invoked by the agent runtime."""
    if tool_name == "get_weather":
        # Propagated HTTPError surfaces here too — no structured fallback.
        return get_weather(kwargs["city"])
    raise KeyError(tool_name)
