"""Offline BM25 lookups for conference papers; rebuildable from content-addressed raw records."""
import argparse,hashlib,json,sqlite3,tempfile
from contextlib import closing
from collections import Counter
from pathlib import Path
R=Path(__file__).resolve().parent
DB=R/'papers.sqlite'
def build():
    rows=[json.loads(x) for x in (R/'abstracts.jsonl').read_text('utf8').splitlines() if x.strip()]
    assert len(rows)==len({r['id'] for r in rows})==1738
    valid=[r for r in rows if r['abstract'] and r.get('sha256')]
    for r in valid:
        assert hashlib.sha256((R/r['path']).read_bytes()).hexdigest()==r['sha256'],r['id']
    tmp=DB.with_suffix('.tmp')
    if tmp.exists():tmp.unlink()
    with closing(sqlite3.connect(tmp)) as db, db:
        db.execute("CREATE VIRTUAL TABLE papers USING fts5(title, abstract, venue UNINDEXED, uuid UNINDEXED, url UNINDEXED, tokenize='unicode61')")
        db.executemany("INSERT INTO papers VALUES(?,?,?,?,?)",[(r['title'],r['abstract'],r['venue'],r['id'],r['url']) for r in valid])
        db.execute("INSERT INTO papers(papers) VALUES('optimize')")
        assert db.execute("select count(*) from papers").fetchone()[0]==len(valid)
    tmp.replace(DB)
    print(json.dumps(dict(frame=len(rows),indexed=len(valid),by_venue=Counter(r['venue'] for r in valid)),indent=2))
def query(text,venue,n):
    if not DB.exists():raise SystemExit('Build the local index with --build first.')
    with sqlite3.connect('file:'+DB.as_posix()+'?mode=ro',uri=True) as db:
        return list(db.execute("SELECT title,venue,uuid,url FROM papers WHERE papers MATCH ? AND (?='' OR venue=?) ORDER BY bm25(papers,2,1) LIMIT ?",(text,venue,venue,n)))
if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('text',nargs='?');ap.add_argument('--build',action='store_true');ap.add_argument('--venue',default='');ap.add_argument('--limit',type=int,default=8);a=ap.parse_args()
    if a.build:build()
    if a.text:
        for r in query(a.text,a.venue,a.limit):print('\t'.join(r))

