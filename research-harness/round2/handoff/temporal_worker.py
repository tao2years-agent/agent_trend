import sys,asyncio,os
from pathlib import Path
from temporalio.client import Client
from temporalio.worker import Worker
from temporal_workflow import Handoff,external_publish

async def main(endpoint,queue,control):
    client=await Client.connect(endpoint)
    async with Worker(client,task_queue=queue,workflows=[Handoff],activities=[external_publish]):
        Path(control+".ready").write_text(str(os.getpid()))
        while not Path(control+".stop").exists():
            await asyncio.sleep(.05)

if __name__=="__main__":
    asyncio.run(main(*sys.argv[1:]))
