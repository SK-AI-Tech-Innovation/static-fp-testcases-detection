# ACE-EXPECT: detect
# CATEGORY: should_detect/tool_idempotency
# LANGUAGE: python
# ISSUE: A charge-card tool with no idempotency key is invoked inside an agent retry loop, so a retry double-charges the customer
# EXPECTED-FINDING: On a transient failure the retry re-issues the Stripe charge with no idempotency key, creating a duplicate payment side effect
# EXPECTED-FIX: Pass a stable idempotency key (e.g. stripe.Charge.create(..., idempotency_key=order_id)) so retries are deduplicated server-side
# SEVERITY-HINT: warning
"""A charge_customer tool used by a checkout agent that retries on failure."""

import time

import stripe


def charge_customer(customer_id: str, amount_cents: int) -> dict:
    """Charge a customer and return the Stripe charge object."""
    # No idempotency_key — each call is a brand-new charge.
    charge = stripe.Charge.create(
        amount=amount_cents,
        currency="usd",
        customer=customer_id,
        description="Order checkout",
    )
    return {"id": charge.id, "status": charge.status}


def run_charge_tool(customer_id: str, amount_cents: int) -> dict:
    """Agent tool wrapper that retries up to 3 times on transient errors."""
    last_err = None
    for attempt in range(3):
        try:
            return charge_customer(customer_id, amount_cents)
        except stripe.error.APIConnectionError as e:
            # Retry re-charges the customer — the first attempt may have succeeded.
            last_err = e
            time.sleep(2**attempt)
    raise last_err
