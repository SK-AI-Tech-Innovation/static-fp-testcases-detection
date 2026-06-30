# ACE-EXPECT: detect
# CATEGORY: should_detect/lang_checkpoint_persistence
# LANGUAGE: python
# ISSUE: Multi-turn chat graph keeps history only in process memory, lost on restart
# EXPECTED-FINDING: Conversation state lives in a plain in-process dict with no checkpointer/thread_id, so a restart wipes history
# EXPECTED-FIX: Persist turns via a LangGraph checkpointer keyed by thread_id so conversations survive restarts
# SEVERITY-HINT: warning
"""A chat endpoint storing message history in a module-level dict instead of a durable checkpointer."""

from typing import TypedDict

from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

llm = ChatOpenAI(model="gpt-4o")


class ChatState(TypedDict):
    history: list[str]
    user: str
    reply: str


def respond(s: ChatState) -> dict:
    convo = "\n".join(s["history"]) + f"\nUser: {s['user']}"
    reply = llm.invoke(convo).content
    return {"reply": reply, "history": s["history"] + [f"User: {s['user']}", f"Bot: {reply}"]}


_graph = StateGraph(ChatState)
_graph.add_node("respond", respond)
_graph.add_edge(START, "respond")
_graph.add_edge("respond", END)
chat = _graph.compile()  # no checkpointer

# volatile per-session memory: gone the moment the process restarts
SESSIONS: dict[str, list[str]] = {}


def chat_turn(session_id: str, message: str) -> str:
    history = SESSIONS.get(session_id, [])
    out = chat.invoke({"history": history, "user": message, "reply": ""})
    SESSIONS[session_id] = out["history"]
    return out["reply"]
