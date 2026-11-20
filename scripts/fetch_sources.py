from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-11-16"
MANIFEST = ROOT / "corpus" / "sources.json"


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (compatible; AI-Agent-Collaboration-Research/1.0; evidence capture)"
    })
    summary = []
    for source in manifest["sources"]:
        target = ROOT / "raw" / source["id"] / DATE
        target.mkdir(parents=True, exist_ok=True)
        body_path = target / "page.html"
        meta_path = target / "metadata.json"
        if body_path.exists() and meta_path.exists():
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            summary.append({"id": source["id"], "status": meta.get("status"), "cached": True})
            continue
        captured_at = datetime.now(timezone.utc).isoformat()
        try:
            response = session.get(source["url"], timeout=35, allow_redirects=True)
            content = response.content
            body_path.write_bytes(content)
            meta = {
                "source_id": source["id"],
                "requested_url": source["url"],
                "final_url": response.url,
                "captured_at_utc": captured_at,
                "status": response.status_code,
                "content_type": response.headers.get("content-type"),
                "sha256": hashlib.sha256(content).hexdigest(),
                "bytes": len(content),
            }
        except Exception as exc:
            meta = {
                "source_id": source["id"],
                "requested_url": source["url"],
                "captured_at_utc": captured_at,
                "status": "fetch_error",
                "error": f"{type(exc).__name__}: {exc}",
            }
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        summary.append({"id": source["id"], "status": meta["status"], "cached": False})
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
