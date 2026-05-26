"""Build search-index.json for the recovered K0BG.COM site.

Walks site/k0bg.com/*.html, strips banners/scripts/markup, extracts the
visible text and <title>, and writes a compact JSON array of
{slug, title, text} records that search.html consumes client-side.

Usage:
    python scripts/build_search_index.py [--root site/k0bg.com]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from html import unescape
from pathlib import Path

TAG_RE = re.compile(r"<[^>]+>")
SCRIPT_STYLE_RE = re.compile(
    r"<(script|style)\b[^>]*>.*?</\1>", re.DOTALL | re.IGNORECASE
)
BANNER_RE = re.compile(
    r"<!-- KOBG_PROVENANCE_BANNER_START -->.*?<!-- KOBG_PROVENANCE_BANNER_END -->",
    re.DOTALL,
)
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.DOTALL | re.IGNORECASE)
WS_RE = re.compile(r"\s+")

SKIP_FILES = {
    "search.html",
    "_browse.html",
    "about-reconstruction.html",
}


def extract(path: Path) -> dict[str, str] | None:
    raw = path.read_text(encoding="utf-8", errors="replace")
    title_match = TITLE_RE.search(raw)
    title = unescape(title_match.group(1).strip()) if title_match else path.stem
    title = WS_RE.sub(" ", title).strip()

    no_banner = BANNER_RE.sub("", raw)
    no_script = SCRIPT_STYLE_RE.sub("", no_banner)
    no_tags = TAG_RE.sub(" ", no_script)
    text = WS_RE.sub(" ", unescape(no_tags)).strip()

    if not text:
        return None
    return {"slug": path.name, "title": title, "text": text}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        default="site/k0bg.com",
        help="Directory containing recovered HTML (default: site/k0bg.com)",
    )
    parser.add_argument(
        "--out",
        default=None,
        help="Output path (default: <root>/search-index.json)",
    )
    args = parser.parse_args()

    root = Path(args.root)
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 1

    out = Path(args.out) if args.out else root / "search-index.json"

    docs: list[dict[str, str]] = []
    for path in sorted(root.glob("*.html")):
        if path.name in SKIP_FILES:
            continue
        record = extract(path)
        if record is not None:
            docs.append(record)

    out.write_text(json.dumps(docs, ensure_ascii=False), encoding="utf-8")
    total_bytes = sum(len(d["text"]) for d in docs)
    print(
        f"Indexed {len(docs)} documents ({total_bytes:,} chars of text); "
        f"wrote {out} ({out.stat().st_size:,} bytes)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
