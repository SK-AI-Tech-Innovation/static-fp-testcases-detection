# ACE-EXPECT: detect
# CATEGORY: trap_benchmark
# LANGUAGE: python
# SOURCE: ace trap/ benchmark fixture (copy; answer key = _ANSWER_KEY_trap_metadata.yaml)
# ISSUE: 6 planted violations: TypedDict/Pydantic 없이 plain dict로 상태 정의 | 필수/선택 필드 구분 없음, 기본값이 dict 리터럴에만 존재 | messages 필드에 Annotated[list, add_messages] 리듀서 없음 | .append()와 직접 키 할당으로 상태 직접 변경(mutation) | 전역 dict로 상태 관리, 노드 간 데이터 흐름 추적 불가 | 단일 전역 pipeline_state, 사용자 간 컨텍스트 격리 없음
# EXPECTED-FINDING: detect the planted anti-patterns above
# EXPECTED-FIX: recommend the corresponding best-practice fixes
# SEVERITY-HINT: mixed
"""Pipeline state management for repository analysis."""


pipeline_state = {
    "messages": [],
    "current_repo": None,
    "analysis_results": [],
    "session_user": None,
    "session_theme": "light",
    "workflow_step": 0,
    "workflow_status": "idle",
    "errors": [],
}


def add_message(role: str, content: str):
    """Append a new message to the conversation history."""
    pipeline_state["messages"].append({"role": role, "content": content})


def set_repo(repo_url: str):
    """Set the current repository being analyzed."""
    pipeline_state["current_repo"] = repo_url
    pipeline_state["workflow_step"] = 0
    pipeline_state["workflow_status"] = "started"


def add_result(result: dict):
    """Store an analysis result."""
    pipeline_state["analysis_results"].append(result)
    pipeline_state["workflow_step"] += 1


def get_messages():
    """Return all messages in history."""
    return pipeline_state["messages"]


def update_session(user: str, theme: str = "light"):
    """Update session-level UI preferences."""
    pipeline_state["session_user"] = user
    pipeline_state["session_theme"] = theme


def reset():
    """Clear all state for a fresh run."""
    pipeline_state["messages"].clear()
    pipeline_state["analysis_results"].clear()
    pipeline_state["current_repo"] = None
    pipeline_state["workflow_step"] = 0
    pipeline_state["workflow_status"] = "idle"
    pipeline_state["errors"].clear()
