# ACE-EXPECT: detect
# CATEGORY: should_detect/obs_trace_propagation
# LANGUAGE: python
# ISSUE: LangGraph multi-node flow logs each LLM node with no run/thread correlation id
# EXPECTED-FINDING: Node-level logs and LLM calls carry no shared run_id/thread_id, so a single graph execution can't be reconstructed
# EXPECTED-FIX: Put a run_id/thread_id into the graph state and include it in every node's logs and LLM metadata
# SEVERITY-HINT: suggestion
"""Two-node LangGraph (classify -> respond) whose logs have nothing tying the nodes to one run."""

import logging
from typing import TypedDict

from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

logger = logging.getLogger("flow")
llm = ChatOpenAI(model="gpt-4o")


class State(TypedDict):
    text: str
    label: str
    reply: str


def classify(state: State) -> dict:
    logger.info("classifying")  # no run/thread id in the log
    out = llm.invoke(f"Label the sentiment of: {state['text']}")
    return {"label": out.content}


def respond(state: State) -> dict:
    logger.info("responding")  # again, nothing correlates this to the classify call
    out = llm.invoke(f"Write a reply for a {state['label']} message: {state['text']}")
    return {"reply": out.content}


graph = StateGraph(State)
graph.add_node("classify", classify)
graph.add_node("respond", respond)
graph.add_edge(START, "classify")
graph.add_edge("classify", "respond")
graph.add_edge("respond", END)
app = graph.compile()
