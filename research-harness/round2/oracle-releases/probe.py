"""One fresh interpreter for each fixed distribution (wheel imports isolated from local site)."""
import json,sys,warnings
sys.path[:0]=sys.argv[1:3]
import sympy,mpmath
from sympy import lambdify,Point,I
assert sys.argv[1] in sympy.__file__ and sys.argv[2] in mpmath.__file__
def observe(name,f,expected):
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore');v=f()
        got=repr(v);return dict(probe=name,expected=expected,observed=got,ok=got==expected)
    except Exception as err:
        got=type(err).__name__;return dict(probe=name,expected=expected,observed=got,ok=got==expected)
out=[]
for name,v in [('empty',()),('single',(1,)),('two',(1,2)),('nested_empty',((),)),('nested_single',((1,),))]:
    out.append(observe(name,lambda:lambdify([],v,modules='math')(),repr(v)))
for name,v,expected in [('real',(3,4),'(3, 4)'),('mixed',(3+I,4),'ValueError'),('pure',(3,I),'ValueError')]:
    out.append(observe(name,lambda:tuple(Point(*v)),expected))
print(json.dumps(dict(version=sympy.__version__,mpmath=mpmath.__version__,runs=out)))

