from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P/"raw"
repo="https://github.com/jiangnanpro/Reruns-of-GHA-workflow";sha="080aa9edd5f54c4e9dc5675ea75bc0f545c37ff3"
items=[
("huang-published.pdf","https://jiangnanpro.github.io/assets/pdf/3795771.pdf","TOSEM 35(10), article 328, Sections 3.2, 4.2 and Table 3; published version","2026-09-18"),
("huang-published.txt","https://doi.org/10.1145/3795771","pdftotext -layout of the author-hosted published article; Section 3.2 and Table 3",""),
("huang-crossref.json","https://api.crossref.org/works/10.1145/3795771","journal online and issue dates",""),
("huang.pdf","https://binlin.info/downloads/Huang2026a.pdf","coauthor manuscript; superseded here by published version",""),
("huang.txt","https://binlin.info/downloads/Huang2026a.pdf","text of coauthor manuscript",""),
("ge.pdf","https://arxiv.org/pdf/2602.02307v1","Sections 3.1/4.1/5.1/6.1 incl. conditional label and job-level sampling","2026-02-02"),
("ge.txt","https://arxiv.org/pdf/2602.02307v1","pdftotext of Ge and Zhang v1",""),
("site.html","https://flaky-build.github.io/","authors' project site: full dataset on request",""),
("stuck.pdf","https://arxiv.org/pdf/2610.41863v1","Sections III and IV; prior-attempt recovery and streak censoring","2026-10-30"),
("stuck.txt","https://arxiv.org/pdf/2610.41863v1","pdftotext of Bardsiri et al. v1",""),
("official-actions.html","https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs","same GITHUB_SHA and REF on rerun; whole, failed or selected jobs",""),
("gharuns-zenodo.json","https://zenodo.org/api/records/23458821","fixed GHARuns record and publisher file sizes/checksums","2026-10-19"),
("runs.parquet.footer","https://zenodo.org/api/records/23458821/files/runs.parquet/content","unaltered footer for 139 groups and native-attempt field",""),
("jobs.parquet.footer","https://zenodo.org/api/records/23458821/files/jobs.parquet/content","unaltered footer for 222 groups and check_suite_id",""),
("huang-tree.txt",repo+"/tree/"+sha,"git ls-tree filenames and blob oids; full source revision",""),
("huang-notebook.txt",repo+"/blob/"+sha+"/Part_1_Empirical/Step%201%20Collect%20reruns.ipynb","uses previous_attempt_url and reverses collected chain; also catch on missing responses",""),
("huang-collector.py.txt",repo+"/blob/"+sha+"/Part_1_Empirical/collect_data.py","collector saves the entire run document: full raw pickle deliberately not used",""),
("huang-all-pointer.txt",repo+"/blob/"+sha+"/data/all_branch_workflow_runs2023_final.pkl.zip","git LFS pointer only; raw pickle not analyzed",""),
("4open.html","https://anonymous.4open.science/api/repo/Reruns-of-GHA-workflow-F0B1/files","anonymous URL redirects to author public repository",""),
("4page.html","https://anonymous.4open.science/r/Reruns-of-GHA-workflow-F0B1/README.md","independent redirect and public release README",""),
("linkfig.txt","https://figshare.com/s/fb59be9661cb01975555","HTTP 202 empty body from author supplementary link during access; not a data source for conclusions",""),
("suite-id-range-hashes.json","https://zenodo.org/records/23458821","101 extra key-column hashes for complete membership of three registered integer bands","")]
def main():
    rows=[]
    for name,url,purpose,date in items:
        pkg=R/name;rows.append({"url":url,"path":"raw/"+name,"detail":purpose,"date":date,"sha256":hashlib.sha256(pkg.read_bytes()).hexdigest()})
    from huang import files
    for kind,src in files.items():rows.append({"url":repo+"/blob/"+sha+"/data/dataframes/"+src["name"],"detail":kind+" official aggregated sequence dataframe, held in temporary cache; re-fetch and git blob verified by huang.py","date":"","sha256":src["sha256"],"blob_oid":src["blob"]})
    (P/"sources.json").write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding="utf8")
if __name__=="__main__":main()
