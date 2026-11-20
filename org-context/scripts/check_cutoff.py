"""Check the historical-task input boundary with synthetic Git data only."""
import io,json,subprocess,tarfile,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run(cwd,*args):
    return subprocess.check_output(["git","-C",str(cwd),*args],stderr=subprocess.DEVNULL)
with tempfile.TemporaryDirectory() as td:
    repo=Path(td)
    run(repo,"init","-q")
    def commit(text):
        (repo/"rule.txt").write_text(text,encoding="utf8")
        run(repo,"add","rule.txt")
        run(repo,"-c","user.name=Fixture","-c","user.email=fixture@example.invalid","-c","commit.gpgsign=false","commit","-qm","fixture")
        return run(repo,"rev-parse","HEAD").decode().strip()
    old=commit("Use compatibility check A")
    new=commit("New answer ONLY_IN_LATER_COMMIT")
    run(repo,"checkout","-q","--detach",old)
    still_readable=b"ONLY_IN_LATER_COMMIT" in run(repo,"show",new+":rule.txt")
    data=run(repo,"archive","--format=tar",old)
    with tarfile.open(fileobj=io.BytesIO(data)) as tf:
        members=tf.getnames()
        only_old=members==["rule.txt"] and tf.extractfile("rule.txt").read()==b"Use compatibility check A"
    assert still_readable and only_old
    out={"fixture":"two local synthetic commits","git":run(repo,"--version").decode().strip(),"detached_old_checkout_can_read_later_blob_by_oid":still_readable,"archive_members":members,"old_archive_has_only_old_contents":only_old,"scope":"Git fixture only; no agent call, connector or enterprise user"}
    dest=ROOT/"state"/"git-replay.json"
    dest.parent.mkdir(exist_ok=True)
    dest.write_text(json.dumps(out,indent=2),encoding="utf8")
    print(out)
