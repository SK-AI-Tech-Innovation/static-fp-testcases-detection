# ACE-EXPECT: detect
# CATEGORY: should_detect/lang_state_graph_workflows
# LANGUAGE: python
# ISSUE: Tool selection done with nested if branching instead of LangGraph conditional routing
# EXPECTED-FINDING: Which tool runs is decided by nested if/else on model output rather than StateGraph conditional edges
# EXPECTED-FIX: Use a LangGraph StateGraph with add_conditional_edges to route to tool nodes
# SEVERITY-HINT: warning
"""An assistant that picks a tool via deeply nested if/else on the model's chosen action and confidence."""

import json

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")


def search_web(q: str) -> str:
    return f"results for {q}"


def query_db(q: str) -> str:
    return f"rows for {q}"


def route(question: str) -> str:
    decision = json.loads(
        llm.invoke(f'Return JSON {{"tool": "...", "confidence": 0-1, "arg": "..."}} for: {question}').content
    )
    # nested if branching to choose/guard tools instead of conditional edges in a graph
    if decision["tool"] == "web":
        if decision["confidence"] > 0.5:
            return search_web(decision["arg"])
        else:
            return "low confidence, asking user to clarify"
    else:
        if decision["confidence"] > 0.5:
            return query_db(decision["arg"])
        else:
            return search_web(decision["arg"])
