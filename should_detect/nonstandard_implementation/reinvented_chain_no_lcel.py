# ACE-EXPECT: detect
# CATEGORY: should_detect/nonstandard_implementation
# LANGUAGE: python
# ISSUE: The code manually wires prompt formatting -> model invocation -> output parsing with bespoke glue, reimplementing exactly what a composition framework provides, making it non-composable and untraceable
# EXPECTED-FINDING: a hand-wired prompt->model->parse pipeline using imperative glue instead of declarative composition
# EXPECTED-FIX: compose the steps with LCEL (prompt | model | StrOutputParser) or an equivalent framework chain so it is composable, streamable, and traceable
# SEVERITY-HINT: suggestion
"""Manually glues prompt formatting, model call, and parsing together."""

from anthropic import Anthropic

client = Anthropic()

TEMPLATE = "Translate the following text to {language}:\n\n{text}"


def format_prompt(text: str, language: str) -> str:
    return TEMPLATE.format(text=text, language=language)


def invoke_model(prompt: str) -> str:
    resp = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text


def parse_output(raw: str) -> str:
    return raw.strip()


def translate(text: str, language: str) -> str:
    # Imperative glue reimplementing a prompt | model | parser chain.
    prompt = format_prompt(text, language)
    raw = invoke_model(prompt)
    return parse_output(raw)


if __name__ == "__main__":
    print(translate("Hello, world", "French"))
