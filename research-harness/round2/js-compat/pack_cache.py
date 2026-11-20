"""Bundle exactly the public, integrity-checked archives referenced by successful lockfiles."""
from pathlib import Path
import json,subprocess,shutil,hashlib,base64,zipfile
B=Path(__file__).resolve().parent
def key(integrity):
    a,d=integrity.split('-',1);digest=base64.b64decode(d).hex();assert a=='sha512'
    return f'_cacache/content-v2/{a}/{digest[:2]}/{digest[2:4]}/{digest[4:]}'
def main():
    exe=shutil.which('node');cli=str(Path(exe).parent/'node_modules/npm/bin/npm-cli.js')
    cache=Path(subprocess.check_output([exe,cli,'config','get','cache'],text=True).strip())
    entries={}
    for lock in sorted((B/'locks').glob('*.json')):
        for path,obj in json.loads(lock.read_text())['packages'].items():
            if path:
                assert obj['resolved'].startswith('https://registry.npmjs.org/')
                entries[obj['integrity']]=obj['resolved']
    dest=B/'raw'/'npm-locked-public-archives.zip'
    with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_STORED) as z:
        total=0
        for integ,url in sorted(entries.items()):
            content=(cache/key(integ)).read_bytes();assert base64.b64encode(hashlib.sha512(content).digest()).decode()==integ.split('-',1)[1]
            total+=len(content);header=zipfile.ZipInfo(key(integ),date_time=(1980,1,1,0,0,0));z.writestr(header,content)
    out=dict(archives=len(entries),payload_bytes=total,bundle_sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),entries=entries)
    (B/'locked-archives.json').write_text(json.dumps(out,indent=2,sort_keys=True),'utf8');print(len(entries),total)
if __name__=='__main__':main()
