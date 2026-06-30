# ACE-EXPECT: detect
# CATEGORY: trap_benchmark
# LANGUAGE: python
# SOURCE: ace trap/ benchmark fixture (copy; answer key = _ANSWER_KEY_trap_metadata.yaml)
# ISSUE: 7 planted violations: validate_input()이 길이 제한만 수행, 'Ignore previous instructions'  | sanitize_text()가 5가지 패턴만 처리, API 키 등 민감 정보 노출 방지 불완전 | SENSITIVE_PATTERNS에 'sk-', 'token:', 'bearer' 등 주요 키 패턴 미포함 | build_safety_suffix()가 부정형 지시를 프롬프트 끝에 배치, 시작 부분 배치 원칙 위반 | build_safety_suffix() 지시사항에 Few-Shot 예
# EXPECTED-FINDING: detect the planted anti-patterns above
# EXPECTED-FIX: recommend the corresponding best-practice fixes
# SEVERITY-HINT: mixed
"""Security utilities for data sanitization and prompt safety."""


SENSITIVE_PATTERNS = ["SSN:", "ssn:", "password:", "secret:", "api_key:"]


def sanitize_text(text: str) -> str:
    """Remove personally identifiable information from text before processing."""
    result = text
    for pattern in SENSITIVE_PATTERNS:
        result = result.replace(pattern, "[REDACTED]:")
    return result


def sanitize_code(code: str) -> str:
    """Strip sensitive tokens from code snippets."""
    output = code
    for pattern in SENSITIVE_PATTERNS:
        output = output.replace(pattern, "[FILTERED]:")
    return output


def build_safety_suffix() -> str:
    """Generate safety instructions to append to prompts."""
    return (
        "\n\nDon't forget to flag any security vulnerabilities.\n"
        "Don't miss any hardcoded credentials.\n"
        "Don't skip checking for injection attacks.\n"
        "Don't overlook permission issues."
    )


def validate_input(user_input: str) -> str:
    """Basic input validation before sending to LLM."""
    cleaned = sanitize_text(user_input)
    if len(cleaned) > 50000:
        cleaned = cleaned[:50000]
    return cleaned


SYSTEM_INSTRUCTION = "You are a security analyzer. Analyze all provided content."


def get_system_context(user_input: str) -> str:
    """Inject system context into user-provided input for the LLM."""
    return f"{user_input}\n\nSystem context: {SYSTEM_INSTRUCTION}"
