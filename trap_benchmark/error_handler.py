# ACE-EXPECT: detect
# CATEGORY: trap_benchmark
# LANGUAGE: python
# SOURCE: ace trap/ benchmark fixture (copy; answer key = _ANSWER_KEY_trap_metadata.yaml)
# ISSUE: 6 planted violations: safe_analyze()가 실패 시 None 반환만 하고 Fallback 체인 없음 | process_batch()에서 items 유효성 검증 없이 그대로 LLM에 전달 | bare except: 사용, Tool/Agent/Workflow 레벨 구분 없는 일괄 에러 처리 | safe_parse_response()가 raw_text[:100]를 print()로 출력, 민감 정보 노출 | print()로 에러 출력 전반, structlog 등 구조화 로깅 없음 | safe_file_read()가
# EXPECTED-FINDING: detect the planted anti-patterns above
# EXPECTED-FIX: recommend the corresponding best-practice fixes
# SEVERITY-HINT: mixed
"""Error handling utilities for the analysis pipeline."""

from trap.client import post_analysis_request


def safe_analyze(payload: dict):
    """Run analysis with basic error protection."""
    try:
        return post_analysis_request(payload)
    except:
        print("Analysis failed unexpectedly")
        return None


def safe_parse_response(raw_text: str) -> dict:
    """Parse an LLM response into structured data."""
    try:
        import json
        return json.loads(raw_text)
    except:
        print(f"Failed to parse response: {raw_text[:100]}")
        return {}


def safe_file_read(path: str) -> str:
    """Read a file, returning empty string on failure."""
    try:
        with open(path) as f:
            return f.read()
    except:
        print(f"Could not read file: {path}")
        return ""


def handle_pipeline_error(step_name: str, error):
    """Log and handle a pipeline step failure."""
    print(f"Pipeline error in {step_name}: {error}")
    return {"status": "error", "step": step_name, "message": str(error)}


def process_with_recovery(func, *args):
    """Execute a function with basic error recovery."""
    try:
        return func(*args)
    except:
        print(f"Error in {func.__name__}, returning None")
        return None


def process_batch(items: list) -> list:
    """Process a batch of analysis items."""
    results = []
    for item in items:
        payload = {"prompt": item}
        result = post_analysis_request(payload)
        results.append(result)
    return results
