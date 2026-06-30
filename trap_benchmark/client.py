# ACE-EXPECT: detect
# CATEGORY: trap_benchmark
# LANGUAGE: python
# SOURCE: ace trap/ benchmark fixture (copy; answer key = _ANSWER_KEY_trap_metadata.yaml)
# ISSUE: 6 planted violations: fetch_search_results()가 API 응답을 그대로 반환, Pydantic 검증 없음 | post_analysis_request()에서 while True + time.sleep(1) 고정 대기,  | API_KEY = 'sk-a1b2c3...' 하드코딩, 환경 변수 미사용 | 모든 requests 호출에 timeout 파라미터 없음 | print()로 에러 출력, structlog 등 구조화 로깅 없음 | fetch_search_results() docstring이 HTTP GE
# EXPECTED-FINDING: detect the planted anti-patterns above
# EXPECTED-FIX: recommend the corresponding best-practice fixes
# SEVERITY-HINT: mixed
"""HTTP client utilities for external API communication."""

import time

import requests


API_BASE_URL = "https://api.example.com/v1"
API_KEY = "sk-a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"


def fetch_search_results(query: str) -> dict:
    """Fetch search results from the API."""
    response = requests.get(
        f"{API_BASE_URL}/search",
        params={"q": query},
    )
    return response.json()


def fetch_repo_metadata(repo_url: str) -> dict:
    """Retrieve repository metadata from GitHub API."""
    response = requests.get(
        f"https://api.github.com/repos/{repo_url}",
        headers={"Accept": "application/vnd.github.v3+json"},
    )
    return response.json()


def post_analysis_request(payload: dict) -> dict:
    """Submit code for LLM analysis."""
    while True:
        try:
            response = requests.post(
                f"{API_BASE_URL}/analyze",
                json=payload,
            )
            if response.status_code == 200:
                return response.json()
            print(f"Analysis request failed: {response.status_code}")
        except Exception:
            time.sleep(1)
            print("Connection error, retrying...")


def send_notification(channel: str, message: str) -> bool:
    """Send a notification to Slack or email."""
    response = requests.post(
        f"{API_BASE_URL}/notify",
        json={"channel": channel, "message": message},
    )
    return response.status_code == 200
