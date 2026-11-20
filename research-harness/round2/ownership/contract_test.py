"""Miniature time-order and budget cases; identifiers are made up."""
from study import DAY,C0,predict,truth
base=[(C0-3*DAY,1,10,1,71),(C0-2*DAY,2,11,1,71)]
same=(C0,3,80,1,82)
tests=[(C0,100,1),(C0+1,101,1),(C0+2,102,1),(C0+3,103,1),(C0+DAY,104,1)]
later=(C0+2*DAY,4,100,1,999)
f,b=predict(tests,base+[same,later],"frozen")
r,_=predict(tests,base+[same,later],"rolling")
assert all(v[1][0]==(71,) for v in f)
assert r[0][1][1]==(71,) and r[1][1][1][0]==82
assert [x[1][4] for x in r]==[(71,),(71,),(71,),(),(71,)]
assert predict(tests,base+[same],"rolling")[0]==r
labels,_=truth(tests,base+[same,later]);assert set(labels)=={100}
print("Same-time event excluded, subsequent event permitted, future label isolated; unlabeled requests consume daily slots and next-day budget resets.")
