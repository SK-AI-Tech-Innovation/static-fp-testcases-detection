# ACE-EXPECT: detect
# CATEGORY: should_detect/no_retry_fallback
# LANGUAGE: python
# ISSUE: Tight loop of LLM calls with no rate-limit (429) handling or pacing
# EXPECTED-FINDING: Batch processing fires requests back-to-back; the first 429 RateLimitError aborts the whole batch with no retry/backoff or Retry-After handling
# EXPECTED-FIX: Catch RateLimitError, respect Retry-After, retry with exponential backoff (tenacity/SDK max_retries), and pace/concurrency-limit the loop
# SEVERITY-HINT: warning
"""Translate a batch of comments in a tight loop with no rate-limit handling."""

from anthropic import Anthropic

client = Anthropic()


def translate_all(comments: list[str]) -> list[str]:
    results = []
    for comment in comments:
        # No 429 handling, no pacing, no backoff. On a large batch this will hit the
        # rate limit and the RateLimitError will bubble up and kill the entire job,
        # losing all progress made so far.
        response = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=200,
            messages=[{"role": "user", "content": f"Translate to English:\n{comment}"}],
        )
        results.append(response.content[0].text)
    return results


if __name__ == "__main__":
    print(translate_all([f"Comentario numero {i}" for i in range(500)]))
