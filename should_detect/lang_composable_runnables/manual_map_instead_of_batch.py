# ACE-EXPECT: detect
# CATEGORY: should_detect/lang_composable_runnables
# LANGUAGE: python
# ISSUE: A Python for-loop maps a chain over inputs one at a time instead of using .batch() or RunnableParallel
# EXPECTED-FINDING: Serial per-item invokes forgo concurrency and the Runnable batch API, hurting throughput
# EXPECTED-FIX: Build the chain with LCEL and call chain.batch(inputs) (or RunnableParallel) for parallel execution
# SEVERITY-HINT: suggestion
"""Batch classifier that loops manually instead of using the Runnable batch API."""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_template("Classify the topic of: {text}")
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
parser = StrOutputParser()


def classify_all(texts: list[str]) -> list[str]:
    results = []
    for text in texts:
        messages = prompt.invoke({"text": text})
        response = model.invoke(messages)
        results.append(parser.invoke(response))
    return results
