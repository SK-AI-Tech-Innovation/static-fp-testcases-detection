# ACE-EXPECT: detect
# CATEGORY: should_detect/god_agent_single_responsibility
# LANGUAGE: python
# ISSUE: A single function clones a repo, parses files, calls the LLM to analyze, formats a report, and sends a notification all in one body
# EXPECTED-FINDING: review_repo mixes I/O (git clone), parsing, LLM analysis, formatting, and notification side-effects in one monolithic function with no separation of concerns
# EXPECTED-FIX: Decompose into focused units (clone_repo, parse_sources, analyze_with_llm, render_report, notify) composed by a thin orchestrator, so each concern is independently testable and reusable
# SEVERITY-HINT: warning
"""A single 'agent' function that does cloning, parsing, analysis, formatting, and notification."""

import os
import subprocess

import requests
from openai import OpenAI

client = OpenAI()


def review_repo(repo_url: str, slack_webhook: str) -> None:
    # Concern 1: clone
    workdir = "/tmp/checkout"
    subprocess.run(["git", "clone", repo_url, workdir], check=True)

    # Concern 2: parse / collect source
    sources = []
    for root, _dirs, files in os.walk(workdir):
        for name in files:
            if name.endswith(".py"):
                with open(os.path.join(root, name)) as fh:
                    sources.append(fh.read())
    blob = "\n\n".join(sources)

    # Concern 3: LLM analysis
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Review this code and list issues."},
            {"role": "user", "content": blob[:50000]},
        ],
    )
    analysis = resp.choices[0].message.content

    # Concern 4: format a report
    report = f"# Review for {repo_url}\n\n{analysis}\n\n(files scanned: {len(sources)})"

    # Concern 5: notify
    requests.post(slack_webhook, json={"text": report})

    # Concern 6: cleanup
    subprocess.run(["rm", "-rf", workdir], check=True)


if __name__ == "__main__":
    review_repo("https://github.com/example/repo.git", "https://hooks.slack.com/x")
