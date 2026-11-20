"""Enumerate one AST-local production edit at a time on lines changed by the official repair."""
import ast,copy,difflib,hashlib,json,os,re,subprocess,tarfile,tempfile
from collections import defaultdict,Counter
from pathlib import Path
P=Path(__file__).resolve().parent
O=P.parent/"oracles"
CACHE=Path(os.getenv("ORACLE_CACHE",str(Path(tempfile.gettempdir())/"verified-sympy-20261120")))
SEED="sympy-gates-20261120-v1"
def digest(st):return hashlib.sha256(st.encode()).hexdigest()
def read(p):return json.loads(p.read_bytes())
def write(p,j):p.write_text(json.dumps(j,ensure_ascii=False,indent=2),encoding="utf8")
def apply(root,f):
    subprocess.run(["git","apply","--whitespace=nowarn",str(f)],cwd=root,check=True,capture_output=True)
def checkout(case,apply_gold=True):
    commit=case["base_commit"];key=case["instance_id"];base=Path(tempfile.mkdtemp(prefix=key+"-gates-"));archive=CACHE/(commit+".tar.gz")
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==case["archive_sha256"]
    with tarfile.open(archive) as t:t.extractall(base,filter="data")
    root=base/("sympy-"+commit);apply(root,O/"raw"/key/"test_patch.diff")
    if apply_gold:apply(root,O/"raw"/key/"patch.diff")
    return root
def edited(text):
    active=None;line=0;out=defaultdict(set)
    for s in text.splitlines():
        if s.startswith("+++ b/"):active=s[6:];continue
        if s.startswith("@@ "):line=int(re.search(r"\+(\d+)",s)[1]);continue
        if not active:continue
        if s.startswith("+"):out[active].add(line);line+=1
        elif s.startswith(" "):line+=1
    return out
def changes(n):
    if isinstance(n,ast.Attribute):
        attrs={"is_number":["is_real","is_imaginary","is_rational","is_integer"],"is_zero":["is_nonzero","is_positive","is_negative"]}
        for v in attrs.get(n.attr,[]):
            a=copy.deepcopy(n);a.attr=v;yield "assumption",ast.unparse(a)
    if isinstance(n,ast.Constant):
        if type(n.value) is int:
            for v in (n.value-1,n.value+1):yield "integer_neighbour",str(v)
        elif type(n.value) is float:
            for v in (n.value/2,n.value*1.5):yield "float_neighbour",str(v)
        elif type(n.value) is bool:yield "boolean_literal",repr(not n.value)
        elif isinstance(n.value,str):
            replacements={"min":["max"],"max":["min"],"(":["["],",)":[")",",]"],"[":["("],"]":[")"],"-":["+"]}
            for v in replacements.get(n.value,[]):yield "literal_substitution",repr(v)
    if isinstance(n,ast.Compare) and len(n.ops)==1:
        swap={ast.Is:[ast.IsNot,ast.Eq],ast.Eq:[ast.NotEq,ast.Lt,ast.LtE],ast.NotEq:[ast.Eq]}
        for kind in swap.get(type(n.ops[0]),[]):
            a=copy.deepcopy(n);a.ops=[kind()];yield "comparison","("+ast.unparse(a)+")"
    if isinstance(n,ast.BinOp):
        for kind in {ast.Add:[ast.Sub],ast.Sub:[ast.Add],ast.Mult:[ast.Add]}.get(type(n.op),[]):
            a=copy.deepcopy(n);a.op=kind();yield "arithmetic","("+ast.unparse(a)+")"
    if isinstance(n,ast.BoolOp):
        a=copy.deepcopy(n);a.op=ast.Or() if isinstance(n.op,ast.And) else ast.And()
        yield "boolean_connector","("+ast.unparse(a)+")"
        for x in n.values:yield "drop_conjunct","("+ast.unparse(x)+")"
    if isinstance(n,ast.Subscript) and isinstance(n.slice,ast.Slice):
        for field in ("lower","upper"):
            if getattr(n.slice,field) is None:continue
            a=copy.deepcopy(n);setattr(a.slice,field,None);yield "slice_bound",ast.unparse(a)
    if isinstance(n,ast.Call):
        for i,kw in enumerate(n.keywords):
            a=copy.deepcopy(n);del a.keywords[i];yield "drop_keyword",ast.unparse(a)
        if isinstance(n.func,ast.Name) and n.func.id=="range" and len(n.args)==3:
            a=copy.deepcopy(n);a.args=a.args[:-1];yield "range_step",ast.unparse(a)
        if isinstance(n.func,ast.Name) and n.func.id=="any":
            a=copy.deepcopy(n);a.func.id="all";yield "quantifier",ast.unparse(a)
    if isinstance(n,ast.Dict) and not n.keys:
        for t in ("None","()"):yield "empty_return",t
    if isinstance(n,ast.Lambda) and isinstance(n.body,ast.Name) and n.body.id=="self":
        for t in ("self","lambda: None"):yield "identity_return",t
