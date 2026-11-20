"""External properties fixed before scoring. The expected side never reads the candidate."""
import functools,itertools,json,math,operator,os,sys
from pathlib import Path
sys.path.insert(0,os.getcwd())
out=[]
def check(name,inputs,expected,fn):
    try:
        actual=fn()
        ok=(actual==expected)
        reason=None
    except Exception as e:
        actual=None;ok=False;reason=type(e).__name__+": "+str(e)[:120]
    out.append({"id":name,"input":inputs,"expected":repr(expected),"actual":repr(actual),"error":reason,"ok":bool(ok)})
def precedence():
    from sympy import symbols,lambdify,Mod
    x,y=symbols("x y")
    tests=[("negative_remainder",-(Mod(x,y)),lambda x,y:-(x%y)),("negative_dividend",Mod(-x,y),lambda x,y:(-x)%y),("offset",-Mod(x,y)+x*y,lambda x,y:-(x%y)+x*y),("power",-x**2,lambda x,y:-(x**2)),("negated_remainder_power",(-Mod(x,y))**3,lambda x,y:(-(x%y))**3)]
    for k,expr,expect in tests:
        for a,b in itertools.product((-7,-2,0,1,8),(-5,-2,2,5)):
            check(f"{k}:{a},{b}",[a,b],expect(a,b),lambda:lambdify((x,y),expr,"math")(a,b))
def string():
    from sympy.codegen.ast import String
    for i,s in enumerate(("a","0","","α","x+y","a b")):
        def f():
            a=String(s);return a.func(*a.args)==a and a==String(s) and a!=String(s+"!")
        check(f"identity:{i}",s,True,f)
def point():
    from sympy import I,Rational,Point
    from sympy.core.parameters import evaluate
    for a,b in itertools.product((-2,0,3),(-2,-1,0,1,2)):
        z=Rational(a,2)+I*Rational(b,3)
        for which in (0,1):
            inp=(z,1) if which==0 else (1,z)
            def f():
                try:Point(*inp);return "accept"
                except ValueError:return "reject"
            check(f"coordinate:{a},{b},{which}",{"real":f"{a}/2","imag":f"{b}/3","axis":which},"accept" if b==0 else "reject",f)
    for a in (-3,0,1,5):
        x=Rational(a,2)
        def f():
            with evaluate(False):Point(x,2)
            return "accept"
        check(f"unevaluated_real:{a}",[f"{a}/2",2],"accept",f)
def minmax():
    from sympy import symbols,Min,Max
    from sympy.printing.pycode import PythonCodePrinter
    xs=symbols("a b c d")
    for size in (2,3,4):
        for k,fn,builtin in (("min",Min,min),("max",Max,max)):
            for i,vals in enumerate(itertools.product((-2,0,2),repeat=size)):
                def evaluate():
                    expr=fn(*xs[:size]);printed=PythonCodePrinter().doprint(expr)
                    # Only in-process generated arithmetic on the four fixed symbols.
                    return eval(printed,{"__builtins__":{},"min":min,"max":max},dict(zip("abcd",vals)))
                check(f"{k}{size}:{i}",list(vals),builtin(vals),evaluate)
def containers():
    from sympy import lambdify
    cases=[(),(1,),(-1,2),[],[0],[(1,)],((),),(1,(2,)),[[],(1,),(-1,2)],((1,2),(3,)),((),[1])]
    for j,value in enumerate(cases):
        check("container:"+str(j),repr(value),value,lambda:lambdify([],value,modules="math")())
def bezout(c,d):
    if d==0:return abs(c),1 if c>0 else -1,0
    g,u,v=bezout(d,c%d);return g,v,u-(c//d)*v
def hnf():
    from sympy import Matrix
    from sympy.matrices.normalforms import hermite_normal_form
    def actual(A):
        h=hermite_normal_form(Matrix(A));return (h.rows,h.cols,tuple(map(int,list(h))))
    for a,b,c,d in itertools.product(range(-2,3),repeat=4):
        det=a*d-b*c
        if det==0:continue
        g,u,v=bezout(c,d)
        assert g==math.gcd(c,d) and u*c+v*d==g
        h=abs(det)//g;r=(u*a+v*b)%h
        A=[[a,b],[c,d]]
        check(f"hnf:{a},{b},{c},{d}",A,(2,2,(h,r,0,g)),lambda:actual(A))
    for v in itertools.product((-2,0,1),repeat=3):
        last=next((x for x in reversed(v) if x),0)
        result=(3,1,tuple(x*(1 if last>0 else -1) for x in v)) if last else (3,0,())
        check("column:"+str(v),list(v),result,lambda:actual([[x] for x in v]))
def symbols_case():
    from sympy import symbols,Function,Symbol,Dummy
    from sympy.core.function import UndefinedFunction
    def describe(s):
        if isinstance(s,(list,tuple)):return type(s).__name__,tuple(describe(x) for x in s)
        return ("function" if isinstance(s,UndefinedFunction) else "dummy" if isinstance(s,Dummy) else "symbol"),s.__name__ if isinstance(s,UndefinedFunction) else s.name
    for cls,k in ((Function,"function"),(Symbol,"symbol"),(Dummy,"dummy")):
        for typ in (list,tuple):
            value=typ(["x:2","y:2"])
            e=(typ.__name__,tuple(("tuple",tuple((k,n+str(i)) for i in range(2))) for n in ("x","y")))
            check(k+"-"+typ.__name__,repr(value),e,lambda:describe(symbols(value,cls=cls)))
def gamma():
    from sympy import eye
    from sympy.tensor.tensor import tensor_indices
    from sympy.physics.hep.gamma_matrices import GammaMatrix as G,LorentzIndex,kahane_simplify
    indices=tensor_indices("i0:8",LorentzIndex)
    for count in range(5):
        for pos in range(count+1):
            free=[G(x) for x in indices[:count]]
            product=lambda a:functools.reduce(operator.mul,a)
            seq=free[:pos]+[G(indices[-1]),G(-indices[-1])]+free[pos:]
            expect=4*product(free) if free else 4*eye(4)
            check(f"clifford:{count}:{pos}",[count,pos],True,lambda:bool(kahane_simplify(product(seq)).equals(expect)))
if __name__=="__main__":
    import sympy
    assert os.path.normcase(str(Path.cwd())) in os.path.normcase(sympy.__file__)
    f={"22080":precedence,"22456":string,"22714":point,"22914":minmax,"23262":containers,"23413":hnf,"23534":symbols_case,"23824":gamma}[sys.argv[1]]
    f();assert len({x["id"] for x in out})==len(out)
    Path(sys.argv[2]).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf8")
