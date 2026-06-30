# ACE-EXPECT: detect
# CATEGORY: should_detect/lang_checkpoint_persistence
# LANGUAGE: python
# ISSUE: A long multi-node LangGraph is compiled with no checkpointer, so state is lost on failure
# EXPECTED-FINDING: StateGraph.compile() is called without a checkpointer, leaving the long flow unable to persist or resume
# EXPECTED-FIX: Compile with a checkpointer (e.g. MemorySaver/SqliteSaver) and invoke with a thread_id config
# SEVERITY-HINT: warning
"""A 4-stage research graph compiled without any checkpointer; a crash mid-run discards all progress."""

from typing import TypedDict

from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

llm = ChatOpenAI(model="gpt-4o")


class State(TypedDict):
    topic: str
    outline: str
    draft: str
    review: str


def plan(s: State) -> dict:
    return {"outline": llm.invoke(f"Outline: {s['topic']}").content}


def write(s: State) -> dict:
    return {"draft": llm.invoke(f"Draft from outline: {s['outline']}").content}


def review(s: State) -> dict:
    return {"review": llm.invoke(f"Review draft: {s['draft']}").content}


g = StateGraph(State)
g.add_node("plan", plan)
g.add_node("write", write)
g.add_node("review", review)
g.add_edge(START, "plan")
g.add_edge("plan", "write")
g.add_edge("write", "review")
g.add_edge("review", END)
# compiled with no checkpointer: no thread_id, no durable state, no resume after a failure
app = g.compile()
