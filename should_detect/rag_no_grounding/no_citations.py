# ACE-EXPECT: detect
# CATEGORY: should_detect/rag_no_grounding
# LANGUAGE: python
# ISSUE: Retrieved chunks carry source identifiers, but the prompt never asks the model to cite which source each claim comes from — answers are unverifiable in a domain (legal/policy) where attribution matters
# EXPECTED-FINDING: No citation/source-attribution instruction in a RAG flow whose chunks have source IDs, so the user cannot trace answers back to documents
# EXPECTED-FIX: Label each chunk with its source ID in the prompt and instruct the model to cite the source ID for every claim it makes
# SEVERITY-HINT: warning
"""Policy-lookup RAG that returns answers with no source attribution."""

import anthropic

client = anthropic.Anthropic()


def answer_policy_question(question: str, docs: list[dict]) -> str:
    # Each doc has a usable source id, but we throw it away when building the prompt.
    context = "\n\n".join(d["text"] for d in docs)

    prompt = (
        f"Answer the question using the context below.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n\nAnswer:"
        # No request to cite which document each statement comes from.
    )

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


if __name__ == "__main__":
    docs = [
        {"source": "HR-POL-12", "text": "Employees accrue 1.5 vacation days per month."},
        {"source": "HR-POL-19", "text": "Unused vacation rolls over up to 10 days."},
    ]
    print(answer_policy_question("How does vacation accrual and rollover work?", docs))
