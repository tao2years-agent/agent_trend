"""Pass 1 enumerates every opcode with stdlib pickletools. Never calls pickle.load."""
import os, sys, zipfile, pickletools, hashlib, json, time, io
from pathlib import Path
from collections import Counter
from array import array
from datetime import datetime,timezone
BASE=Path(__file__).resolve().parent
ARCHIVE=Path(os.environ.get('RECHECK_ARCHIVE',str(Path(os.environ['TEMP'])/'ase25-rechecks-15559526.zip')))
CACHE=Path(os.environ['TEMP'])/'recheck-feature-availability-15559526'
MEMBER='replication_package_rechecks/recheck_builds_items.pkl'
ALLOWED=set('PROTO FRAME EMPTY_LIST MEMOIZE MARK EMPTY_DICT SHORT_BINUNICODE BINUNICODE SHORT_BINBYTES BINBYTES STACK_GLOBAL EMPTY_TUPLE NEWOBJ BUILD BININT1 BININT2 BININT BINFLOAT LONG1 LONG4 SETITEMS SETITEM APPENDS APPEND BINGET LONG_BINGET NEWTRUE NEWFALSE NONE STOP'.split())
def main():
    CACHE.mkdir(exist_ok=True);ops=Counter();memo=array('I');gets=0;extra=set()
    with ARCHIVE.open('rb') as f:md5=hashlib.file_digest(f,'md5').hexdigest()
    assert md5=='348cedd8f2a0a0bee139031ad6240813',md5
    with zipfile.ZipFile(ARCHIVE) as z:
        info=z.getinfo(MEMBER)
        with z.open(MEMBER) as inp, io.BufferedReader(inp,buffer_size=2**20) as buf:
            for op,arg,pos in pickletools.genops(buf):
                name=op.name;ops[name]+=1
                if name not in ALLOWED:extra.add(name)
                if name=='MEMOIZE':memo.append(0)
                elif name in ('BINGET','LONG_BINGET'):
                    assert arg<len(memo);memo[arg]=pos;gets+=1
    payload=dict(archive_filename=ARCHIVE.name,official_url='https://zenodo.org/records/15559526',md5=md5,member=MEMBER,bytes=info.file_size,zip_crc=hex(info.CRC),memo_entries=len(memo),gets=gets,opcodes=ops,unrecognized=sorted(extra),full_scan_time_utc=datetime.now(timezone.utc).isoformat())
    (BASE/'opcode-audit.json').write_text(json.dumps(payload,indent=2),encoding='utf8')
    print('checked',info.file_size,'bytes;',len(memo),'memo slots;',ops,'extra',extra,flush=True)
    assert not extra,extra
    with (CACHE/'last-get.u32').open('wb') as f:memo.tofile(f)
if __name__=='__main__':main()
