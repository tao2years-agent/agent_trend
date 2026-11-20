"""Recount the release's official fixture and fingerprint the exact panel SQL."""
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def sha(data):
    return hashlib.sha256(data).hexdigest()

def read_index(name):
    rows = json.loads((ROOT / name).read_text(encoding="utf8"))
    for row in rows:
        assert sha((ROOT / row["path"]).read_bytes()) == row["sha256"], row["id"]
    return rows

source = read_index("independent-sources.json")
fixture = read_index("independent-fixture-sources.json")
history = read_index("independent-history-sources.json")

def panel_hash(row):
    dashboard = json.loads((ROOT / row["path"]).read_text(encoding="utf8"))
    panel = next(item for item in dashboard["panels"] if item["id"] == 86)
    return sha(panel["targets"][0]["rawSql"].encode("utf8"))

tags = [f"v1.0.3-beta{i}" for i in range(13, 20)] + ["main"]
hashes = {}
for ref in tags:
    hashes[ref] = {}
    for dialect in ("mysql", "postgresql"):
        key = f"{ref}:grafana/dashboards/{dialect}/dora-details-change-failure-rate.json"
        row = next(row for row in source if row["id"] == key)
        hashes[ref][dialect] = panel_hash(row)
assert all(hashes[ref] == hashes[tags[0]] for ref in tags)
merge = {row["id"]: panel_hash(row) for row in history if row["id"].startswith("merge-")}
assert merge["merge-8890-legacy"] == merge["merge-8870-mysql"] == hashes["main"]["mysql"]
assert merge["merge-8870-postgresql"] == hashes["main"]["postgresql"]
assert hashes["main"]["mysql"] != hashes["main"]["postgresql"]

def official_csv(ending):
    row = next(r for r in fixture if "/connect_incident_to_deployment/" in r["id"] and r["id"].endswith("/"+ending))
    with (ROOT / row["path"]).open(encoding="utf8", newline="") as data:
        return list(csv.DictReader(data))

deploys = official_csv("cicd_deployment_commits_after.csv")
mappings = official_csv("project_mapping.csv")
incidents = official_csv("incidents.csv")
relations = official_csv("project_incident_deployment_relationships.csv")
scopes = {m["row_id"] for m in mappings if m["table"] == "cicd_scopes" and m["project_name"] == "project1"}
incident_ids = {i["id"] for i in incidents}
last = {}
for row in deploys:
    if row["cicd_scope_id"] in scopes and row["result"] == "SUCCESS" and row["environment"] == "PRODUCTION":
        key = row["cicd_deployment_id"]
        ended = datetime.fromisoformat(row["finished_date"])
        last[key] = max(last.get(key, ended), ended)
begin = datetime(2022,9,1,tzinfo=timezone.utc)
end = datetime(2022,10,1,tzinfo=timezone.utc)
counts = {key: len({r["id"] for r in relations if r["deployment_id"] == key and r["id"] in incident_ids})
          for key, ended in sorted(last.items()) if begin <= ended < end}
cases = sum(count > 0 for count in counts.values())
linked = sum(counts.values())
assert (len(counts), cases, linked) == (5, 2, 6)
result = dict(verified_source_records=[len(source),len(fixture),len(history)],hashes=hashes,merge=merge,project="project1",count_per_deployment=counts,affected_deployments=cases,linked_incidents=linked,total_deployments=len(counts),comparison={"mysql_ratio":cases/len(counts),"postgresql_ratio":linked/len(counts)},method="Python relational arithmetic on upstream's test fixture; no Grafana or database engine")
(ROOT / "independent-check.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
print(result["verified_source_records"],counts,result["comparison"])
