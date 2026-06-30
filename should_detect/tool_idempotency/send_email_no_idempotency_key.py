# ACE-EXPECT: detect
# CATEGORY: should_detect/tool_idempotency
# LANGUAGE: python
# ISSUE: A send-email tool has no idempotency/dedup key and is re-invoked by the agent loop, so retries send duplicate emails
# EXPECTED-FINDING: A transient SMTP/API failure triggers a retry that sends the same notification again; the recipient receives duplicate emails
# EXPECTED-FIX: Attach a dedup key (e.g. SendGrid's "X-Message-Id" / a stable message_id stored before send) and skip the send if that key was already delivered
# SEVERITY-HINT: warning
"""A send_notification tool for a customer-onboarding agent with at-most-once intent."""

import time

import requests

SENDGRID_URL = "https://api.sendgrid.com/v3/mail/send"


def send_notification(to_email: str, subject: str, body: str, api_key: str) -> int:
    """Send a transactional email; returns the HTTP status code."""
    payload = {
        "personalizations": [{"to": [{"email": to_email}]}],
        "from": {"email": "noreply@example.com"},
        "subject": subject,
        "content": [{"type": "text/plain", "value": body}],
    }
    # No unique message key in the payload — provider can't dedup retries.
    resp = requests.post(
        SENDGRID_URL,
        json=payload,
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.status_code


def notify_with_retry(to_email: str, subject: str, body: str, api_key: str) -> int:
    """Agent tool that retries the send on failure — re-sends the email each time."""
    for attempt in range(4):
        try:
            return send_notification(to_email, subject, body, api_key)
        except requests.RequestException:
            time.sleep(1 + attempt)
    raise RuntimeError("email send failed after retries")
