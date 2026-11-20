"""Freeze the exact wheel-only environment once and reinstall from local files on Windows."""
from pathlib import Path
from importlib import metadata
import csv,hashlib,json,zipfile,sys,tempfile,platform,sqlite3
from email.parser import BytesParser
B=Path(__file__).resolve().parent
def main():
    wheelhouse=Path(sys.argv[1]);out=[]
    for path in sorted(wheelhouse.glob('*.whl')):
        with zipfile.ZipFile(path) as z:
            meta=next(n for n in z.namelist() if n.endswith('.dist-info/METADATA'));m=BytesParser().parsebytes(z.read(meta))
        name=m['Name'];v=m['Version'];installed=metadata.version(name);assert installed==v,(name,installed,v)
        out.append(dict(name=name,version=v,file=path.name,bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    assert any(x['name']=='mlflow' and x['version']=='3.18.0' for x in out)
    (B/'requirements-win-py312.lock').write_text(''.join(f"{x['name']}=={x['version']} --hash=sha256:{x['sha256']}\n" for x in out),'utf8')
    (B/'environment.json').write_text(json.dumps(dict(python=sys.version,platform=platform.system(),architecture=platform.machine(),sqlite=sqlite3.sqlite_version,wheels=out),indent=2),'utf8')
    import mlflow
    base=Path(mlflow.__file__).resolve().parent
    verified=[]
    for pkg_path in ['genai/prompts/__init__.py','prompt/registry_utils.py','tracking/client.py','store/model_registry/abstract_store.py','store/model_registry/sqlalchemy_store.py','entities/model_registry/prompt_version.py']:
        local=B/'raw'/('mlflow__'+pkg_path.replace('/','__')+'.txt');official=(base/pkg_path).read_bytes();raw=local.read_bytes()
        assert raw==official,pkg_path
        verified.append(dict(module='mlflow/'+pkg_path,extracted=local.relative_to(B).as_posix(),installed_sha256=hashlib.sha256(official).hexdigest()))
    (B/'runtime-source-match.json').write_text(json.dumps(verified,indent=2),'utf8')
    print(len(out),'wheel hashes;',sum(x['bytes'] for x in out),'bytes,',len(verified),'implementation files byte-for-byte identical')
if __name__=='__main__':main()
