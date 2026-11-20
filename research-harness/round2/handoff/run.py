"""Run both real engines. Example: python run.py --temporal /path/to/temporal --out /fresh/path"""
import argparse
import asyncio
from datetime import datetime,timezone,timedelta
import json
import os
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from importlib.metadata import version
from temporalio.client import Client
from temporalio.api.enums.v1 import EventType
from target import prepare,advance,payload,audit
from temporal_workflow import Handoff

BASE=Path(__file__).resolve().parent
SCENARIOS=("resume","stale","duplicate","lost")

def make_spec(root,scenario,guarded):
    root.mkdir(parents=True)
    spec={"db":str(root/"target.sqlite"),"checkpoints":str(root/"graph.sqlite"),"guarded":guarded,"scenario":scenario,"gates":2 if scenario=="duplicate" else 1}
    prepare(spec["db"])
    return spec

def graph_case(spec):
    steps=[]
    def invoke(action):
        p=subprocess.Popen([sys.executable,str(BASE/"graph_worker.py"),json.dumps(spec),action,"1"],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        stdout,stderr=p.communicate(timeout=45)
        if p.returncode not in (0,75):
            raise RuntimeError(stderr)
        out=json.loads(stdout) if stdout.strip() else None
        steps.append({"action":action,"pid":p.pid,"code":p.returncode,"state":out})
        return out
    initial=invoke("start")
    assert initial["interrupts"][0]["request"]=="R1"
    if spec["scenario"]=="stale":advance(spec["db"])
    end=invoke("approve")
    if spec["scenario"]=="duplicate":
        assert end["interrupts"][0]["request"]=="R2"
        end=invoke("approve")
    if spec["scenario"]=="lost":
        assert steps[-1]["code"]==75
        end=invoke("recover")
    return {"status":end["status"],"steps":steps,**audit(spec["db"])}

async def wait_until(fn,timeout=35):
    until=time.monotonic()+timeout
    while time.monotonic()<until:
        obj=await fn()
        if obj:return obj
        await asyncio.sleep(.15)
    raise TimeoutError("wait exceeded")

async def temporal_case(client,endpoint,queue,spec):
    root=Path(spec["db"]).parent
    procs=[]
    logs=[]
    trace=[]
    def spawn():
        control=str(root/("worker"+str(len(procs)+1)))
        log=open(control+".log","a",encoding="utf8")
        logs.append(log)
        proc=subprocess.Popen([sys.executable,str(BASE/"temporal_worker.py"),endpoint,queue,control],stdout=log,stderr=subprocess.STDOUT)
        procs.append(proc)
        return proc
    def kill(p):
        p.terminate()
        p.wait(timeout=10)
    async def spin(stage):
        async def match():
            try:
                return await handle.query(Handoff.waiting_for,rpc_timeout=timedelta(seconds=2))==stage
            except Exception:
                return False
        await wait_until(match)
    try:
        first=spawn()
        handle=await client.start_workflow(Handoff.run,spec,id=queue,task_queue=queue)
        await spin(1)
        trace.append({"action":"pending_R1","worker":first.pid})
        kill(first)
        if spec["scenario"]=="stale":advance(spec["db"])
        second=spawn()
        await spin(1)
        trace.append({"action":"recovered_R1","worker":second.pid})
        await handle.signal(Handoff.approval,payload(1))
        if spec["scenario"]=="duplicate":
            await spin(2)
            trace.append({"action":"duplicate_R1_at_R2","worker":second.pid})
            await handle.signal(Handoff.approval,payload(1))
        if spec["scenario"]=="lost":
            async def exited():return second.poll() is not None
            await wait_until(exited)
            assert second.returncode==75
            third=spawn()
            trace.append({"action":"external_commit_then_crash","worker":second.pid,"code":75,"replacement_worker":third.pid})
        status=await asyncio.wait_for(handle.result(),60)
        history=await handle.fetch_history()
        events=[]
        for ev in history.events:
            typ=EventType.Name(ev.event_type).removeprefix("EVENT_TYPE_")
            row={"id":ev.event_id,"type":typ}
            if typ=="ACTIVITY_TASK_STARTED":row["attempt"]=ev.activity_task_started_event_attributes.attempt
            events.append(row)
        return {"status":status,"steps":trace,"history":events,"runtime_worker_pids":[int((root/f"worker{n}.ready").read_text()) for n in range(1,len(procs)+1)],**audit(spec["db"])}
    finally:
        for proc in procs:
            if proc.poll() is None:kill(proc)
        for log in logs:log.close()

def assert_result(name,guarded,row):
    expected_status=("held_stale" if guarded and name=="stale" else "held_request" if guarded and name=="duplicate" else "published")
    count=0 if expected_status!="published" else 2 if name=="lost" and not guarded else 1
    assert row["status"]==expected_status and len(row["effects"])==count,(name,guarded,row)
    if name=="stale" and not guarded:assert row["effects"]==["v2"]
    if name=="lost":assert len({x["pid"] for x in row["invocations"]})==2

async def main(cli,out):
    out.mkdir(parents=True,exist_ok=True)
    work=Path(tempfile.mkdtemp(prefix="handoff-contract-"))
    result_file=out/"observations.json"
    if result_file.exists():raise FileExistsError(result_file)
    os.environ["PYTHONDONTWRITEBYTECODE"]="1"
    os.environ["LANGSMITH_TRACING"]="false"
    data={"started_utc":datetime.now(timezone.utc).isoformat(),"versions":{p:version(p) for p in ("langgraph","langgraph-checkpoint","langgraph-checkpoint-sqlite","temporalio")},"python":sys.version,"temporal":subprocess.check_output([cli,"--version"],text=True).strip(),"runs":[]}
    def persist():
        result_file.write_text(json.dumps(data,indent=2),encoding="utf8")
    with socket.socket() as sock:
        sock.bind(("127.0.0.1",0))
        port=sock.getsockname()[1]
    address=f"127.0.0.1:{port}"
    (out/"server-command.txt").write_text("temporal server start-dev --ip 127.0.0.1 --port <ephemeral> --headless --db-filename <fresh private temp>/server.sqlite\n",encoding="utf8")
    with (out/"server.log").open("w",encoding="utf8") as logfile:
        server=subprocess.Popen([cli,"server","start-dev","--ip","127.0.0.1","--port",str(port),"--headless","--db-filename",str(work/"server.sqlite")],stdout=logfile,stderr=subprocess.STDOUT)
        try:
            async def connect():
                try:return await Client.connect(address)
                except Exception:return None
            client=await wait_until(connect,60)
            async def group(engine):
                for scenario in SCENARIOS:
                    for guarded in (False,True):
                        key=f"{engine}-{scenario}-"+("guarded" if guarded else "bare")
                        spec=make_spec(work/key,scenario,guarded)
                        if engine=="langgraph":obs=await asyncio.to_thread(graph_case,spec)
                        else:obs=await temporal_case(client,address,key,spec)
                        assert_result(scenario,guarded,obs)
                        data["runs"].append({"engine":engine,"scenario":scenario,"guarded":guarded,**obs})
                        persist()
                        print(key,obs["status"],obs["effects"],flush=True)
            await asyncio.gather(group("langgraph"),group("temporal"))
        finally:
            server.terminate()
            server.wait(timeout=12)
    assert len(data["runs"])==16
    data["finished_utc"]=datetime.now(timezone.utc).isoformat()
    persist()

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--temporal",required=True)
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    asyncio.run(main(args.temporal,args.out))
