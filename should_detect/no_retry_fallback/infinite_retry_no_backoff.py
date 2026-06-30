# ACE-EXPECT: detect
# CATEGORY: should_detect/no_retry_fallback
# LANGUAGE: python
# ISSUE: `while True` retry loop with no backoff, jitter, or attempt cap
# EXPECTED-FINDING: Failed LLM calls are retried in a tight infinite loop with no delay or maximum attempts, hammering the API and risking a hang during an outage
# EXPECTED-FIX: Use bounded exponential backoff with jitter and a max-attempts cap (e.g. tenacity @retry(stop=stop_after_attempt, wait=wait_exponential)), then give up/fallback
# SEVERITY-HINT: critical
"""Call the model and retry forever with no delay until it eventually succeeds."""

import time

from anthropic import Anthropic

client = Anthropic()


def answer_question(question: str) -> str:
    while True:
        try:
            response = client.messages.create(
                model="claude-opus-4-20250514",
                max_tokens=512,
                messages=[{"role": "user", "content": question}],
            )
            return response.content[0].text
        except Exception:
            # No backoff, no jitter, no attempt cap. During a sustained outage this spins
            # as fast as the CPU allows, amplifying load on an already-struggling API and
            # never giving up. time is imported but the loop never sleeps.
            continue


if __name__ == "__main__":
    print(answer_question("What is the capital of France?"))
    _ = time  # imported deliberately; note the retry loop still never sleeps
