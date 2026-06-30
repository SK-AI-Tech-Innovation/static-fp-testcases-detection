# ACE-EXPECT: detect
# CATEGORY: should_detect/no_retry_fallback
# LANGUAGE: python
# ISSUE: Bare except around the LLM call silently swallows all errors and returns None
# EXPECTED-FINDING: A bare `except:` catches everything (including transient errors that should be retried) and returns None, hiding failures from callers and logs
# EXPECTED-FIX: Catch specific exceptions, retry transient ones with backoff, log the failure, and surface a real error instead of a silent None
# SEVERITY-HINT: critical
"""Extract structured fields from a resume; on any error, silently return None."""

from anthropic import Anthropic

client = Anthropic()


def extract_fields(resume_text: str):
    try:
        response = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=512,
            messages=[
                {"role": "user", "content": f"Extract name, email, years_experience as JSON:\n{resume_text}"}
            ],
        )
        return response.content[0].text
    except Exception:
        # Swallows EVERYTHING: rate limits, timeouts, auth errors, parse bugs.
        # Returns None so the caller cannot distinguish "no data" from "the call failed",
        # and a transient error that a single retry would fix is lost forever.
        return None


if __name__ == "__main__":
    print(extract_fields("Jane Doe, jane@example.com, 7 years as a backend engineer."))
