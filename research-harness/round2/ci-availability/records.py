"""Inert decoder for this audited protocol-4 stream. Never imports a serialized name.

No pickle Unpickler or pickle.load is used. The sole ObjectId representation is discarded.
Referenced memo objects survive only through their last GET, precomputed by scan.py.
"""
from scan import *
import mmap
ROOT=object();MARK=object();IGNORED_OID=object();OID_SYMBOL=object()

def records():
    audit=json.loads((BASE/'opcode-audit.json').read_text(encoding='utf8'))
    assert not audit['unrecognized'] and audit['md5']=='348cedd8f2a0a0bee139031ad6240813'
    with (CACHE/'last-get.u32').open('rb') as index, mmap.mmap(index.fileno(),0,access=mmap.ACCESS_READ) as mm:
        end=memoryview(mm).cast('I')
        try:
            with zipfile.ZipFile(ARCHIVE) as z, z.open(MEMBER) as raw, io.BufferedReader(raw,2**20) as buf:
                stack=[];marks=[];memo={};slots=0
                for op,arg,pos in pickletools.genops(buf):
                    n=op.name
                    if n=='MEMOIZE':
                        if end[slots]:memo[slots]=stack[-1]
                        slots+=1
                    elif n in ('SHORT_BINUNICODE','BINUNICODE','SHORT_BINBYTES','BINBYTES','BININT1','BININT2','BININT','BINFLOAT','LONG1','LONG4'):
                        stack.append(arg)
                    elif n=='EMPTY_DICT':stack.append({})
                    elif n=='EMPTY_LIST':stack.append([] if stack else ROOT)
                    elif n=='MARK':marks.append(len(stack));stack.append(MARK)
                    elif n in ('BINGET','LONG_BINGET'):
                        stack.append(memo[arg])
                        if end[arg]==pos:del memo[arg]
                    elif n=='SETITEMS':
                        spot=marks.pop();d=stack[spot-1]
                        assert type(d) is dict
                        d.update(zip(stack[spot+1::2],stack[spot+2::2]))
                        del stack[spot:]
                        if len(stack)==3 and stack[0] is ROOT and stack[1] is MARK:
                            yield stack.pop()
                    elif n=='SETITEM':
                        v=stack.pop();k=stack.pop();stack[-1][k]=v
                    elif n=='APPENDS':
                        spot=marks.pop();dest=stack[spot-1]
                        if dest is ROOT:
                            for d in stack[spot+1:]:yield d
                        else:
                            assert type(dest) is list
                            dest.extend(stack[spot+1:])
                        del stack[spot:]
                    elif n=='APPEND':
                        v=stack.pop()
                        if stack[-1] is ROOT:yield v
                        else:stack[-1].append(v)
                    elif n=='EMPTY_TUPLE':stack.append(())
                    elif n=='STACK_GLOBAL':
                        symbol=stack.pop();module=stack.pop()
                        if (module,symbol)!=('bson.objectid','ObjectId'):raise ValueError('Unrecognized global, stopped')
                        stack.append(OID_SYMBOL)
                    elif n=='NEWOBJ':
                        args=stack.pop();cl=stack.pop()
                        assert args==() and cl is OID_SYMBOL
                        stack.append(IGNORED_OID)
                    elif n=='BUILD':
                        value=stack.pop()
                        assert stack[-1] is IGNORED_OID and type(value) is bytes and len(value)==12
                    elif n in ('NEWFALSE','NEWTRUE','NONE'):stack.append({'NEWFALSE':False,'NEWTRUE':True,'NONE':None}[n])
                    elif n=='PROTO':assert arg==4
                    elif n=='FRAME':pass
                    elif n=='STOP':
                        assert stack==[ROOT] and slots==len(end) and not memo and not marks
                    else:raise ValueError('Unsupported opcode '+n)
        finally:end.release()
