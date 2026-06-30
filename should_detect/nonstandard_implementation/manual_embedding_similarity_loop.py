# ACE-EXPECT: detect
# CATEGORY: should_detect/nonstandard_implementation
# LANGUAGE: python
# ISSUE: Semantic search is done by re-embedding the whole corpus on every query and computing cosine similarity in a pure-Python O(n) loop, which does not scale and recomputes embeddings each call
# EXPECTED-FINDING: a hand-rolled in-memory cosine-similarity loop over an embedded corpus used as a retrieval mechanism, with no persistent index
# EXPECTED-FIX: store embeddings in a vector database / ANN index (FAISS, Chroma, pgvector, Pinecone) and query it for nearest neighbors instead of looping in Python
# SEVERITY-HINT: warning
"""Hand-rolled cosine-similarity search over a large corpus, recomputed per query."""

import math

from openai import OpenAI

client = OpenAI()

CORPUS = [f"document number {i} about various topics" for i in range(50_000)]


def embed(text: str) -> list[float]:
    resp = client.embeddings.create(model="text-embedding-3-small", input=text)
    return resp.data[0].embedding


def cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb)


def search(query: str, top_k: int = 3) -> list[str]:
    q_vec = embed(query)
    scored = []
    # Re-embeds and scans the entire corpus on every single query.
    for doc in CORPUS:
        d_vec = embed(doc)
        scored.append((cosine(q_vec, d_vec), doc))
    scored.sort(reverse=True)
    return [doc for _, doc in scored[:top_k]]


if __name__ == "__main__":
    print(search("find me a relevant document"))
