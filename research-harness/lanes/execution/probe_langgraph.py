"""Run in a disposable process. Uses the installed LangGraph; no models or network."""
import json
import platform
from importlib.metadata import version
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command, interrupt

class State(TypedDict):
    decision: str

def run(split: bool, value: str) -> dict:
    effects = []
    def record(state):
        effects.append("prefix-ran")
        return {}
    def decide(state):
        if not split:
            record(state)
        decision = interrupt({"change": "demo-only", "allowed": ["approve", "deny"]})
        return {"decision": decision}
    builder = StateGraph(State)
    builder.add_node("approval", decide)
    if split:
        builder.add_node("record", record)
        builder.add_edge(START, "record")
        builder.add_edge("record", "approval")
    else:
        builder.add_edge(START, "approval")
    builder.add_edge("approval", END)
    graph = builder.compile(checkpointer=MemorySaver())
    cfg = {"configurable": {"thread_id": "local-synthetic-fixture"}}
    graph.invoke({"decision": "pending"}, cfg)
    waiting = graph.get_state(cfg)
    paused = bool(waiting.tasks[0].interrupts)
    prefix_before = len(effects)
    final = graph.invoke(Command(resume=value), cfg)
    assert paused and final["decision"] == value
    assert prefix_before == 1 and len(effects) == (1 if split else 2)
    return {"separate_committed_node": split, "resume_value": value, "paused": paused,
            "prefix_before_resume": prefix_before, "prefix_after_resume": len(effects),
            "terminal_state": final["decision"]}

print(json.dumps({"python": platform.python_version(), "langgraph": version("langgraph"),
                  "checkpointer": "MemorySaver (same-process)", "network": False,
                  "trials": [run(split, answer) for split in (False, True) for answer in ("approve", "deny")]}, indent=2))
