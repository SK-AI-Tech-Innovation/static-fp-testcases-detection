# ACE-EXPECT: detect
# CATEGORY: should_detect/nonstandard_implementation
# LANGUAGE: python
# ISSUE: The prompt is assembled by hand with repeated += string concatenation and manual newlines, which is error-prone, hard to maintain, and offers no variable validation or reuse
# EXPECTED-FINDING: prompt construction via ad-hoc += string concatenation instead of a templating mechanism
# EXPECTED-FIX: use a prompt template (e.g. LangChain PromptTemplate / ChatPromptTemplate, or at minimum a single parameterized f-string/Jinja template) with named input variables
# SEVERITY-HINT: suggestion
"""Builds a product-description prompt by += concatenation."""

from anthropic import Anthropic

client = Anthropic()


def build_prompt(name: str, features: list[str], tone: str, audience: str) -> str:
    prompt = ""
    prompt += "You are a marketing copywriter.\n"
    prompt += "Write a product description.\n"
    prompt += "Product name: " + name + "\n"
    prompt += "Features:\n"
    for f in features:
        prompt += "- " + f + "\n"
    prompt += "Tone: " + tone + "\n"
    prompt += "Target audience: " + audience + "\n"
    prompt += "Keep it under 80 words.\n"
    return prompt


def describe(name, features, tone, audience):
    resp = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=200,
        messages=[{"role": "user", "content": build_prompt(name, features, tone, audience)}],
    )
    return resp.content[0].text


if __name__ == "__main__":
    print(describe("AcmePhone", ["OLED screen", "5-day battery"], "playful", "students"))
