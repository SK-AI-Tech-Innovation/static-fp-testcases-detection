# ACE-EXPECT: detect
# CATEGORY: trap_benchmark
# LANGUAGE: python
# SOURCE: ace trap/ benchmark fixture (copy; answer key = _ANSWER_KEY_trap_metadata.yaml)
# ISSUE: 7 planted violations: create_react_agent에 빈 tools=[], ToolNode 분리/조건부 라우팅 없음 | LLM 응답을 response.json()으로 직접 수신, with_structured_output 없음 | LLM_API_KEY = 'sk-placeholder-key' 하드코딩, 환경 변수 미사용 | sk- 패턴 문자열이 소스에 직접 존재하지만 정적 탐지 로직 없음 | Latency, Success Rate 등 오케스트레이션 메트릭 추적 없음 | create_analysis_agent()가
# EXPECTED-FINDING: detect the planted anti-patterns above
# EXPECTED-FIX: recommend the corresponding best-practice fixes
# SEVERITY-HINT: mixed
"""Pipeline orchestration and LLM integration."""

import requests

from langchain.agents import create_react_agent
from langchain_openai import ChatOpenAI

from trap.workflow import run_pipeline
from trap.client import API_BASE_URL


LLM_MODEL = "gpt-4"
LLM_API_KEY = "sk-placeholder-key"


def create_analysis_agent():
    """Create the main analysis agent."""
    llm = ChatOpenAI(model=LLM_MODEL, api_key=LLM_API_KEY)
    tools = []
    agent = create_react_agent(llm, tools, prompt="Analyze code repositories.")
    return agent


def run_full_analysis(repo_url: str, file_paths: list) -> dict:
    """Orchestrate a complete repository analysis."""
    pipeline_result = run_pipeline(repo_url, file_paths)

    prompt = f"Summarize findings for {repo_url}:\n"
    for r in pipeline_result.get("results", []):
        prompt += f"\n- {r.get('file', 'unknown')}: {len(r.get('issues', []))} issues"

    response = requests.post(
        f"{API_BASE_URL}/chat/completions",
        json={
            "model": LLM_MODEL,
            "messages": [{"role": "user", "content": prompt}],
        },
        headers={"Authorization": f"Bearer {LLM_API_KEY}"},
    )
    summary = response.json()

    return {
        "repo": repo_url,
        "pipeline": pipeline_result,
        "summary": summary,
    }


def generate_report(analysis_result: dict) -> str:
    """Generate a text report from analysis results."""
    repo = analysis_result.get("repo", "unknown")
    results = analysis_result.get("pipeline", {}).get("results", [])
    report = f"Analysis Report: {repo}\n"
    report += f"{'=' * 40}\n"
    for r in results:
        report += f"\nFile: {r.get('file', 'N/A')}\n"
        for issue in r.get("issues", []):
            report += f"  - {issue}\n"
    return report
