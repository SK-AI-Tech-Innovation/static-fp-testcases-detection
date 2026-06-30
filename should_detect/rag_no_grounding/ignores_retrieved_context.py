# ACE-EXPECT: detect
# CATEGORY: should_detect/rag_no_grounding
# LANGUAGE: python
# ISSUE: The code runs retrieval and gets relevant chunks, but never injects them into the prompt — the model answers the question with no context at all, defeating the purpose of RAG
# EXPECTED-FINDING: Retrieved context is fetched but dropped (unused variable) instead of being placed into the prompt, so answers are ungrounded
# EXPECTED-FIX: Inject the retrieved chunks into the prompt and instruct the model to ground its answer in them
# SEVERITY-HINT: critical
"""RAG pipeline that retrieves chunks then forgets to put them in the prompt."""

import anthropic

client = anthropic.Anthropic()


def retrieve(query: str) -> list[str]:
    # Pretend vector search; returns relevant passages.
    return ["Refunds are issued within 14 business days to the original payment method."]


def answer_question(question: str) -> str:
    chunks = retrieve(question)  # retrieved, but never used below
    _ = chunks

    # Bug: context is missing from the prompt entirely — pure parametric guess.
    prompt = f"Question: {question}\n\nAnswer:"

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


if __name__ == "__main__":
    print(answer_question("How long do refunds take?"))
