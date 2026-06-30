# ACE-EXPECT: detect
# CATEGORY: should_detect/rag_no_grounding
# LANGUAGE: python
# ISSUE: Retrieval uses top_k=1 with no reranking, so a single nearest-neighbor chunk is the model's only grounding — if that one chunk is the wrong one, the answer is wrong, and there is no recall headroom
# EXPECTED-FINDING: Naive single-result retrieval (top_k=1) with no reranking step, giving the generator almost no context to ground on
# EXPECTED-FIX: Retrieve more candidates (e.g. top_k 8-20) and apply a reranker to select the best few, improving recall and grounding quality
# SEVERITY-HINT: warning
"""RAG that retrieves only the single closest vector with no rerank stage."""

import anthropic

client = anthropic.Anthropic()


def vector_search(query: str, top_k: int) -> list[str]:
    # Stand-in for a vector DB query returning the top_k nearest chunks.
    raise NotImplementedError


def answer_question(question: str) -> str:
    # top_k=1 and no reranker: the entire answer rests on one nearest neighbor.
    chunks = vector_search(question, top_k=1)
    context = chunks[0] if chunks else ""

    prompt = (
        f"Answer using only the context below.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n\nAnswer:"
    )

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


if __name__ == "__main__":
    print(answer_question("What is the warranty period for the X200?"))
