"""Separate native address/retry identity controls, independent of the application binder."""
import asyncio
import argparse
import json
from pathlib import Path
import socket
import tempfile
import subprocess
import sys
from datetime import timedelta
from uuid import uuid4
from temporalio.client import Client
from temporalio.api.workflowservice.v1 import SignalWorkflowExecutionRequest
from temporalio.api.common.v1 import WorkflowExecution,Payloads
from temporalio.api.enums.v1 import EventType
from run import make_spec,wait_until,BASE
from target import payload,audit
from temporal_workflow import Handoff

def graph(root):
    s=make_spec(root,"duplicate",False)
    def invoke(action,gate,identifier=None):
        cmd=[sys.executable,str(BASE/"graph_worker.py"),json.dumps(s),action,str(gate)]
        if identifier:cmd.append(identifier)
        p=subprocess.run(cmd,capture_output=True,text=True,timeout=40)
        if p.returncode: return {"code":p.returncode,"error":p.stderr.strip().splitlines()[-1]}
        return json.loads(p.stdout)
    first=invoke("start",1); id1=first["interrupt_ids"][0]
    second=invoke("approve",1,id1); id2=second["interrupt_ids"][0]
    repeated=invoke("approve",1,id1)
    before=audit(s["db"])
    valid=invoke("approve",2,id2) if not before["effects"] else None
    return {"R1":id1,"R2":id2,"duplicate_old_interrupt":repeated,"before_valid_R2":before,"after_valid_R2":valid,"target":audit(s["db"])}

async def temporal(root,cli):
    spec=make_spec(root,"duplicate",False);queue="native"
    with socket.socket() as sock:
        sock.bind(("127.0.0.1",0));endpoint="127.0.0.1:"+str(sock.getsockname()[1])
    dev=subprocess.Popen([cli,"server","start-dev","--headless","--ip","127.0.0.1","--port",endpoint.split(":")[-1],"--db-filename",str(root/"server.sqlite")],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    runner=None
    try:
        async def connect():
            try:return await Client.connect(endpoint)
            except Exception:return None
        client=await wait_until(connect)
        runner=subprocess.Popen([sys.executable,str(BASE/"temporal_worker.py"),endpoint,queue,str(root/"worker")],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        h=await client.start_workflow(Handoff.run,spec,id=queue,task_queue=queue)
        rid1,rid2=str(uuid4()),str(uuid4())
        async def send(gate,rid):
            req=SignalWorkflowExecutionRequest(namespace=client.namespace,workflow_execution=WorkflowExecution(workflow_id=queue),signal_name="approval",input=Payloads(payloads=await client.data_converter.encode([payload(gate)])),identity="native-retry-control",request_id=rid)
            await client.workflow_service.signal_workflow_execution(req)
        assert await h.query(Handoff.waiting_for)==1
        await send(1,rid1)
        assert await h.query(Handoff.waiting_for)==2
        await send(1,rid1)
        gate=await h.query(Handoff.waiting_for)
        before=audit(spec["db"])
        if not before["effects"]: await send(2,rid2)
        result=await asyncio.wait_for(h.result(),20)
        history=await h.fetch_history()
        events=[e.event_id for e in history.events if EventType.Name(e.event_type)=="EVENT_TYPE_WORKFLOW_EXECUTION_SIGNALED"]
        return {"same_request_id_sent_twice":rid1,"fresh_request_id":rid2,"gate_after_repeat":gate,"before_valid_R2":before,"result":result,"signal_event_ids":events,"target":audit(spec["db"])}
    finally:
        if runner is not None:runner.terminate();runner.wait(10)
        dev.terminate();dev.wait(10)

async def main(cli,out):
    root=Path(tempfile.mkdtemp(prefix="handoff-native-"))
    g,t=await asyncio.gather(asyncio.to_thread(graph,root/"lg"),temporal(root/"tp",cli))
    out.write_text(json.dumps({"langgraph":g,"temporal":t},indent=2),encoding="utf8")
    print(g,t)
if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--temporal",required=True);ap.add_argument("--out",required=True,type=Path);args=ap.parse_args();asyncio.run(main(args.temporal,args.out))
