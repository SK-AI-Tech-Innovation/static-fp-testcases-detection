# ACE-EXPECT: detect
# CATEGORY: should_detect/token_budget_unbounded
# LANGUAGE: python
# ISSUE: An entire large document is stuffed into the prompt with no chunking, retrieval, or size limit
# EXPECTED-FINDING: The full file contents are inlined into a single prompt regardless of size, wasting tokens and risking context-window overflow
# EXPECTED-FIX: Chunk/retrieve only the relevant sections (RAG), cap input length, or truncate to a token budget before sending
# SEVERITY-HINT: warning
"""Answer a question over a document by dumping the whole file into the prompt."""

from pathlib import Path

from anthropic import Anthropic

client = Anthropic()


def answer_over_document(doc_path: str, question: str) -> str:
    # Reads the ENTIRE document (could be megabytes) and inlines all of it into one prompt.
    # No chunking, no retrieval of relevant passages, no length cap: a large file
    # explodes the token count, costs a fortune, and can exceed the context window.
    full_text = Path(doc_path).read_text(encoding="utf-8")
    response = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": f"Here is the full document:\n\n{full_text}\n\nQuestion: {question}",
            }
        ],
    )
    return response.content[0].text


if __name__ == "__main__":
    print(answer_over_document("annual_report.txt", "What was net revenue?"))
