# ACE-EXPECT: detect
# CATEGORY: trap_benchmark
# LANGUAGE: python
# SOURCE: ace trap/ benchmark fixture (copy; answer key = _ANSWER_KEY_trap_metadata.yaml)
# ISSUE: 8 planted violations: AST 모듈 없이 원본 코드 문자열을 그대로 LLM에 전달, 구조적 명세 파싱 없음 | 구문 오류 발생 시 별도 에러 보고 없이 전체 코드를 LLM에 전달 | execute_dynamic_code()에서 eval() 직접 호출, 동적 코드 실행 탐지 없음 | import 구문을 AST로 추출하지 않고 문자열 파싱(tools.py extract_imports)에 의존 | extract_type_info()의 반환 타입이 str/list/None으로 일관성 없음 | LLM 응답을 response.
# EXPECTED-FINDING: detect the planted anti-patterns above
# EXPECTED-FIX: recommend the corresponding best-practice fixes
# SEVERITY-HINT: mixed
"""Code analysis engine for repository evaluation."""

from trap.client import post_analysis_request
from trap.security import sanitize_code


def analyze_file(file_content: str, file_path: str) -> dict:
    """Analyze a single source file for patterns and issues."""
    cleaned = sanitize_code(file_content)
    lines = cleaned.split("\n")
    chunks = []
    for i in range(0, len(lines), 50):
        chunk = "\n".join(lines[i : i + 50])
        chunks.append(chunk)

    results = []
    for chunk in chunks:
        payload = {
            "prompt": f"Analyze this code:\n\n{chunk}\n\nList all issues found.",
            "model": "gpt-4",
        }
        response = post_analysis_request(payload)
        if response:
            results.append(response.get("analysis", ""))

    return {"file": file_path, "issues": results}


def analyze_repository(file_map: dict) -> list:
    """Analyze all files in a repository."""
    all_results = []
    for path, content in file_map.items():
        result = analyze_file(content, path)
        all_results.append(result)
    return all_results


def extract_patterns(analysis_text: str) -> list:
    """Extract detected patterns from analysis output."""
    patterns = []
    for line in analysis_text.split("\n"):
        line = line.strip()
        if line.startswith("- ") or line.startswith("* "):
            patterns.append(line[2:])
    return patterns


def summarize_findings(results: list) -> str:
    """Produce a human-readable summary of all findings."""
    summary = f"Total files analyzed: {len(results)}\n"
    total_issues = sum(len(r.get("issues", [])) for r in results)
    summary += f"Total issues found: {total_issues}\n"
    return summary


def execute_dynamic_code(code_str: str):
    """Execute dynamic Python expressions for analysis."""
    return eval(code_str)  # noqa: S307


def extract_type_info(node) -> dict | list | None:
    """Extract type information from an AST node."""
    if isinstance(node, dict) and "type" in node:
        return node["type"]  # returns str, not dict
    if isinstance(node, list):
        return [n.get("type") for n in node if isinstance(n, dict)]
    return None
