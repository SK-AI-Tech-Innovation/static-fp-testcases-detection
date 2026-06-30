# ACE-EXPECT: detect
# CATEGORY: should_detect/unvalidated_output_to_sink
# LANGUAGE: python
# ISSUE: LLM output is passed to eval()/exec() to compute a result, executing arbitrary model-produced code with no validation
# EXPECTED-FINDING: The model's reply is evaluated with eval(), so any expression the model emits runs in-process; a malformed or unexpected response causes arbitrary execution or crashes
# EXPECTED-FIX: Request a structured result (e.g. a numeric answer field via structured output) or use a safe, restricted evaluator (ast.literal_eval / a sandboxed math parser) instead of eval/exec on raw model text
# SEVERITY-HINT: critical
"""eval() applied to LLM output to 'compute' an answer."""

from openai import OpenAI

client = OpenAI()


def compute(question: str) -> float:
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Return a single Python expression that computes the answer.",
            },
            {"role": "user", "content": question},
        ],
    )
    expr = resp.choices[0].message.content

    # Arbitrary model-generated code executed in-process.
    return eval(expr)


if __name__ == "__main__":
    print(compute("What is 12% of 250?"))
