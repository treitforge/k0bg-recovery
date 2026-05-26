"""Smarter merge: match HTML <img> tags to PDF-extracted images by aspect ratio.

Positional ordering was wrong for many articles because the iOS PDF rasterizer
lays out images in visual (top-to-bottom, left-to-right) order while HTML source
order follows markup position. With floated images, those diverge.

The HTML <img> tag's width/height attributes encode the intended display
geometry, which (since they came from Alan's original site) reliably matches
the aspect ratio of the original image. Each extracted JPEG/PNG has known
pixel dimensions. Matching on aspect ratio is therefore an excellent signal.

Algorithm:
  1. For each article, read each <img>'s declared (w, h) and each extracted
     image's actual pixel dims.
  2. Compute pairwise cost = |log(aspect_html) - log(aspect_real)|
     (log so 7.46->1.15 and 1.15->7.46 are equally bad).
  3. Solve as a bipartite assignment problem (Hungarian) over the smaller
     of the two sides.
  4. For any HTML img with no dims, fall back to positional order among
     unassigned extracted images.
  5. Restore the original HTML width/height (it is the intended display size).
"""
from __future__ import annotations

import json
import math
import re
import struct
import zlib
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

BANNER_RE = re.compile(
    re.escape(BANNER_MARKER_START) + r".*?" + re.escape(BANNER_MARKER_END),
    re.DOTALL,
)
IMG_RE = re.compile(r"<img\b([^>]*)>", re.IGNORECASE)
SRC_RE = re.compile(r"""\bsrc\s*=\s*(?P<q>["'])(?P<v>[^"']*)(?P=q)""", re.IGNORECASE)
W_RE = re.compile(r'\bwidth\s*=\s*"?(\d+)"?', re.IGNORECASE)
H_RE = re.compile(r'\bheight\s*=\s*"?(\d+)"?', re.IGNORECASE)


def jpeg_dims(data: bytes) -> tuple[int, int] | None:
    i = 2
    n = len(data)
    while i + 4 < n:
        if data[i] != 0xFF:
            return None
        marker = data[i + 1]
        if marker in (0xD8, 0xD9):
            i += 2
            continue
        seglen = struct.unpack(">H", data[i + 2 : i + 4])[0]
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            if i + 9 > n:
                return None
            h, w = struct.unpack(">HH", data[i + 5 : i + 9])
            return (w, h)
        i += 2 + seglen
    return None


def png_dims(data: bytes) -> tuple[int, int] | None:
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    # IHDR follows the 8-byte signature: length(4) + 'IHDR'(4) + width(4) + height(4) ...
    w, h = struct.unpack(">II", data[16:24])
    return (w, h)


def image_dims(path: Path) -> tuple[int, int] | None:
    data = path.read_bytes()
    if path.suffix.lower() in (".jpg", ".jpeg"):
        return jpeg_dims(data)
    if path.suffix.lower() == ".png":
        return png_dims(data)
    # generic
    if data[:2] == b"\xff\xd8":
        return jpeg_dims(data)
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return png_dims(data)
    return None


