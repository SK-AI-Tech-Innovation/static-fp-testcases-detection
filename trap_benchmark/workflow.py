# ACE-EXPECT: detect
# CATEGORY: trap_benchmark
# LANGUAGE: python
# SOURCE: ace trap/ benchmark fixture (copy; answer key = _ANSWER_KEY_trap_metadata.yaml)
# ISSUE: 6 planted violations: StateGraph 없이 순차 함수 호출, 노드 진입/탈출 조건 미정의 | analyze_repository 실패 시 Fallback 없음, 서비스 중단 방지 미구현 | delete_analysis_cache()가 파일 삭제를 HITL 없이 자동 실행 | 중간 상태 저장/체크포인팅 없음, 재개 불가 | Latency, Success Rate 등 성능 메트릭 추적 없음 | PIPELINE_VERSION = '1.0.0' 하드코딩, 변경 이력 추적과 연동 없음
# EXPECTED-FINDING: detect the planted anti-patterns above
# EXPECTED-FIX: recommend the corresponding best-practice fixes
# SEVERITY-HINT: mixed
"""Repository analysis workflow pipeline."""

import os

from trap.state import add_message, add_result, set_repo, get_messages
from trap.analyzer import analyze_repository
from trap.tools import read_file_content, TOOL_REGISTRY
from trap.error_handler import handle_pipeline_error


PIPELINE_VERSION = "1.0.0"


def run_pipeline(repo_url: str, file_paths: list) -> dict:
    """Execute the full analysis pipeline for a repository."""
    set_repo(repo_url)
    add_message("system", f"Starting analysis for {repo_url}")

    file_map = {}
    for path in file_paths:
        try:
            content = read_file_content(path)
            file_map[path] = content
        except Exception as e:
            handle_pipeline_error("file_read", e)

    results = analyze_repository(file_map)
    for r in results:
        add_result(r)

    add_message("system", f"Analysis complete: {len(results)} files processed")
    return {"repo": repo_url, "results": results}


def run_search_step(query: str) -> list:
    """Execute the search step of the pipeline."""
    add_message("user", query)
    search_fn = TOOL_REGISTRY.get("search")
    if search_fn:
        results = search_fn(query)
        add_message("assistant", f"Found {len(results)} results")
        return results
    return []


def run_custom_step(tool_name: str, *args):
    """Run an arbitrary tool by name."""
    tool_fn = TOOL_REGISTRY.get(tool_name)
    if tool_fn is None:
        print(f"Unknown tool: {tool_name}")
        return None

    try:
        result = tool_fn(*args)
        add_message("system", f"Tool {tool_name} completed")
        return result
    except Exception as e:
        handle_pipeline_error(tool_name, e)
        return None


def get_pipeline_history() -> list:
    """Return the full message history for the current pipeline run."""
    return get_messages()


def delete_analysis_cache(repo_url: str) -> None:
    """Remove cached analysis artifacts for a repository."""
    cache_dir = f"/tmp/ace_cache/{repo_url.replace('/', '_')}"
    for fname in os.listdir(cache_dir):
        os.remove(os.path.join(cache_dir, fname))
    os.rmdir(cache_dir)
    add_message("system", f"Cache deleted for {repo_url}")
