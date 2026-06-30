# ACE-EXPECT: detect
# CATEGORY: should_detect/lang_checkpoint_persistence
# LANGUAGE: python
# ISSUE: Human-in-the-loop graph can't pause/resume because it has no checkpointer
# EXPECTED-FINDING: An approval-gated graph is compiled without a checkpointer, so it cannot interrupt and resume across the human decision
# EXPECTED-FIX: Compile with a checkpointer and use interrupt_before plus a thread_id so the run pauses for approval and resumes
# SEVERITY-HINT: warning
"""A spend-approval workflow that blocks inline for input because it has no durable pause/resume."""

from typing import TypedDict

from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

llm = ChatOpenAI(model="gpt-4o")


class ApprovalState(TypedDict):
    request: str
    proposal: str
    decision: str
    result: str


def draft(s: ApprovalState) -> dict:
    return {"proposal": llm.invoke(f"Propose a purchase for: {s['request']}").content}


def execute(s: ApprovalState) -> dict:
    if s["decision"] != "approve":
        return {"result": "rejected"}
    return {"result": llm.invoke(f"Confirm purchase: {s['proposal']}").content}


g = StateGraph(ApprovalState)
g.add_node("draft", draft)
g.add_node("execute", execute)
g.add_edge(START, "draft")
g.add_edge("draft", "execute")
g.add_edge("execute", END)
flow = g.compile()  # no checkpointer and no interrupt_before -> cannot pause for the human


def run(request: str) -> str:
    state = {"request": request, "proposal": "", "decision": "", "result": ""}
    # blocking input() instead of interrupting/resuming a checkpointed graph
    drafted = flow.invoke(state)
    decision = input(f"Approve? {drafted['proposal']}\n> ")
    final = flow.invoke({**drafted, "decision": decision})
    return final["result"]
