# ACE-EXPECT: detect
# CATEGORY: should_detect/test_deterministic_mocking
# LANGUAGE: python
# ISSUE: LangChain chain unit test invokes a real ChatOpenAI model instead of a fake/mock LLM
# EXPECTED-FINDING: Real model in the chain makes the test slow, costly, network-bound, and non-reproducible
# EXPECTED-FIX: Swap ChatOpenAI for langchain_core.runnables FakeListLLM or a patched client returning fixed output
# SEVERITY-HINT: warning
"""Unit test for a LangChain prompt->model->parser chain using a live model."""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


def build_chain():
    prompt = ChatPromptTemplate.from_template("Give a fun fact about {topic}.")
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    return prompt | model | StrOutputParser()


def test_chain_produces_fact():
    chain = build_chain()
    result = chain.invoke({"topic": "octopuses"})
    assert isinstance(result, str)
    assert len(result) > 10
