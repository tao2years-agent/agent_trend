"""SQL independently expands the arrays published by Huang & Lin and checks the denominators."""
import csv,gzip,sqlite3,json
from ast import literal_eval
from huang import P,files,fetch,write
def main():
    db=sqlite3.connect(":memory:")
    db.executescript("CREATE TABLE occ(kind TEXT,k TEXT,seq TEXT,expected INTEGER,last TEXT);")
    for k in files:
        with gzip.open(fetch(files[k]),"rt",encoding="utf8") as f:
            for row in csv.DictReader(f):
                arrays=[literal_eval(row[x]) for x in ("reruns ids","rerun conclusion","reruns","last rerun's conclusion")]
                db.executemany("INSERT INTO occ VALUES(?,?,?,?,?)",[(k,json.dumps(i),json.dumps(seq),int(n),last) for i,seq,n,last in zip(*arrays)])
    db.executescript("CREATE TABLE u AS SELECT DISTINCT * FROM occ;CREATE UNIQUE INDEX uniq ON u(kind,k);")
    out={}
    for kind in files:
        data=db.execute("""SELECT COUNT(*),SUM(json_array_length(seq)=0),SUM(json_extract(seq,'$[0]')='failure' AND json_extract(seq,'$[1]')='success'),SUM(json_extract(seq,'$[0]')='failure' AND json_extract(seq,'$[1]')='failure'),SUM(json_extract(seq,'$[0]')='failure' AND json_extract(seq,'$[#-1]')='success') FROM u WHERE kind=?""",(kind,)).fetchone()
        out[kind]=dict(zip(["unique_sets","missing_sequences","red_green_next","red_red_next","red_green_last"],data))
    write("sql-check.json",out);print(out)
if __name__=="__main__":main()
