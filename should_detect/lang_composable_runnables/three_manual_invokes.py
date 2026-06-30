# ACE-EXPECT: detect
# CATEGORY: should_detect/lang_composable_runnables
# LANGUAGE: python
# ISSUE: prompt -> llm -> parse implemented as three sequential manual .invoke() calls with hand glue
# EXPECTED-FINDING: Manual chaining bypasses LCEL, losing streaming, batching, and composability benefits
# EXPECTED-FIX: Compose as a single Runnable: prompt | llm | StrOutputParser() and call once
# SEVERITY-HINT: suggestion
"""Headline generator wired by hand instead of using LCEL composition."""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_template("Write a headline for: {article}")
model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
parser = StrOutputParser()


def generate_headline(article: str) -> str:
    messages = prompt.invoke({"article": article})
    response = model.invoke(messages)
    headline = parser.invoke(response)
    return headline
