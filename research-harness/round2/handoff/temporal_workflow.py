from datetime import timedelta
from temporalio import workflow,activity
with workflow.unsafe.imports_passed_through():
    from target import check,publish

@activity.defn
async def external_publish(args:dict)->str:
    return publish(args["spec"],args["msg"])

@workflow.defn
class Handoff:
    def __init__(self):
        self.messages=[]
        self.gate=0

    @workflow.signal
    def approval(self,msg:dict):
        self.messages.append(msg)

    @workflow.query
    def waiting_for(self)->int:
        return self.gate

    @workflow.run
    async def run(self,spec:dict)->str:
        for n in range(1,spec["gates"]+1):
            self.gate=n
            await workflow.wait_condition(lambda: bool(self.messages))
            msg=self.messages.pop(0)
            if not check(msg,n,spec["guarded"]):
                return "held_request"
        self.gate=0
        return await workflow.execute_activity(external_publish,{"spec":spec,"msg":msg},
            start_to_close_timeout=timedelta(seconds=3))
