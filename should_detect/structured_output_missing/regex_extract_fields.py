# ACE-EXPECT: detect
# CATEGORY: should_detect/structured_output_missing
# LANGUAGE: python
# ISSUE: Structured fields are scraped out of free-text model output with regular expressions
# EXPECTED-FINDING: The LLM is prompted in natural language and the answer is parsed with re.search patterns instead of a schema
# EXPECTED-FIX: Request schema-enforced structured output (response_format with a json_schema / Pydantic model) so fields arrive as typed data, not regex-matched text
# SEVERITY-HINT: warning
"""Pull a sentiment label and score out of an LLM reply using regex."""

import re

from openai import OpenAI

client = OpenAI()


def classify_review(review: str) -> dict:
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Classify the review. Reply with a line 'Sentiment: <positive|negative>' "
                    "and a line 'Score: <0-100>'."
                ),
            },
            {"role": "user", "content": review},
        ],
    )

    text = resp.choices[0].message.content

    # Brittle: depends on the model emitting exactly this text shape every time.
    sentiment_match = re.search(r"Sentiment:\s*(\w+)", text)
    score_match = re.search(r"Score:\s*(\d+)", text)

    return {
        "sentiment": sentiment_match.group(1) if sentiment_match else None,
        "score": int(score_match.group(1)) if score_match else None,
    }


if __name__ == "__main__":
    print(classify_review("Honestly the best purchase I've made all year."))
