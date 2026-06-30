# ACE-EXPECT: detect
# CATEGORY: trap_benchmark
# LANGUAGE: python
# SOURCE: ace trap/ benchmark fixture (copy; answer key = _ANSWER_KEY_trap_metadata.yaml)
# ISSUE: 8 planted violations: extract_imports()가 문자열 파싱으로 import 추출, AST 기반 완전 추출 아님 | TOOL_REGISTRY dict로 도구 직접 호출, ToolNode 분리/조건부 라우팅 없음 | 모든 Tool 함수에 입력 검증 없음, 잘못된 입력에 명확한 에러 반환 없음 | args_schema 없음, Pydantic BaseModel 또는 JSON Schema 미정의 | 모든 Tool 함수에 파라미터 타입 힌트 없음 | 복잡한 파라미터에 중첩 Pydantic 모델 없이 plain 인자 
# EXPECTED-FINDING: detect the planted anti-patterns above
# EXPECTED-FIX: recommend the corresponding best-practice fixes
# SEVERITY-HINT: mixed
"""Tool definitions for the analysis pipeline."""

from trap.client import fetch_search_results, fetch_repo_metadata


def search_repositories(query):
    """Search for repositories matching the query."""
    raw = fetch_search_results(query)
    if raw and "items" in raw:
        return [item["full_name"] for item in raw["items"]]
    return []


def get_repo_info(owner_repo):
    """Get basic information about a repository."""
    data = fetch_repo_metadata(owner_repo)
    return {
        "name": data.get("name"),
        "stars": data.get("stargazers_count"),
        "language": data.get("language"),
    }


def read_file_content(file_path):
    """Read a source file from the local filesystem."""
    with open(file_path) as f:
        return f.read()


def count_lines(content):
    """Count lines of code in the given content."""
    return len(content.strip().split("\n"))


def extract_imports(content):
    """Extract import statements from Python source code."""
    lines = content.split("\n")
    imports = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("import ") or stripped.startswith("from "):
            imports.append(stripped)
    return imports


TOOL_REGISTRY = {
    "search": search_repositories,
    "repo_info": get_repo_info,
    "read_file": read_file_content,
    "count_lines": count_lines,
    "extract_imports": extract_imports,
}
