"""Independently reopen the stopped fixture database read-only; export only allowlisted technical values."""
import json,hashlib,sqlite3,tempfile,sys
from pathlib import Path
B=Path(__file__).resolve().parent
def main():
    obs=json.loads((B/'observations.json').read_text())
    files=[Path(sys.argv[1])] if len(sys.argv)>1 else list(Path(tempfile.gettempdir()).glob('mlflow-prompt-registry-*/registry.sqlite'))
    db=next(p for p in files if hashlib.sha256(p.read_bytes()).hexdigest()==obs['sqlite_file_sha256'])
    conn=sqlite3.connect(db.as_uri()+'?mode=ro',uri=True)
    sql="select alias,version from registered_model_aliases where name=? order by alias"
    aliases=dict(conn.execute(sql,(obs['name'],)));tags="select version,value from model_version_tags where name=? and key=? order by version"
    templates=dict(conn.execute(tags,(obs['name'],'mlflow.prompt.text')))
    configs={v:json.loads(x) for v,x in conn.execute(tags,(obs['name'],'_mlflow_prompt_model_config'))}
    check=conn.execute('pragma integrity_check').fetchone()[0];violations=conn.execute('pragma foreign_key_check').fetchall();conn.close()
    assert check=='ok' and not violations and aliases=={'candidate':3,'production':1}
    assert len(templates)==len(configs)==3 and configs[2]['temperature']==0.8
    out=dict(sqlite_sha256=obs['sqlite_file_sha256'],bytes=db.stat().st_size,integrity_check=check,foreign_key_violations=len(violations),aliases=aliases,templates=templates,model_config=configs)
    (B/'reopened-sqlite.json').write_text(json.dumps(out,indent=2),'utf8');print(out)
if __name__=='__main__':main()
