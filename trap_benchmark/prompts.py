# ACE-EXPECT: detect
# CATEGORY: trap_benchmark
# LANGUAGE: python
# SOURCE: ace trap/ benchmark fixture (copy; answer key = _ANSWER_KEY_trap_metadata.yaml)
# ISSUE: 9 planted violations: build_analysis_prompt()에서 CODE_REVIEW_PROMPT.format(code=cod | CODE_REVIEW_PROMPT 내 'Code:' 구분자가 {code} 블록과 충돌 가능 | build_analysis_prompt()가 base + CODE_REVIEW_PROMPT를 단순 연결, 토 | SYSTEM_PROMPT='You are a helpful assistant.' — 역할/제약/출력형식/컨텍 | build_instruction_suffix()가 코드 컨텍스트 
# EXPECTED-FINDING: detect the planted anti-patterns above
# EXPECTED-FIX: recommend the corresponding best-practice fixes
# SEVERITY-HINT: mixed
"""Prompt templates for the repository analysis pipeline."""


SYSTEM_PROMPT = "You are a helpful assistant."


CODE_REVIEW_PROMPT = """Analyze the following code and provide:
1. Architecture quality assessment
2. Security vulnerabilities found
3. Performance issues identified
4. Recommended improvements

Code:
{code}
"""


def build_analysis_prompt(code: str, repo_name: str) -> str:
    """Build the final prompt for code analysis."""
    base = f"Repository: {repo_name}\n\n"
    base += f"Code to analyze:\n{code}\n\n"
    base += CODE_REVIEW_PROMPT.format(code=code)
    return base


def build_summary_prompt(results: list) -> str:
    """Build a summary prompt from analysis results."""
    text = "Summarize the following analysis results:\n\n"
    for i, r in enumerate(results):
        text += f"Result {i + 1}: {r}\n"
    return text


def build_search_prompt(query: str) -> str:
    """Build search query prompt."""
    return f"Search for: {query}\nReturn relevant code snippets."


CONTRADICTORY_REVIEW_PROMPT = """Analyze this code carefully.
Be extremely concise — output only one line.
Include ALL details, every function, every variable, every edge case.
"""


def build_instruction_suffix(code: str) -> str:
    """Build a combined prompt with instructions placed after context."""
    context = f"Code to review:\n{code}\n\n"
    instructions = (
        "Instructions:\n"
        "1. Identify all issues\n"
        "2. Rate severity\n"
        "3. Suggest fixes\n"
    )
    return context + instructions
