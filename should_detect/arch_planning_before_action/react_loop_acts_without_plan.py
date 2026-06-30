# ACE-EXPECT: detect
# CATEGORY: should_detect/arch_planning_before_action
# LANGUAGE: python
# ISSUE: ReAct-style multi-tool loop dispatches side-effecting tools with no upfront plan
# EXPECTED-FINDING: Each model thought triggers an immediate tool action (send_email, charge, etc.) with no plan→validate→execute separation
# EXPECTED-FIX: Run a planning pass that produces an ordered tool plan, validate it, then execute the approved steps
# SEVERITY-HINT: warning
"""Bare ReAct agent that interleaves thinking and acting, firing real tools each turn."""

import json
import re

from anthropic import Anthropic

client = Anthropic()


def send_email(to: str, body: str) -> str:
    return f"sent to {to}"


def charge_customer(customer_id: str, amount: float) -> str:
    return f"charged {customer_id} {amount}"


TOOLS = {"send_email": send_email, "charge_customer": charge_customer}


def run_agent(goal: str, max_steps: int = 8) -> None:
    scratch = f"Goal: {goal}\n"
    for _ in range(max_steps):
        resp = client.messages.create(
            model="claude-opus-4-20250514",
            max_tokens=512,
            messages=[{"role": "user", "content": scratch + "\nReply ACTION: <tool> <json-args>"}],
        )
        text = resp.content[0].text
        m = re.search(r"ACTION:\s*(\w+)\s*(\{.*\})", text)
        if not m:
            return
        tool, args = m.group(1), json.loads(m.group(2))
        # acts immediately on the model's thought — no plan was ever built or validated
        observation = TOOLS[tool](**args)
        scratch += f"\nAction: {tool}\nObservation: {observation}\n"
