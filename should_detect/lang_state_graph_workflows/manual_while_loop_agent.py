# ACE-EXPECT: detect
# CATEGORY: should_detect/lang_state_graph_workflows
# LANGUAGE: python
# ISSUE: Agent loop hand-rolled as a manual while-loop instead of a LangGraph StateGraph
# EXPECTED-FINDING: The reason/act cycle is a manual while True loop with mutable scratch state, not graph nodes/edges
# EXPECTED-FIX: Express the loop as a LangGraph StateGraph with an agent node and a conditional edge back to itself
# SEVERITY-HINT: warning
"""A tool-using agent whose control flow is a bare while-loop over chat state."""

import json

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")


def calculator(expr: str) -> str:
    return str(eval(expr))  # noqa: S307


def run(question: str) -> str:
    messages = [{"role": "user", "content": question + " You may reply CALL: <expr> to compute."}]
    # manual loop driving the agent instead of a compiled StateGraph
    while True:
        reply = llm.invoke(messages).content
        if reply.startswith("CALL:"):
            result = calculator(reply[len("CALL:"):].strip())
            messages.append({"role": "assistant", "content": reply})
            messages.append({"role": "user", "content": f"Result: {result}"})
            continue
        return reply


if __name__ == "__main__":
    print(run("What is 2300 * 17?"))
