import json
import sys
from typing_extensions import TypedDict
from langgraph.graph import StateGraph,START,END
from langgraph.types import interrupt,Command
from langgraph.checkpoint.sqlite import SqliteSaver
from target import check,publish,payload

class State(TypedDict,total=False):
    spec:dict
    gate:int
    status:str
    last:dict

def approval(s):
    n=s["gate"]
    msg=interrupt({"request":"R"+str(n),"approved_digest":payload(n)["target"]})
    if not check(msg,n,s["spec"]["guarded"]):
        return {"status":"held_request"}
    return {"last":msg,"gate":n+1,"status":"ready" if n==s["spec"]["gates"] else "waiting"}

def apply(s):
    return {"status":publish(s["spec"],s["last"])}

def run(spec,action,gate,interrupt_id=None):
    g=StateGraph(State)
    g.add_node("approval",approval)
    g.add_node("publish",apply)
    g.add_edge(START,"approval")
    g.add_conditional_edges("approval",lambda s: {"held_request":END,"ready":"publish","waiting":"approval"}[s["status"]])
    g.add_edge("publish",END)
    with SqliteSaver.from_conn_string(spec["checkpoints"]) as ck:
        app=g.compile(checkpointer=ck)
        config={"configurable":{"thread_id":"single-request"}}
        if action=="start":
            cmd={"spec":spec,"gate":1,"status":"waiting"}
        elif action=="recover":
            cmd=None
        else:
            cmd=Command(resume={interrupt_id:payload(gate)} if interrupt_id else payload(gate))
        out=app.invoke(cmd,config,durability="sync")
        state=app.get_state(config)
        return {"status":out["status"],"next":list(state.next),"interrupts":[v.value for v in out.get("__interrupt__",[])],"interrupt_ids":[v.id for v in out.get("__interrupt__",[])]}

if __name__=="__main__":
    print(json.dumps(run(json.loads(sys.argv[1]),sys.argv[2],int(sys.argv[3]),sys.argv[4] if len(sys.argv)>4 else None)))