def hungarian(cost: list[list[float]]) -> list[int]:
    """Solve square assignment via O(n^3) Hungarian. Returns row->col."""
    n = len(cost)
    INF = float("inf")
    u = [0.0] * (n + 1)
    v = [0.0] * (n + 1)
    p = [0] * (n + 1)
    way = [0] * (n + 1)
    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = [INF] * (n + 1)
        used = [False] * (n + 1)
        while True:
            used[j0] = True
            i0 = p[j0]
            delta = INF
            j1 = -1
            for j in range(1, n + 1):
                if not used[j]:
                    cur = cost[i0 - 1][j - 1] - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j
            for j in range(n + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while j0 != 0:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
    result = [-1] * n
    for j in range(1, n + 1):
        if p[j] != 0:
            result[p[j] - 1] = j - 1
    return result


def aspect_cost(ar_h: float | None, ar_p: float | None) -> float:
    if ar_h is None or ar_p is None:
        # missing data: large but finite cost so it's a tie-breaker for unmatched
        return 5.0
    return abs(math.log(ar_h) - math.log(ar_p))


def solve_assignment(html_imgs: list[dict], pdf_imgs: list[dict]) -> list[int]:
    """Return mapping html_idx -> pdf_idx (or -1 if no PDF image left).

    We add dummy rows or columns so the matrix is square; dummies have cost 5.0
    so real matches always beat them when available.
    """
    n_h = len(html_imgs)
    n_p = len(pdf_imgs)
    n = max(n_h, n_p, 1)
    cost: list[list[float]] = [[5.0] * n for _ in range(n)]
    for i in range(n_h):
        ar_h = html_imgs[i].get("ar")
        for j in range(n_p):
            ar_p = pdf_imgs[j].get("ar")
            base = aspect_cost(ar_h, ar_p)
            # tiny position-tie-breaker so equally-good matches prefer same order
            order_penalty = abs((i / max(n_h - 1, 1)) - (j / max(n_p - 1, 1))) * 0.001
            cost[i][j] = base + order_penalty
    assignment = hungarian(cost)
    result: list[int] = [-1] * n_h
    for i in range(n_h):
        j = assignment[i]
        if j < n_p:
            result[i] = j
    return result


def pdf_image_list(slug: str) -> list[dict]:
    """Return list of {file, ar, w, h} unique images in page-then-index order."""
    manifest = json.loads((ASSETS / slug / "manifest.json").read_text(encoding="utf-8"))
    seen: set[str] = set()
    out: list[dict] = []
    for page in manifest["pages"]:
        for img in page["images"]:
            if img.get("duplicate"):
                continue
            f = img["file"]
            if f in seen:
                continue
            seen.add(f)
            p = ASSETS / slug / f
            dims = image_dims(p) if p.exists() else None
            ar = (dims[0] / dims[1]) if dims and dims[1] else None
            out.append({"file": f, "w": dims[0] if dims else None,
                        "h": dims[1] if dims else None, "ar": ar})
    return out


def parse_html_imgs(body: str) -> list[dict]:
    """Return list of {match_start, match_end, src_start, src_end, src, ar} per <img>."""
    out: list[dict] = []
    for m in IMG_RE.finditer(body):
        inner = m.group(1)
        s = SRC_RE.search(inner)
        if not s:
            continue
        w_m = W_RE.search(inner)
        h_m = H_RE.search(inner)
        w = int(w_m.group(1)) if w_m else None
        h = int(h_m.group(1)) if h_m else None
        ar = (w / h) if (w and h) else None
        out.append(
            {
                "match_start": m.start(),
                "match_end": m.end(),
                # convert inner offsets to body offsets
                "src_start": m.start(1) + s.start("v"),
                "src_end": m.start(1) + s.end("v"),
                "src": s.group("v"),
                "w": w,
                "h": h,
                "ar": ar,
            }
        )
    return out


def split_around_banner(text: str) -> tuple[str, str, str]:
    m = BANNER_RE.search(text)
    if not m:
        return text, "", ""
    return text[: m.start()], text[m.start() : m.end()], text[m.end() :]


def restore_from_backup(html_path: Path) -> str:
    bak = html_path.with_suffix(".cc-original.html")
    if bak.exists():
        return bak.read_text(encoding="utf-8", errors="replace")
    text = html_path.read_text(encoding="utf-8", errors="replace")
    return BANNER_RE.sub("", text)


def banner_html_with_note(pdf_name: str, slug: str, image_count: int, swapped: int) -> str:
    pdf_href = f"_pdf/{pdf_name}"
    gallery_rel = f"_pdf_assets/{slug}/gallery.html"
    # The <style> rule prevents visible squishing when the PDF-extracted image
    # has a different aspect ratio from the HTML's hardcoded width/height.
    return (
        BANNER_MARKER_START
        + "<style>img[data-original-src]{height:auto !important;max-width:100%}</style>"
        + "<div style=\"background:#fffbe6;border:1px solid #f0c36d;padding:10px 14px;"
        "margin:0 0 14px 0;border-radius:6px;font:14px/1.45 system-ui,sans-serif;color:#3b2f00\">"
        "<strong>Recovered article.</strong> HTML body is from Common Crawl (text only);"
        f" images came from the Sep 2022 iOS PDF: <a href=\"{pdf_href}\">{pdf_name}</a>"
        f" &middot; <a href=\"{gallery_rel}\">{image_count} extracted images &amp; links</a>"
        f" &middot; <strong>{swapped} of {image_count} images merged inline</strong>"
        " (aspect-ratio matched). Original src preserved on each "
        "<code>&lt;img&gt;</code> as <code>data-original-src</code>.</div>"
        + BANNER_MARKER_END
    )


def merge_one(pdf_stem: str, html_name: str) -> dict | None:
    html_path = SITE / html_name
    if not html_path.exists():
        return None
    rollup = json.loads((ASSETS / "rollup.json").read_text(encoding="utf-8"))
    slug = pdf_name = None
    for e in rollup:
        if e["pdf"].rsplit(".", 1)[0] == pdf_stem:
            slug = e["slug"]
            pdf_name = e["pdf"]
            break
    if not slug:
        return None

    pdf_imgs = pdf_image_list(slug)
    if not pdf_imgs:
        return {"html": html_name, "swapped": 0, "leftover": 0, "pdf_imgs": 0}

    # always operate on the CC original, not the previously-merged body
    body = restore_from_backup(html_path)
    html_imgs = parse_html_imgs(body)
    if not html_imgs:
        return {"html": html_name, "swapped": 0, "leftover": 0, "pdf_imgs": len(pdf_imgs)}

    mapping = solve_assignment(html_imgs, pdf_imgs)

    # Rewrite body using the matched src. Process in reverse so offsets stay valid.
    new_body = body
    swapped = 0
    leftover = 0
    for i in range(len(html_imgs) - 1, -1, -1):
        info = html_imgs[i]
        j = mapping[i]
        if j < 0:
            # mark as missing
            tag = new_body[info["match_start"] : info["match_end"]]
            if "data-missing" not in tag.lower():
                tag = tag[:-1] + ' data-missing="true">'
            new_body = new_body[: info["match_start"]] + tag + new_body[info["match_end"] :]
            leftover += 1
            continue
        new_src = f"_pdf_assets/{slug}/{pdf_imgs[j]['file']}"
        # replace just the src value
        new_body = (
            new_body[: info["src_start"]] + new_src + new_body[info["src_end"] :]
        )
        # add data-original-src right before the closing >
        # Find the new match_end (it shifted by len(new_src) - len(old))
        delta = len(new_src) - (info["src_end"] - info["src_start"])
        new_match_end = info["match_end"] + delta
        # Insert before the final '>' of this tag
        if 'data-original-src' not in new_body[info["match_start"] : new_match_end].lower():
            insertion = f' data-original-src="{info["src"]}"'
            insert_pos = new_match_end - 1  # before '>'
            new_body = new_body[:insert_pos] + insertion + new_body[insert_pos:]
        swapped += 1

    # Banner
    banner = banner_html_with_note(pdf_name, slug, len(pdf_imgs), swapped)
    body_match = re.search(r"<body[^>]*>", new_body, re.IGNORECASE)
    if body_match:
        idx = body_match.end()
        new_body = new_body[:idx] + "\n" + banner + "\n" + new_body[idx:]
    else:
        new_body = banner + "\n" + new_body

    html_path.write_text(new_body, encoding="utf-8")
    return {
        "html": html_name,
        "pdf_stem": pdf_stem,
        "slug": slug,
        "pdf_imgs": len(pdf_imgs),
        "html_imgs": len(html_imgs),
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
    html_map: dict[str, str] = dict(PDF_TO_HTML)
    stem = find_homepage_pdf_stem(rollup)
    if stem:
        html_map[stem] = HOMEPAGE_HTML

    results = []
    for stem, html_name in sorted(html_map.items()):
        r = merge_one(stem, html_name)
        if r is None:
            print(f"  [-] {stem:45s} -> {html_name} (skipped)")
            continue
        flag = "[OK]" if r["leftover"] == 0 else "[!] "
        print(
            f"  {flag} {stem:45s} -> {html_name:20s} "
            f"swapped={r['swapped']:>3}  leftover={r['leftover']}  pdf={r['pdf_imgs']}  html={r.get('html_imgs','?')}"
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
        f"{leftover_total} <img> tags had no PDF counterpart"
    )
    try:
        import fix_layout
        fix_layout.main()
    except Exception as exc:  # pragma: no cover
        print(f"WARN: fix_layout did not run cleanly: {exc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
