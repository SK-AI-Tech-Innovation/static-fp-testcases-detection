# ACE-EXPECT: detect
# CATEGORY: should_detect/token_budget_unbounded
# LANGUAGE: python
# ISSUE: The same static text is re-embedded on every loop iteration instead of once
# EXPECTED-FINDING: A constant query/document is sent to the embeddings API inside the loop, paying for identical embeddings on each iteration
# EXPECTED-FIX: Compute the embedding once outside the loop (or memoize/cache it) and reuse the vector
# SEVERITY-HINT: warning
"""Score many candidate documents against a fixed query, re-embedding the query every time."""

from openai import OpenAI

client = OpenAI()


def embed(text: str) -> list[float]:
    return client.embeddings.create(model="text-embedding-3-small", input=text).data[0].embedding


def rank_documents(query: str, documents: list[str]) -> list[tuple[str, float]]:
    scored = []
    for doc in documents:
        # The query never changes, but we re-embed it on EVERY iteration. For N documents
        # that is N redundant embedding calls (N-1 wasted), burning tokens and latency.
        query_vec = embed(query)
        doc_vec = embed(doc)
        score = sum(a * b for a, b in zip(query_vec, doc_vec))
        scored.append((doc, score))
    return sorted(scored, key=lambda x: x[1], reverse=True)


if __name__ == "__main__":
    print(rank_documents("best laptop for travel", [f"laptop review {i}" for i in range(200)]))
