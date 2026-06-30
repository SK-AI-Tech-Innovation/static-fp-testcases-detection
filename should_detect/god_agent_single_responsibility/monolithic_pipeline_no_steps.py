# ACE-EXPECT: detect
# CATEGORY: should_detect/god_agent_single_responsibility
# LANGUAGE: python
# ISSUE: A multi-stage data-to-LLM pipeline (load, clean, chunk, embed, retrieve, generate, persist) is written as one long inline function with no step boundaries
# EXPECTED-FINDING: run_pipeline inlines loading, cleaning, chunking, embedding, retrieval, generation, and persistence as one continuous flow, so stages cannot be retried, tested, or reordered independently
# EXPECTED-FIX: Extract each stage into a named function with a clear input/output contract and compose them in an explicit pipeline (or step list), enabling per-stage testing, retry, and reuse
# SEVERITY-HINT: warning
"""A RAG-style pipeline written as one monolithic function with no extracted steps."""

import re

from openai import OpenAI

client = OpenAI()


def run_pipeline(raw_docs: list[str], question: str) -> str:
    # load + clean
    cleaned = [re.sub(r"\s+", " ", d).strip() for d in raw_docs if d.strip()]

    # chunk
    chunks = []
    for doc in cleaned:
        for i in range(0, len(doc), 500):
            chunks.append(doc[i : i + 500])

    # embed
    embeds = []
    for ch in chunks:
        e = client.embeddings.create(model="text-embedding-3-small", input=ch)
        embeds.append(e.data[0].embedding)

    # naive retrieval (keyword overlap, inline)
    q_words = set(question.lower().split())
    scored = sorted(
        chunks, key=lambda c: len(q_words & set(c.lower().split())), reverse=True
    )
    context = "\n".join(scored[:3])

    # generate
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"Use this context:\n{context}"},
            {"role": "user", "content": question},
        ],
    )
    answer = resp.choices[0].message.content

    # persist
    with open("/tmp/answers.log", "a") as fh:
        fh.write(answer + "\n")

    return answer


if __name__ == "__main__":
    print(run_pipeline(["doc one text", "doc two text"], "what is this?"))