def enumerate_case(case):
    key=case["instance_id"];root=checkout(case);d=O/"raw"/key
    targets=edited((d/"patch.diff").read_text("utf8"))
    allrows=[];bad=[];duplicates=[];fingerprints=set()
    for path,lines in targets.items():
        assert "/tests/" not in path and path.endswith(".py")
        orig=(root/path).read_text("utf8");source=orig.splitlines(keepends=True);tree=ast.parse(orig)
        original_ast=ast.dump(tree,include_attributes=False)
        for n in ast.walk(tree):
            l=getattr(n,"lineno",0)
            if l not in lines:continue
            if isinstance(n,ast.ClassDef) and any(isinstance(x,ast.Name) and x.id=="Atom" for x in n.bases):
                position=source[l-1].index("Atom, ");options=[("drop_base",position,position+6,"")]
            elif n.end_lineno==l:
                options=[(op,n.col_offset,n.end_col_offset,v) for op,v in changes(n)]
            else:continue
            for op,start,end,after in options:
                line=source[l-1];before=line.encode()[start:end].decode()
                changed_line=(line.encode()[:start]+after.encode()+line.encode()[end:]).decode()
                changed="".join(source[:l-1]+[changed_line]+source[l:])
                token=digest(f"{key}|{path}|{l}:{start}|{op}|{after}")[:12]
                r={"id":"V"+token,"case":key,"path":path,"line":l,"column":start,"operator":op,"before":before,"after":after,"changed_line":changed_line.rstrip(),"original_line":line.rstrip()}
                try:compile(changed,path,"exec");ast_hash=digest(ast.dump(ast.parse(changed),include_attributes=False))
                except (SyntaxError,ValueError) as e:bad.append(r|{"exclude":type(e).__name__});continue
                r["ast_sha256"]=ast_hash
                if ast_hash==digest(original_ast) or (path,ast_hash) in fingerprints:duplicates.append(r|{"exclude":"same_AST"});continue
                fingerprints.add((path,ast_hash))
                diff="".join(difflib.unified_diff(source,changed.splitlines(keepends=True),"a/"+path,"b/"+path))
                r["diff_sha256"]=digest(diff);r["diff"]=diff;allrows.append(r)
    groups=defaultdict(list)
    for r in allrows:groups[r["operator"]].append(r)
    for v in groups.values():v.sort(key=lambda z:digest(SEED+z["id"]))
    selection=[]
    import itertools
    for step in itertools.zip_longest(*(groups[k] for k in sorted(groups,key=lambda o:digest(SEED+o)))):
        selection.extend(x["id"] for x in step if x)
    choose=set(selection[:10])
    for r in allrows:
        r["selected"]=r["id"] in choose
        diff=r.pop("diff")
        if r["selected"]:
            f=P/"patches"/key/(r["id"]+".diff");f.parent.mkdir(exist_ok=True,parents=True);f.write_bytes(diff.encode())
    return {"case":key,"gold_added_lines":{k:sorted(v) for k,v in targets.items()},"changes":allrows,"noncompiling":bad,"duplicates":duplicates}
if __name__=="__main__":
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(2) as ex:cases=list(ex.map(enumerate_case,read(O/"cohort.json")["selected"]))
    write(P/"candidates.json",cases);print([(c["case"],len(c["changes"]),sum(v["selected"] for v in c["changes"])) for c in cases])
