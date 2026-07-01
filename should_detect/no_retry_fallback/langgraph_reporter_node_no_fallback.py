# ACE-EXPECT: detect
# CATEGORY: should_detect/no_retry_fallback
# LANGUAGE: python
# SOURCE: SK ATIT project feedback — CSwind (Notion: https://app.notion.com/p/sk-atit/CSwind-d1d1772c74d5839db2c281ee42cd0346)
# ISSUE: The final reporter node of a LangGraph pipeline calls the LLM once with no retry/fallback, so a transient API error discards every upstream node's work
# EXPECTED-FINDING: The terminal `report` node issues a single unguarded LLM call; a 429/5xx or timeout there propagates out of the graph and loses all prior node results, with no retry, backoff, or degraded fallback path
# EXPECTED-FIX: Wrap the reporter LLM call with bounded retries + exponential backoff (tenacity / SDK max_retries) and a fallback (cached/secondary model or partial report) so a late transient failure does not throw away the whole run
# SEVERITY-HINT: warning
"""Multi-node LangGraph report pipeline whose final LLM call has no resilience.

The expensive upstream nodes (fetch, analyze) succeed and populate the state, but the
terminal reporter node calls the model exactly once. If that single call fails on a
transient server error, the entire pipeline's accumulated work is lost.
"""
from typing import TypedDict

from langgraph.graph import END, START, StateGraph
from openai import OpenAI

client = OpenAI()


class PipelineState(TypedDict):
    repo: str
    findings: list[str]
    report: str


def fetch_node(state: PipelineState) -> dict:
    # Pretend this pulls and prepares a large amount of context (slow / costly).
    return {"findings": []}


def analyze_node(state: PipelineState) -> dict:
    # Expensive multi-step analysis whose results live only in graph state.
    findings = [f"finding about {state['repo']}", "another finding"]
    return {"findings": findings}


def report_node(state: PipelineState) -> dict:
    # The ONLY place the final answer is produced — and it is a single naked call.
    # If the service is overloaded (429) or returns a 5xx here, this raises and the
    # graph aborts: fetch + analyze work is thrown away with nothing to resume from.
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Write a final report from these findings."},
            {"role": "user", "content": "\n".join(state["findings"])},
        ],
    )
    return {"report": response.choices[0].message.content}


def build_graph() -> object:
    graph = StateGraph(PipelineState)
    graph.add_node("fetch", fetch_node)
    graph.add_node("analyze", analyze_node)
    graph.add_node("report", report_node)
    graph.add_edge(START, "fetch")
    graph.add_edge("fetch", "analyze")
    graph.add_edge("analyze", "report")
    graph.add_edge("report", END)
    return graph.compile()


def run(repo: str) -> str:
    result = build_graph().invoke({"repo": repo, "findings": [], "report": ""})
    return result["report"]
