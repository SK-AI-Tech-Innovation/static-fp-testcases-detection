# ACE-EXPECT: detect
# CATEGORY: should_detect/tool_idempotency
# LANGUAGE: python
# ISSUE: A tool POSTs to an external provisioning API with no idempotency key, re-invoked by tenacity retry, so it provisions duplicate resources
# EXPECTED-FINDING: tenacity re-runs the POST on transient 5xx/timeout; without an Idempotency-Key header the provider creates a second resource each retry
# EXPECTED-FIX: Generate a stable Idempotency-Key (uuid bound to the request) and send it as a header so the provider deduplicates retried POSTs
# SEVERITY-HINT: warning
"""A provision_vm tool for an infra agent, retried via tenacity."""

import requests
from tenacity import retry, stop_after_attempt, wait_exponential

PROVISION_URL = "https://api.cloudprovider.example/v1/instances"


@retry(stop=stop_after_attempt(4), wait=wait_exponential(multiplier=1, max=20))
def provision_vm(region: str, size: str, token: str) -> dict:
    """Create a VM instance and return its descriptor."""
    # POST has no Idempotency-Key header — each retry provisions a new instance.
    resp = requests.post(
        PROVISION_URL,
        json={"region": region, "size": size},
        headers={"Authorization": f"Bearer {token}"},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()


def provision_vm_tool(region: str, size: str, token: str) -> dict:
    """Entry point registered as an agent tool; relies on the retried POST above."""
    instance = provision_vm(region, size, token)
    return {"instance_id": instance["id"], "ip": instance["public_ip"]}
