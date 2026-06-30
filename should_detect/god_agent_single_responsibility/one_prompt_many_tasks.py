# ACE-EXPECT: detect
# CATEGORY: should_detect/god_agent_single_responsibility
# LANGUAGE: python
# ISSUE: A single LLM call is asked to classify, summarize, translate, and score in one prompt, overloading one step with unrelated tasks
# EXPECTED-FINDING: process_review packs four distinct tasks (classification, summarization, translation, sentiment scoring) into one prompt/response, making each result entangled, unvalidatable, and hard to evaluate
# EXPECTED-FIX: Split into separate, single-purpose calls (or a structured-output pipeline) for classify, summarize, translate, and score, each with its own schema and prompt
# SEVERITY-HINT: warning
"""One LLM call asked to do classification + summarization + translation + scoring at once."""

from openai import OpenAI

client = OpenAI()


def process_review(review_text: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "Do ALL of the following for the review and return everything: "
                    "1) classify it into one of [bug, praise, feature-request], "
                    "2) write a one-sentence summary, "
                    "3) translate the summary to Korean, "
                    "4) give a sentiment score from -1.0 to 1.0."
                ),
            },
            {"role": "user", "content": review_text},
        ],
    )
    # All four results come back tangled in one free-text blob.
    return resp.choices[0].message.content


if __name__ == "__main__":
    print(process_review("The app keeps crashing when I open settings."))
