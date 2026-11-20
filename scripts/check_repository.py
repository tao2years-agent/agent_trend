from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "README.md",
    "AGENTS.md",
    "INDEX.md",
    "DEVELOPMENT.md",
    "NOTICE.md",
    "state/checkpoint.md",
    "research-harness/AGENTS.md",
    "research-harness/round2/index.md",
    "research-harness/round2/protocol.md",
    "research-harness/round2/state/checkpoint.md",
    "research-harness/round2/state/coverage.md",
    "org-context/AGENTS.md",
    "org-context/wiki/index.md",
]

INDEX_DOCUMENTS = [
    "README.md",
    "AGENTS.md",
    "INDEX.md",
    "DEVELOPMENT.md",
    "NOTICE.md",
    "state/checkpoint.md",
    "research-harness/README.md",
    "research-harness/AGENTS.md",
    "research-harness/round2/index.md",
    "research-harness/round2/protocol.md",
    "research-harness/round2/state/checkpoint.md",
    "org-context/AGENTS.md",
    "org-context/wiki/index.md",
]

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def local_target(document: Path, href: str) -> Path | None:
    parsed = urlsplit(href.strip())
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    return (document.parent / unquote(parsed.path)).resolve()


def main() -> int:
    errors: list[str] = []

    for relative in REQUIRED:
        path = ROOT / relative
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"missing required entry point: {relative}")

    for relative in INDEX_DOCUMENTS:
        document = ROOT / relative
        if not document.is_file():
            continue
        text = document.read_text(encoding="utf-8")
        for href in LINK_RE.findall(text):
            target = local_target(document, href)
            if target is not None and not target.exists():
                errors.append(f"broken local link: {relative} -> {href}")

    oversized = [
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.parts and path.stat().st_size >= 100 * 1024 * 1024
    ]
    for relative in oversized:
        errors.append(f"file exceeds GitHub's 100 MiB object limit: {relative}")

    if errors:
        print("REPOSITORY CHECK FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "REPOSITORY CHECK PASSED: "
        f"{len(REQUIRED)} entry points, {len(INDEX_DOCUMENTS)} navigation documents"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

