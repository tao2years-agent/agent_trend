from pathlib import Path
import concurrent.futures,subprocess,json,tempfile,os
R=Path(__file__).resolve().parent
repos={'early':'METR/Measuring-Early-2025-AI-on-Exp-OSS-Devs','late':'METR/Measuring-Late-2025-AI-on-OSS-Devs'}
def fetch(item):
 k,n=item
 with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as t:
  def git(*args):
   return subprocess.check_output(['git','-C',t,'-c','http.proxy=','-c','http.version=HTTP/1.1',*args],stderr=subprocess.DEVNULL)
  git('init','--bare');git('fetch','--depth=1','--filter=blob:none','https://github.com/'+n+'.git','HEAD');h=git('rev-parse','FETCH_HEAD').decode().strip()
  ls=git('ls-tree','-r','--name-only',h).decode().splitlines();return k,dict(repo=n,sha=h,files=ls,date=git('show','-s','--format=%cI',h).decode().strip())
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(2) as e:data=dict(e.map(fetch,repos.items()))
 (R/'repository-locks.json').write_text(json.dumps(data,indent=2),encoding='utf8')
 for k,i in data.items():print(k,i['sha'],i['date'],i['files'][:120])
