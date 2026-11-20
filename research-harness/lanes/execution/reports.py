import pathlib as P,requests, concurrent.futures as CF, hashlib,json,datetime
HERE=P.Path(__file__).resolve().parent
pairs=[('openhands','https://arxiv.org/abs/2511.03690','SDK 论文摘要与版本历史，区分架构自述和独立评测。'),('sweagent','https://arxiv.org/abs/2405.15793','ACI 论文摘要与版本历史；研究任务是仓库 issue，结果不外推到人力节约。'),('codex','https://openai.com/index/harness-engineering/','2026-02-11 内部单团队经验，优先级、验收和将失败模式回写仓库。'),('codex','https://developers.openai.com/cookbook/examples/agents_sdk/agent_improvement_loop','官方示例把轨迹、人的反馈、模型反馈、回归评测和 harness 变更建议串联。')]
def get(row):
 k,url,detail=row
 for i in range(3):
  try:
   with requests.Session() as s:
    s.trust_env=bool(i%2)
    r=s.get(url,timeout=16);r.raise_for_status();b=r.content
   if b'Just a moment...' in b[:1000]:raise ValueError('challenge')
   break
  except Exception as e:
   if i==2:return k,None,str(e)
 sha=hashlib.sha256(b).hexdigest();p=HERE/'raw'/k/sha[:16]/'report.html';p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():assert p.read_bytes()==b
 else:p.write_bytes(b)
 return k,dict(url=url,download_url=url,path=p.relative_to(HERE.parents[1]).as_posix(),date='',sha256=sha,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),kind='report',detail=detail),None
if __name__=='__main__':
 with CF.ThreadPoolExecutor(4) as ex: rows=list(ex.map(get,pairs))
 path=HERE/'sources.json'; data=json.loads(path.read_text('utf8'))
 for k,item,err in rows:
  print(k,item['url'] if item else err)
  if item and all(i['path']!=item['path'] for i in data[k]):data[k].append(item)
 path.write_text(json.dumps(data,ensure_ascii=False,indent=2),'utf8')
