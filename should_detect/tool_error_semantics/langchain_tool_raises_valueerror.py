# ACE-EXPECT: detect
# CATEGORY: should_detect/tool_error_semantics
# LANGUAGE: python
# ISSUE: A LangChain @tool raises a raw ValueError instead of returning a structured error the LLM can reason about
# EXPECTED-FINDING: When the user is missing the tool throws an uncaught ValueError, aborting the agent run instead of giving the model a recoverable, machine-readable error
# EXPECTED-FIX: Return a structured error object (e.g. {"error_code": "USER_NOT_FOUND", "message": ..., "recoverable": True, "suggestion": ...}) so the LLM can adapt
# SEVERITY-HINT: warning
"""Look up a CRM user record as a LangChain tool for an account-support agent."""

from langchain_core.tools import tool

# Tiny in-memory CRM stand-in.
_USERS = {"u_1001": {"name": "Ada Lovelace", "plan": "pro"}}


@tool
def get_user(user_id: str) -> dict:
    """Fetch a CRM user record by its user_id."""
    record = _USERS.get(user_id)
    if record is None:
        # Raw exception bubbles straight out of the tool and crashes the agent loop.
        raise ValueError(f"No user found for id {user_id!r}")
    if record["plan"] not in {"pro", "enterprise"}:
        raise ValueError("User plan is not eligible for support tooling")
    return record


@tool
def get_user_invoices(user_id: str) -> list[dict]:
    """List recent invoices for a user."""
    # Depends on get_user succeeding; same raw-raise failure mode.
    user = get_user.invoke({"user_id": user_id})
    return [{"id": "inv_1", "user": user["name"], "amount_cents": 4900}]
