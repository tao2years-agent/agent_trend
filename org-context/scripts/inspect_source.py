"""Capture a source file and companion tests at a dated upstream commit."""
from pathlib import Path
import concurrent.futures as cf
import datetime as dt
import hashlib
import json
import re
import subprocess
import urllib.parse

ROOT = Path(__file__).resolve().parents[1]
STAMP = "2026-11-18"
TARGETS = {
    "openai/codex": [r"/project_doc\.rs$", r"/project_doc_tests\.rs$"],
    "google-gemini/gemini-cli": [r"/memoryDiscovery\.ts$", r"/memoryDiscovery\.test\.ts$"],
    "Aider-AI/aider": [r"^aider/repomap\.py$", r"test_repomap\.py$"],
    "nrwl/nx": [r"/affected-project-graph\.ts$", r"/affected-project-graph\.spec\.ts$"],
    "pact-foundation/pact_broker": [r"matrix/.*/?query\.rb$|matrix/query\.rb$", r"matrix/query_spec\.rb$"],
    "backstage/backstage": [r"/BuiltinKindsEntityProcessor\.ts$", r"/BuiltinKindsEntityProcessor\.test\.ts$"],
    "QwenLM/qwen-code": [r"/memoryDiscovery\.ts$", r"/memoryDiscovery\.test\.ts$"],
}

def fetch(url):
    return subprocess.check_output(["curl.exe", "--noproxy", "*", "-fsSL", "--retry", "1", "--max-time", "35", url])

def run(item):
    repo, patterns = item
    dest = ROOT / "raw" / "git" / repo.split("/")[-1] / STAMP
    dest.mkdir(parents=True, exist_ok=True)
    if (dest / "manifest.json").exists():
        return
    base = "https://api.github.com/repos/" + repo
    commit = json.loads(fetch(base + "/commits?per_page=1&until=2026-11-18T15:59:59Z"))[0]
    sha = commit["sha"]
    tree = json.loads(fetch(base + "/git/trees/" + sha + "?recursive=1"))
    rows = []
    for pattern in patterns:
        matches = [n["path"] for n in tree["tree"] if re.search(pattern, n["path"])]
        if not matches:
            print(repo, "missing", pattern, flush=True)
            continue
        path = min(matches, key=len)
        url = f"https://raw.githubusercontent.com/{repo}/{sha}/{urllib.parse.quote(path)}"
        content = fetch(url)
        (dest / Path(path).name).write_bytes(content)
        rows.append({"file": path, "url": f"https://github.com/{repo}/blob/{sha}/{path}", "sha256": hashlib.sha256(content).hexdigest()})
    (dest / "manifest.json").write_text(json.dumps(dict(repo=repo, commit=sha, date=commit["commit"]["committer"]["date"], files=rows), indent=2), encoding="utf8")
    print(repo, len(rows), flush=True)

if __name__ == "__main__":
    with cf.ThreadPoolExecutor(max_workers=7) as pool:
        for future in [pool.submit(run, item) for item in TARGETS.items()]:
            try:
                future.result()
            except Exception as exc:
                print(str(exc), flush=True)
