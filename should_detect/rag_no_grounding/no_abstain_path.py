# ACE-EXPECT: detect
# CATEGORY: should_detect/rag_no_grounding
# LANGUAGE: python
# ISSUE: When retrieval returns nothing (or irrelevant chunks), the code still asks the model to answer, and the prompt gives no instruction to abstain — so the model invents an answer with zero supporting context
# EXPECTED-FINDING: No abstention path — empty/insufficient context is sent to the model anyway, with no "say you don't know" instruction or short-circuit
# EXPECTED-FIX: Instruct the model to reply "I don't know" when the context does not contain the answer, and/or short-circuit when retrieval is empty
# SEVERITY-HINT: critical
"""RAG QA with no 'I don't know' instruction and no handling of empty retrieval."""

import anthropic

client = anthropic.Anthropic()


def answer_question(question: str, retrieved_chunks: list[str]) -> str:
    # retrieved_chunks may be empty (no relevant docs), but we proceed regardless.
    context = "\n\n".join(retrieved_chunks)

    prompt = (
        f"Use the context to answer the question.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n\nAnswer:"
        # No instruction permitting the model to abstain when context is missing.
    )

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


if __name__ == "__main__":
    # Empty retrieval — the model will confidently make something up.
    print(answer_question("What is our 2027 parental-leave policy?", []))
