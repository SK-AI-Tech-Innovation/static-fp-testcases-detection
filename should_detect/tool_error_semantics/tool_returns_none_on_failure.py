# ACE-EXPECT: detect
# CATEGORY: should_detect/tool_error_semantics
# LANGUAGE: python
# ISSUE: A search tool returns None on failure with no error signal, so the LLM cannot tell "no results" from "the tool broke"
# EXPECTED-FINDING: On a DB miss or query error the tool returns None; the model sees an empty/null result with no error_code or suggestion and may hallucinate an answer
# EXPECTED-FIX: Return a structured result that distinguishes success/empty/error, e.g. {"status": "error", "error_code": "DB_TIMEOUT", "recoverable": True, "suggestion": ...}
# SEVERITY-HINT: warning
"""A knowledge-base search tool for a RAG agent."""

import sqlite3
from typing import Optional


def search_kb(query: str, db_path: str = "kb.sqlite") -> Optional[list[str]]:
    """Search the knowledge base and return matching passages, or None."""
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.execute(
            "SELECT passage FROM docs WHERE passage LIKE ?", (f"%{query}%",)
        )
        rows = cur.fetchall()
    except sqlite3.Error:
        # Swallows the error and returns None — indistinguishable from "no match".
        return None
    finally:
        try:
            conn.close()
        except Exception:
            return None
    if not rows:
        return None
    return [r[0] for r in rows]


def tool_search(query: str) -> Optional[list[str]]:
    """Entry point registered as an agent tool."""
    return search_kb(query)
