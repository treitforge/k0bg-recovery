"""Generate gallery2/index.html — a landing page that replaces the
non-archivable Gallery2 PHP photo gallery with links to all per-article
image galleries reconstructed from the September 2022 PDF capture.

Run from repo root:
    python scripts/make_gallery_landing.py

This writes site/k0bg.com/gallery2/index.html based on the existing
_pdf_assets/<slug>/gallery.html aggregations and their manifest.json
metadata. It is safe to re-run; the file is regenerated each time.
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site" / "k0bg.com"
ASSETS = SITE / "_pdf_assets"
OUT = SITE / "gallery2" / "index.html"


SPECIAL_TITLES = {
    "abcs": "The ABCs of Mobile HF",
    "k-bg-com": "K0BG.com (front page)",
    "rfi-problems": "RFI Problems",
    "the-proper-split-beads-to-suppress-rfi": "The Proper Split Beads To Suppress RFI",
}


def pretty_title(slug: str) -> str:
    if slug in SPECIAL_TITLES:
        return SPECIAL_TITLES[slug]
    words = slug.replace("-", " ").split()
    fixed = []
    for w in words:
        lw = w.lower()
        if lw in {"vhf", "rfi", "uhf", "dc", "rf", "hf", "rv", "ev"}:
            fixed.append(lw.upper())
        elif lw == "pl259s":
            fixed.append("PL-259s")
        else:
            fixed.append(w[:1].upper() + w[1:].lower())
    return " ".join(fixed)


def count_images(gallery_html: Path) -> int:
    try:
        text = gallery_html.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return 0
    return len(re.findall(r"<img\b", text))


def load_manifest(slug_dir: Path) -> dict:
    mf = slug_dir / "manifest.json"
    if not mf.exists():
        return {}
    try:
        return json.loads(mf.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def collect_entries() -> list[dict]:
    entries: list[dict] = []
    for d in sorted(ASSETS.iterdir()):
        if not d.is_dir():
            continue
        gallery = d / "gallery.html"
        if not gallery.exists():
            continue
        manifest = load_manifest(d)
        pdf_name = manifest.get("pdf") or (d.name + ".pdf")
        page_count = manifest.get("page_count")
        img_count = count_images(gallery)
        unique = manifest.get("unique_images") or img_count
        entries.append(
            {
                "slug": d.name,
                "title": pretty_title(d.name),
                "gallery_href": f"../_pdf_assets/{d.name}/gallery.html",
                "pdf_href": f"../_pdf/{pdf_name}",
                "pdf_name": pdf_name,
                "image_count": img_count,
                "unique_images": unique,
                "page_count": page_count,
            }
        )
    entries.sort(key=lambda e: e["title"].lower())
    return entries


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Photo Gallery &middot; K&Oslash;BG.COM (reconstruction)</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root {{ color-scheme: light; }}
body {{
  font: 15px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
        "Helvetica Neue", Arial, sans-serif;
  color: #1a1a1a;
  background: #fafaf6;
  margin: 0;
  padding: 24px 18px 64px;
}}
.wrap {{ max-width: 980px; margin: 0 auto; }}
header {{ border-bottom: 1px solid #d8d4c4; padding-bottom: 14px; margin-bottom: 22px; }}
header h1 {{ margin: 0 0 6px; font-size: 26px; }}
header p {{ margin: 4px 0; color: #4a4636; }}
.notice {{
  background: #fffbe6;
  border: 1px solid #f0c36d;
  border-radius: 6px;
  padding: 12px 16px;
  margin: 0 0 26px;
  color: #3b2f00;
  font-size: 14px;
  line-height: 1.5;
}}
.notice strong {{ color: #5a4400; }}
.summary {{ font-size: 14px; color: #555; margin: 0 0 18px; }}
ul.galleries {{
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 10px;
}}
ul.galleries li {{
  background: #fff;
  border: 1px solid #e2decd;
  border-radius: 6px;
  padding: 12px 14px;
  transition: border-color 0.15s, box-shadow 0.15s;
}}
ul.galleries li:hover {{
  border-color: #c2b97c;
  box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}}
ul.galleries a.title {{
  display: block;
  font-weight: 600;
  font-size: 15px;
  color: #2a4a8a;
  text-decoration: none;
  margin-bottom: 4px;
}}
ul.galleries a.title:hover {{ text-decoration: underline; }}
ul.galleries .meta {{
  font-size: 12px;
  color: #6a6450;
}}
ul.galleries .meta a {{ color: #6a6450; }}
nav.bottom {{
  margin-top: 32px;
  padding-top: 14px;
  border-top: 1px solid #d8d4c4;
  font-size: 13px;
  color: #555;
}}
nav.bottom a {{ color: #2a4a8a; }}
</style>
</head>
<body>
<div class="wrap">
<header>
  <h1>K&Oslash;BG Photo Gallery</h1>
  <p>Per-article image galleries reconstructed from the September 2022 PDF capture.</p>
</header>

<div class="notice">
  <strong>About this page.</strong>
  The original K&Oslash;BG.COM site ran a Gallery2 PHP photo gallery at
  <code>/gallery2/main&#46;php</code> with hundreds of albums and thousands
  of reader-contributed installation photos. That dynamic gallery could not
  be crawled or republished &mdash; only individual album entry pages were
  ever captured. What you can browse instead, below, are the article-by-article
  photo galleries extracted from the 43 PDF article captures that survive.
</div>

<p class="summary">{total_galleries} article galleries &middot; {total_images} images</p>

<ul class="galleries">
{rows}
</ul>

<nav class="bottom">
  <a href="../index.html">&larr; Back to K&Oslash;BG home</a>
  &middot;
  <a href="../about-reconstruction.html">About this reconstruction</a>
</nav>
</div>
</body>
</html>
"""


ROW_TEMPLATE = (
    '  <li>\n'
    '    <a class="title" href="{gallery_href}">{title}</a>\n'
    '    <div class="meta">{image_count} image{plural}'
    '{page_part}'
    ' &middot; <a href="{pdf_href}">source PDF</a></div>\n'
    '  </li>'
)


def render(entries: list[dict]) -> str:
    rows = []
    for e in entries:
        plural = "" if e["image_count"] == 1 else "s"
        if e["page_count"]:
            page_part = f' &middot; {e["page_count"]} page{"" if e["page_count"] == 1 else "s"}'
        else:
            page_part = ""
        rows.append(
            ROW_TEMPLATE.format(
                gallery_href=html.escape(e["gallery_href"]),
                title=html.escape(e["title"]),
                image_count=e["image_count"],
                plural=plural,
                page_part=page_part,
                pdf_href=html.escape(e["pdf_href"]),
            )
        )
    total_images = sum(e["image_count"] for e in entries)
    return HTML_TEMPLATE.format(
        total_galleries=len(entries),
        total_images=total_images,
        rows="\n".join(rows),
    )


def main() -> None:
    entries = collect_entries()
    if not entries:
        raise SystemExit("No _pdf_assets/<slug>/gallery.html files found.")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(entries), encoding="utf-8")
    total_images = sum(e["image_count"] for e in entries)
    print(f"Wrote {OUT.relative_to(ROOT)} ({len(entries)} galleries, {total_images} images)")


if __name__ == "__main__":
    main()
