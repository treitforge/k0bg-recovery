"""Rewrite CC-recovered HTML to use locally-extracted images from the PDFs.

Positional assumption (verified by counts):
  The k-th <img src=...> in the CC HTML aligns to the k-th unique image
  extracted from the matching iOS PDF, in page+index order. Safari rendered
  top-to-bottom, so the PDF's image order == the HTML's image order.

For each article in PDF_TO_HTML:
  - back up the current HTML to <name>.cc-original.html (only on first run)
  - parse <img ...> tags in document order, skipping any inside the banner
  - rewrite each src to point at _pdf_assets/<slug>/<filename> for image k
  - if there are more <img> tags than PDF images, leftover tags keep their
    original (broken) src and get a data-broken attribute so we can style them
  - if the PDF has more images than HTML, the extras stay in the gallery only
  - write merged HTML back to <name>.html

A short merge-report.json is written next to the script summarizing matches,
swaps, and any leftover broken refs.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from splice_assets import (
    BANNER_MARKER_END,
    BANNER_MARKER_START,
    HOMEPAGE_HTML,
    PDF_TO_HTML,
)

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "recovered" / "k0bg.com"
ASSETS = SITE / "_pdf_assets"

# Add the home page to the merge set; resolve its slug at runtime.
HTML_MAP: dict[str, str] = dict(PDF_TO_HTML)  # pdf_stem -> html_name

BANNER_RE = re.compile(
    re.escape(BANNER_MARKER_START) + r".*?" + re.escape(BANNER_MARKER_END),
    re.DOTALL,
)
IMG_RE = re.compile(r"<img\b([^>]*)>", re.IGNORECASE)
SRC_RE = re.compile(r"""\bsrc\s*=\s*(?P<q>["'])(?P<v>[^"']*)(?P=q)""", re.IGNORECASE)


def pdf_image_order(slug: str) -> list[str]:
    """Unique extracted filenames in page-then-index order."""
    manifest = json.loads((ASSETS / slug / "manifest.json").read_text(encoding="utf-8"))
    seen: set[str] = set()
    out: list[str] = []
    for page in manifest["pages"]:
        for img in page["images"]:
            if img.get("duplicate"):
                continue
            f = img["file"]
            if f in seen:
                continue
            seen.add(f)
            out.append(f)
    return out


def split_around_banner(text: str) -> tuple[str, str, str]:
    """Return (before, banner, after); banner may be empty."""
    m = BANNER_RE.search(text)
    if not m:
        return text, "", ""
    return text[: m.start()], text[m.start() : m.end()], text[m.end() :]


def backup_original(html_path: Path) -> None:
    bak = html_path.with_suffix(".cc-original.html")
    if bak.exists():
        return
    text = html_path.read_text(encoding="utf-8", errors="replace")
    # strip any provenance banner from the backup so it's truly the CC original
    text = BANNER_RE.sub("", text)
    bak.write_text(text, encoding="utf-8")


def rewrite_imgs(body: str, slug: str, ordered: list[str]) -> tuple[str, int, int]:
    """Rewrite img src in document order; return (new_body, swapped, leftover)."""
    out: list[str] = []
    cursor = 0
    idx = 0
    swapped = 0
    leftover = 0
    for m in IMG_RE.finditer(body):
        out.append(body[cursor : m.start()])
        inner = m.group(1)
        src_m = SRC_RE.search(inner)
        if not src_m:
            out.append(m.group(0))
            cursor = m.end()
            continue
        original_src = src_m.group("v")
        if idx < len(ordered):
            new_src = f"_pdf_assets/{slug}/{ordered[idx]}"
            new_inner = (
                inner[: src_m.start("v")] + new_src + inner[src_m.end("v") :]
            )
            # add data-original-src so we keep a breadcrumb
            if "data-original-src" not in new_inner.lower():
                new_inner += f' data-original-src="{original_src}"'
            out.append(f"<img{new_inner}>")
            swapped += 1
        else:
            # not enough extracted images; mark as missing
            new_inner = inner
            if "data-missing" not in new_inner.lower():
                new_inner += ' data-missing="true"'
            out.append(f"<img{new_inner}>")
            leftover += 1
        idx += 1
        cursor = m.end()
    out.append(body[cursor:])
    return "".join(out), swapped, leftover


def banner_with_merge_note(banner: str, swapped: int, total_pdf: int) -> str:
    if not banner:
        return banner
    note = (
        " &middot; <strong>{} of {} images merged inline from the PDF</strong>."
        " Original src kept on each <code>&lt;img&gt;</code> as <code>data-original-src</code>.".format(
            swapped, total_pdf
        )
    )
    if "images merged inline" in banner:
        # already noted; replace
        banner = re.sub(
            r"\s&middot; <strong>\d+ of \d+ images merged inline.*?</code>\.",
            "",
            banner,
        )
    # insert before the closing </div> of the banner box
    banner = banner.replace(
        ".</div>", "." + note + "</div>", 1
    ) if banner.endswith(BANNER_MARKER_END) and ".</div>" in banner else banner
    return banner


def merge_one(pdf_stem: str, html_name: str) -> dict | None:
    html_path = SITE / html_name
    if not html_path.exists():
        return None
    # find slug from rollup
    rollup = json.loads((ASSETS / "rollup.json").read_text(encoding="utf-8"))
    slug = None
    for e in rollup:
        if e["pdf"].rsplit(".", 1)[0] == pdf_stem:
            slug = e["slug"]
            break
    if not slug:
        return None
    ordered = pdf_image_order(slug)
    if not ordered:
        return {"html": html_name, "swapped": 0, "leftover": 0, "pdf_imgs": 0}

    backup_original(html_path)
    text = html_path.read_text(encoding="utf-8", errors="replace")
    before, banner, after = split_around_banner(text)
    body = before + after
    new_body, swapped, leftover = rewrite_imgs(body, slug, ordered)

    # reinsert banner (with a small merge note) right after <body...>
    new_banner = banner_with_merge_note(banner, swapped, len(ordered))
    if new_banner:
        body_match = re.search(r"<body[^>]*>", new_body, re.IGNORECASE)
        if body_match:
            i = body_match.end()
            new_body = new_body[:i] + "\n" + new_banner + "\n" + new_body[i:]
        else:
            new_body = new_banner + "\n" + new_body

    html_path.write_text(new_body, encoding="utf-8")
    return {
        "html": html_name,
        "pdf_stem": pdf_stem,
        "slug": slug,
        "pdf_imgs": len(ordered),
        "swapped": swapped,
        "leftover": leftover,
    }


def find_homepage_pdf_stem(rollup: list[dict]) -> str | None:
    for e in rollup:
        stem = e["pdf"].rsplit(".", 1)[0]
        norm = re.sub(r"[^A-Za-z0-9]", "", stem).upper()
        if norm in ("KBGCOM", "K0BGCOM"):
            return stem
    return None


def main() -> int:
    rollup = json.loads((ASSETS / "rollup.json").read_text(encoding="utf-8"))
    homepage_stem = find_homepage_pdf_stem(rollup)
    if homepage_stem:
        HTML_MAP[homepage_stem] = HOMEPAGE_HTML

    results = []
    for stem, html_name in sorted(HTML_MAP.items()):
        r = merge_one(stem, html_name)
        if r is None:
            print(f"  [-] {stem:45s} -> {html_name} (skipped: html missing)")
            continue
        flag = "[OK]" if r["leftover"] == 0 else "[!] "
        print(
            f"  {flag} {stem:45s} -> {html_name:20s} "
            f"swapped={r['swapped']:>3}  leftover={r['leftover']}  pdf={r['pdf_imgs']}"
        )
        results.append(r)

    (ROOT / "merge-report.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8"
    )
    swapped_total = sum(r["swapped"] for r in results)
    leftover_total = sum(r["leftover"] for r in results)
    print()
    print(
        f"merged {len(results)} HTML files; swapped {swapped_total} <img> srcs; "
        f"{leftover_total} <img> tags had no PDF counterpart (kept original src)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
