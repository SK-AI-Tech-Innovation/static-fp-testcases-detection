# ACE-EXPECT: detect
# CATEGORY: should_detect/lang_state_graph_workflows
# LANGUAGE: python
# ISSUE: Intent routing implemented as an if/elif/else chain instead of a LangGraph StateGraph
# EXPECTED-FINDING: Agent orchestration uses hand-rolled if/elif branching for routing, not explicit nodes/edges/conditional routing
# EXPECTED-FIX: Model the router as a LangGraph StateGraph with a conditional edge dispatching to handler nodes
# SEVERITY-HINT: warning
"""Customer-support bot whose intent dispatch is a fragile if/elif/else ladder."""

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")


def classify_intent(text: str) -> str:
    out = llm.invoke(f"Classify into refund|status|complaint|other:\n{text}")
    return out.content.strip().lower()


def handle(text: str) -> str:
    intent = classify_intent(text)
    # routing as branching logic rather than a StateGraph with conditional edges
    if intent == "refund":
        return llm.invoke(f"Draft a refund response: {text}").content
    elif intent == "status":
        return llm.invoke(f"Draft an order-status response: {text}").content
    elif intent == "complaint":
        return llm.invoke(f"Draft an apology for: {text}").content
    else:
        return llm.invoke(f"Draft a generic helpful response: {text}").content


if __name__ == "__main__":
    print(handle("Where is my package?"))
