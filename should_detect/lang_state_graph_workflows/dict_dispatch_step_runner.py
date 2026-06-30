# ACE-EXPECT: detect
# CATEGORY: should_detect/lang_state_graph_workflows
# LANGUAGE: python
# ISSUE: Workflow steps dispatched via a hand-rolled dict-of-functions instead of a LangGraph StateGraph
# EXPECTED-FINDING: Step sequencing is a manual function-table loop with no explicit graph nodes/edges/state schema
# EXPECTED-FIX: Define each step as a StateGraph node with explicit edges so routing and state are declarative
# SEVERITY-HINT: warning
"""A multi-stage extraction pipeline orchestrated by a dict dispatch table and a for-loop."""

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")


def extract(state: dict) -> dict:
    state["entities"] = llm.invoke(f"Extract entities: {state['doc']}").content
    return state


def normalize(state: dict) -> dict:
    state["normalized"] = llm.invoke(f"Normalize: {state['entities']}").content
    return state


def summarize(state: dict) -> dict:
    state["summary"] = llm.invoke(f"Summarize: {state['normalized']}").content
    return state


STEPS = {"extract": extract, "normalize": normalize, "summarize": summarize}
ORDER = ["extract", "normalize", "summarize"]


def run(doc: str) -> dict:
    state = {"doc": doc}
    # manual dispatch through a function table — no StateGraph, no edges, no conditional routing
    for name in ORDER:
        state = STEPS[name](state)
    return state
