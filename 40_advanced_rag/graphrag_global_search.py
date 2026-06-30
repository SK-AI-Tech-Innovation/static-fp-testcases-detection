# ACE-EXPECT: detect
# CATEGORY: 40_advanced_rag
# RELABELED (ground-truth fix): `map_community` does json.loads(resp.content[0].text)
#   on Anthropic free-text with NO schema enforcement — a genuine structured-output
#   violation. Originally mislabeled clean (the file's intent was the no-retrieval axis).
# SOURCE: Microsoft GraphRAG — global search (map-reduce over community summaries)
# WHY-CORRECT: GraphRAG global search answers corpus-wide ("sense-making") questions by a
#   MAP-REDUCE over precomputed community summaries: map the query against each community summary
#   to produce partial answers with scores, then reduce the top partials into a final answer.
#   There is intentionally NO vector top-k retrieval here — global search does not embed/search
#   chunks; it reasons over the community report hierarchy.
# EXPECTED-WRONG: engine may flag "no vector store / no embedding retrieval -> RAG without
#   retrieval", or claim the missing top-k similarity search is a bug.
# CORRECT-VERDICT: no findings
"""GraphRAG global search: map-reduce over community summaries (no vector top-k by design)."""
import json

import anthropic

llm = anthropic.Anthropic()


def map_community(query: str, community_summary: str) -> dict:
    resp = llm.messages.create(
        model="claude-haiku-4-5",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Community summary:\n{community_summary}\n\n"
                    f"Question: {query}\n"
                    'Respond as JSON {"answer": str, "score": 0-100}.'
                ),
            }
        ],
    )
    return json.loads(resp.content[0].text)


def global_search(query: str, community_summaries: list[str]) -> str:
    partials = [map_community(query, s) for s in community_summaries]
    partials.sort(key=lambda p: p["score"], reverse=True)
    context = "\n".join(f"- {p['answer']}" for p in partials if p["score"] > 0)
    final = llm.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=600,
        messages=[
            {"role": "user", "content": f"Question: {query}\nPartial answers:\n{context}\nSynthesize."}
        ],
    )
    return final.content[0].text


if __name__ == "__main__":
    summaries = ["Cluster A: supply chain", "Cluster B: pricing strategy"]
    print(global_search("What are the main themes?", summaries))
