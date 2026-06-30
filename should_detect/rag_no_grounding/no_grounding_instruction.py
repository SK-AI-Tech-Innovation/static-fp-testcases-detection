# ACE-EXPECT: detect
# CATEGORY: should_detect/rag_no_grounding
# LANGUAGE: python
# ISSUE: Retrieved context is injected into the prompt, but the model is never told to answer ONLY from that context, so it is free to answer from its own parametric knowledge and hallucinate
# EXPECTED-FINDING: RAG prompt that supplies context but omits any grounding directive constraining the answer to the retrieved passages
# EXPECTED-FIX: Add an explicit grounding instruction (e.g. "Answer using only the provided context; do not use outside knowledge")
# SEVERITY-HINT: critical
"""RAG QA that pastes context but never tells the model to stay grounded in it."""

import anthropic

client = anthropic.Anthropic()


def answer_question(question: str, retrieved_chunks: list[str]) -> str:
    context = "\n\n".join(retrieved_chunks)

    # Context is present, but there is no instruction to rely on it exclusively.
    prompt = f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


if __name__ == "__main__":
    chunks = ["The Acme X200 router supports Wi-Fi 6 and has 4 gigabit ports."]
    print(answer_question("How many ports does the X200 have?", chunks))
