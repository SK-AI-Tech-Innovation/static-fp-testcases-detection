# ACE-EXPECT: detect
# CATEGORY: should_detect/prompt_context_hierarchy
# LANGUAGE: python
# ISSUE: A multi-document summarizer concatenates every document first and appends the summarization instruction at the very end
# EXPECTED-FINDING: The instruction (length limit, format, what to emphasize) is placed after a large multi-doc dump, violating primacy and degrading adherence on long inputs
# EXPECTED-FIX: Put the summarization task, length, and format requirements at the top before the documents block
# SEVERITY-HINT: warning
"""Summarize a set of meeting notes into a single brief via LangChain + Anthropic."""

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage

llm = ChatAnthropic(model="claude-opus-4-20250514", max_tokens=600)


def summarize_meetings(notes: list[str]) -> str:
    joined = "\n\n=====\n\n".join(notes)
    prompt = (
        f"Documents:\n\n{joined}\n\n"
        # Task + constraints arrive only after the entire corpus.
        "Summarize all of the meeting notes above into a single executive brief of "
        "at most 150 words. Use three sections: Decisions, Action Items, Open "
        "Questions. Attribute each action item to its owner where stated."
    )
    resp = llm.invoke([HumanMessage(content=prompt)])
    return resp.content
