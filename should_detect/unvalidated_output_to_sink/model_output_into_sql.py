# ACE-EXPECT: detect
# CATEGORY: should_detect/unvalidated_output_to_sink
# LANGUAGE: python
# ISSUE: LLM-generated text is interpolated directly into a SQL string and executed with no validation or parameterization
# EXPECTED-FINDING: The model's free-text output (a WHERE clause / value) is concatenated into the SQL passed to cursor.execute, so a malformed or wrong model response corrupts or misdirects the query
# EXPECTED-FIX: Have the model emit a constrained structured value (e.g. a validated field name from an allowlist plus a typed parameter), then run a parameterized query (execute(sql, params)) instead of string interpolation
# SEVERITY-HINT: critical
"""LLM output interpolated straight into a SQL query string."""

import sqlite3

from openai import OpenAI

client = OpenAI()
db = sqlite3.connect("shop.db")


def find_products(natural_query: str) -> list:
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Translate the request into a SQL WHERE clause body only.",
            },
            {"role": "user", "content": natural_query},
        ],
    )
    where_clause = resp.choices[0].message.content

    # Model text dropped straight into the query — no validation, no parameters.
    sql = f"SELECT * FROM products WHERE {where_clause}"
    return db.execute(sql).fetchall()


if __name__ == "__main__":
    print(find_products("red shoes under 50 dollars"))
