# ACE-EXPECT: detect
# CATEGORY: should_detect/lang_composable_runnables
# LANGUAGE: python
# ISSUE: A retrieval-augmented answer flow is wired manually (retrieve, format, prompt, model, parse) step by step
# EXPECTED-FINDING: Hand-wired RAG glue bypasses LCEL composition (RunnableParallel/RunnablePassthrough) for context injection
# EXPECTED-FIX: Compose retriever and question via RunnableParallel into prompt | model | parser as one Runnable
# SEVERITY-HINT: suggestion
"""RAG answerer assembled by hand instead of as a composable LCEL chain."""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_template(
    "Use the context to answer.\nContext:\n{context}\n\nQuestion: {question}"
)
model = ChatOpenAI(model="gpt-4o", temperature=0)
parser = StrOutputParser()


def answer(retriever, question: str) -> str:
    docs = retriever.invoke(question)
    context = "\n\n".join(d.page_content for d in docs)
    messages = prompt.invoke({"context": context, "question": question})
    response = model.invoke(messages)
    return parser.invoke(response)
