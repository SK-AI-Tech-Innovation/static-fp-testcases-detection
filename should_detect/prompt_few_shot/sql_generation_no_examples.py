# ACE-EXPECT: detect
# CATEGORY: should_detect/prompt_few_shot
# LANGUAGE: python
# ISSUE: A natural-language-to-SQL prompt provides the schema but zero few-shot query examples
# EXPECTED-FINDING: A complex generation task (NL -> SQL) gives only the schema and no example pairs, so dialect, join style, and output formatting (with/without markdown fences) are inconsistent
# EXPECTED-FIX: Include 2-3 NL-question -> SQL examples in the target dialect to anchor syntax, conventions, and the raw-SQL output format
# SEVERITY-HINT: suggestion
"""Generate PostgreSQL queries from natural language via Anthropic."""

from anthropic import Anthropic

client = Anthropic()

SCHEMA = """
table customers(id int, name text, country text, created_at timestamptz)
table orders(id int, customer_id int, total_cents int, placed_at timestamptz)
"""


def generate_sql(question: str) -> str:
    prompt = (
        "You convert questions into PostgreSQL queries. "
        f"Database schema:\n{SCHEMA}\n"
        "Write a single SQL query that answers the question. Return only SQL.\n\n"
        f"Question: {question}"
    )
    # No example queries, so join/aggregation style and fencing are unanchored.
    resp = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text
