# ACE-EXPECT: detect
# CATEGORY: should_detect/god_agent_single_responsibility
# LANGUAGE: python
# ISSUE: Tool-using agent loop interleaves orchestration (deciding next action) with tool implementations (weather, math, search) in one function, so control flow and capabilities are not separated
# EXPECTED-FINDING: agent_loop embeds the tool bodies (get_weather, calculate, web_search) directly inside the reasoning/dispatch loop, conflating the orchestrator with the tools it should merely coordinate
# EXPECTED-FIX: Separate the orchestrator (plan/dispatch/observe loop) from a registry of independent tool functions, so tools are added/tested in isolation and the loop only coordinates them
# SEVERITY-HINT: warning
"""An agent loop with no separation between orchestration and the tool implementations."""

import requests
from openai import OpenAI

client = OpenAI()


def agent_loop(goal: str) -> str:
    history = [{"role": "user", "content": goal}]
    for _ in range(5):
        resp = client.chat.completions.create(model="gpt-4o", messages=history)
        msg = resp.choices[0].message.content
        history.append({"role": "assistant", "content": msg})

        # Orchestration and tool bodies are fused together inline.
        if msg.startswith("WEATHER:"):
            city = msg.split(":", 1)[1].strip()
            data = requests.get(f"https://wttr.in/{city}?format=3").text
            history.append({"role": "user", "content": f"OBSERVATION: {data}"})
        elif msg.startswith("CALC:"):
            expr = msg.split(":", 1)[1].strip()
            result = sum(float(x) for x in expr.split("+"))
            history.append({"role": "user", "content": f"OBSERVATION: {result}"})
        elif msg.startswith("SEARCH:"):
            term = msg.split(":", 1)[1].strip()
            hits = requests.get(f"https://api.example.com/search?q={term}").json()
            history.append({"role": "user", "content": f"OBSERVATION: {hits}"})
        else:
            return msg
    return "gave up"


if __name__ == "__main__":
    print(agent_loop("What's the weather in Seoul?"))
