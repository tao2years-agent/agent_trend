from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


def main() -> None:
    manifest = json.loads((ROOT / "corpus" / "sources.json").read_text(encoding="utf-8"))
    matrix = json.loads((ROOT / "corpus" / "product_matrix.json").read_text(encoding="utf-8"))
    source_ids = {item["id"] for item in manifest["sources"]}
    check(len(source_ids) == len(manifest["sources"]), "duplicate source IDs")
    for product in matrix["products"]:
        for source_id in product["evidence"]:
            check(source_id in source_ids, f"{product['id']} references unknown source {source_id}")
    for source_id in source_ids:
        meta = ROOT / "raw" / source_id / "2026-11-16" / "metadata.json"
        check(meta.exists(), f"missing capture metadata for {source_id}")
    required = [
        ROOT / "wiki" / "index.md",
        ROOT / "outputs" / "ai-agent-collaboration-report.md",
        ROOT / "outputs" / "index.html",
        ROOT / "state" / "checkpoint.md",
        ROOT / "state" / "coverage.md",
    ]
    for path in required:
        check(path.exists() and path.stat().st_size > 200, f"missing or empty {path.relative_to(ROOT)}")
    for md_path in ROOT.rglob("*.md"):
        # raw/ contains immutable, intentionally partial upstream snapshots.
        # Their relative links describe the source site/repository and are not
        # expected to resolve inside this research repository.
        if "raw" in md_path.relative_to(ROOT).parts:
            continue
        text = md_path.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if target.startswith(("http://", "https://", "#")):
                continue
            relative = target.split("#", 1)[0]
            resolved = (md_path.parent / relative).resolve()
            check(resolved.exists(), f"broken link in {md_path.relative_to(ROOT)} -> {target}")
    html_text = (ROOT / "outputs" / "index.html").read_text(encoding="utf-8")
    check("<main id=\"report\">" in html_text, "HTML report main missing")
    check("id=\"nav-search\"" in html_text, "HTML navigation search missing")
    check("跨组织" in html_text and "WorkBuddy" in html_text, "HTML content incomplete")
    if ERRORS:
        print("LINT FAILED")
        for error in ERRORS:
            print(f"- {error}")
        raise SystemExit(1)
    print(f"LINT PASSED: {len(source_ids)} sources, {len(matrix['products'])} products")


if __name__ == "__main__":
    main()
