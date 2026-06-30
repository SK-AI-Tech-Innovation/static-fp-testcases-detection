# ACE-EXPECT: detect
# CATEGORY: should_detect/prompt_context_hierarchy
# LANGUAGE: python
# ISSUE: A RAG answer prompt dumps all retrieved context first and places the actual task instruction at the very end
# EXPECTED-FINDING: The critical "answer only from context, cite sources, say I don't know" instruction is buried after a large context block, violating primacy and weakening compliance
# EXPECTED-FIX: Put the instruction/constraints at the top of the prompt before the retrieved context (or in the system message), with the context clearly delimited afterward
# SEVERITY-HINT: warning
"""Build a RAG answer prompt from retrieved passages and call the chat model."""

from anthropic import Anthropic

client = Anthropic()


def answer_question(question: str, passages: list[str]) -> str:
    context_block = "\n\n".join(f"[{i}] {p}" for i, p in enumerate(passages))
    prompt = (
        f"Here are the retrieved documents:\n\n{context_block}\n\n"
        f"User question: {question}\n\n"
        # Critical instruction comes dead last, after a huge context dump.
        "Now answer the question using ONLY the documents above. "
        "Cite the bracketed source numbers you used. "
        "If the answer is not in the documents, say 'I don't know'."
    )
    resp = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text
