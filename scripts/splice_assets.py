"""Build per-article PDF galleries and splice provenance banners into CC HTML.

For each rebuilt PDF:
  - Build _pdf_assets/<slug>/gallery.html with thumbnails of every extracted image
    in page+index order, plus a links section grouping URIs by page.
  - Find the best-matching CC-recovered .html article using an explicit map
    (the CC filenames are abbreviations like 'antmount.html' that no fuzzy
    matcher can guess reliably). Prepend a banner pointing at the gallery
    and the PDF.

This script is idempotent: it strips ALL prior banners from every HTML file
before re-inserting, so re-running cleans up earlier mismatches.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "recovered" / "k0bg.com"
ASSETS = SITE / "_pdf_assets"
PDF_DIR_REL = "_pdf"  # served alongside the site

BANNER_MARKER_START = "<!-- KOBG_PROVENANCE_BANNER_START -->"
BANNER_MARKER_END = "<!-- KOBG_PROVENANCE_BANNER_END -->"

# Explicit PDF basename -> CC HTML filename map, hand-verified from the
# k0bg.com filename conventions (Alan used short abbreviations like
# "antmount" / "wiring" / "signal" that fuzzy slugging cannot recover).
PDF_TO_HTML: dict[str, str] = {
    "ABCs": "abcs.html",
    "Alternators & Batteries": "alternator.html",
    "Amateur Mobile Insurance": "insure.html",
    "Amateur Radio VHF Options": "options.html",
    "Amplifiers, Commercial": "amplifiers.html",
    "Antenna Cap Hat": "caphats.html",
    "Antenna Coil Adjustment Procedure": "coil.html",
    "Antenna Controllers": "controllers.html",
    "Antenna Efficiency": "eff.html",
    "Antenna Matching": "match.html",
    "Antenna Mounts": "antmount.html",
    "Antenna Myths": "myths.html",
    "Antenna Problems": "problems.html",
    "Antenna Shootouts": "shootout.html",
    "Antenna, Commercial": "antennas.html",
    "Audio Filtering & Speakers": "audio.html",
    "Auto-Couplers": "couplers.html",
    "Bonding": "bonding.html",
    "Cables & Interfacing": "cabling.html",
    "Coax & PL259s": "coax.html",
    "Common Mode Currents": "common.html",
    "Controlling Static": "static.html",
    "Digital Electronics": "electronics.html",
    "Glossary of K0BG": "glossary.html",
    "Grounds, RF & DC": "ground.html",
    "Home Brew Things": "things.html",
    "How To Wind A Choke": "choke.html",
    "Hybrid Automobiles": "hybrid.html",
    "Ignition Notes on RFI": "ignition.html",
    "Installation Notes": "install.html",
    "Miniature Radios": "miniature.html",
    "Neat Gadgets": "neat.html",
    "OTR & RV": "otrrv.html",
    "Portable Operation": "portable.html",
    "RFI Problems": "rfi.html",
    "Safe Mobile Operation": "safety.html",
    "Signal To Noise Ratio": "signal.html",
    "The Proper Split Beads to Suppress RFI": "beads.html",
    "Transmit Audio": "audioxmit.html",
    "Tricks of the Trade": "tricks.html",
    "What I Use": "what.html",
    "Wiring & Grounding": "wiring.html",
}
# The home-page PDF has a non-ASCII filename (KØBG.COM.pdf, mojibaked as
# "K╪BG.COM.pdf" on Windows). Resolve at runtime by extension+size match.
HOMEPAGE_PDF_TITLE = "KØBG.COM"
HOMEPAGE_HTML = "index.html"


def slugify(s: str) -> str:
    s = s.lower()
    s = re.sub(r"&", " and ", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def normalized_token(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def page_title(html_text: str, fallback: str) -> str:
    m = re.search(r"<title>([^<]+)</title>", html_text, re.IGNORECASE)
    if m:
        return html.unescape(m.group(1)).strip()
    return fallback


def build_gallery(slug: str, manifest: dict, html_filename: str | None) -> None:
    target = ASSETS / slug
    pdf_name = manifest["pdf"]
    title = pdf_name.rsplit(".", 1)[0]

    pieces: list[str] = []
    pieces.append("<!doctype html><html><head><meta charset='utf-8'>")
    pieces.append(f"<title>{html.escape(title)} - extracted assets</title>")
    pieces.append(
        "<style>"
        "body{font:14px/1.4 system-ui,sans-serif;margin:24px;max-width:1100px;background:#fafafa;color:#111}"
        "h1{font-size:20px;margin:0 0 4px}"
        "h2{font-size:15px;margin:24px 0 8px;border-bottom:1px solid #ddd;padding-bottom:4px}"
        ".meta{color:#555;margin-bottom:18px}"
        ".meta a{color:#0366d6}"
        ".grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px}"
        ".card{background:#fff;border:1px solid #e1e4e8;border-radius:6px;padding:8px;text-align:center}"
        ".card img{max-width:100%;max-height:200px;display:block;margin:0 auto 6px}"
        ".card .lbl{font-size:11px;color:#666;font-family:ui-monospace,monospace}"
        ".uris{background:#fff;border:1px solid #e1e4e8;border-radius:6px;padding:12px}"
        ".uris details{margin-bottom:8px}"
        ".uris summary{cursor:pointer;font-weight:600}"
        ".uris ul{margin:6px 0 0 0;padding-left:20px}"
        ".uris li{margin:2px 0;word-break:break-all}"
        "</style></head><body>"
    )
    pieces.append(f"<h1>{html.escape(title)}</h1>")
    pieces.append("<div class='meta'>")
    pieces.append(
        "Images and outbound links extracted from "
        f"<a href='../../{PDF_DIR_REL}/{html.escape(pdf_name)}'>{html.escape(pdf_name)}</a>, "
        f"a Sep 2022 iOS PDF capture of the live K0BG.com article. "
        f"{manifest['page_count']} pages, {manifest['unique_images']} unique images."
    )
    if html_filename:
        pieces.append(
            f" &middot; <a href='../../{html.escape(html_filename)}'>Common Crawl HTML</a>"
        )
    pieces.append("</div>")

    pieces.append("<h2>Images</h2><div class='grid'>")
    seen = set()
    for page in manifest["pages"]:
        for img in page["images"]:
            if img.get("duplicate"):
                continue
            f = img["file"]
            if f in seen:
                continue
            seen.add(f)
            pieces.append(
                f"<div class='card'><a href='{html.escape(f)}'>"
                f"<img src='{html.escape(f)}' loading='lazy' alt=''></a>"
                f"<div class='lbl'>p{page['page']} &middot; {html.escape(f)}</div></div>"
            )
    pieces.append("</div>")

    pieces.append("<h2>Outbound links (by page)</h2><div class='uris'>")
    for page in manifest["pages"]:
        if not page["uris"]:
            continue
        unique = []
        seen_u = set()
        for u in page["uris"]:
            if u not in seen_u:
                seen_u.add(u)
                unique.append(u)
        pieces.append(
            f"<details open><summary>Page {page['page']} ({len(unique)} links)</summary><ul>"
        )
        for u in unique:
            pieces.append(
                f"<li><a href='{html.escape(u)}' rel='noopener'>{html.escape(u)}</a></li>"
            )
        pieces.append("</ul></details>")
    pieces.append("</div></body></html>")
    (target / "gallery.html").write_text("\n".join(pieces), encoding="utf-8")


def html_candidates() -> dict[str, Path]:
    out: dict[str, Path] = {}
    for p in SITE.glob("*.html"):
        if p.name in ("_browse.html",):
            continue
        out[p.name] = p
    return out


def pdf_title_to_filename(rollup: list[dict]) -> dict[str, str]:
    """Map normalized PDF stem -> actual filename on disk (handles mojibake)."""
    out: dict[str, str] = {}
    for entry in rollup:
        stem = entry["pdf"].rsplit(".", 1)[0]
        out[stem] = entry["pdf"]
    return out


def resolve_html(pdf_stem: str, candidates: dict[str, Path]) -> Path | None:
    # explicit map first
    if pdf_stem in PDF_TO_HTML:
        name = PDF_TO_HTML[pdf_stem]
        return candidates.get(name)
    # home page - filename has mojibake-prone non-ASCII char
    norm = re.sub(r"[^A-Za-z0-9]", "", pdf_stem)
    if norm.upper() in ("KBGCOM", "K0BGCOM"):
        return candidates.get(HOMEPAGE_HTML)
    return None


def strip_all_banners() -> int:
    """Remove any prior provenance banner from every HTML file in SITE."""
    count = 0
    pattern = re.compile(
        re.escape(BANNER_MARKER_START) + r".*?" + re.escape(BANNER_MARKER_END)
        + r"\s*",
        re.DOTALL,
    )
    for p in SITE.glob("*.html"):
        if p.name == "_browse.html":
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        new = pattern.sub("", text)
        if new != text:
            p.write_text(new, encoding="utf-8")
            count += 1
    return count


def banner_html(slug: str, pdf_name: str, gallery_rel: str, image_count: int) -> str:
    pdf_href = f"{PDF_DIR_REL}/{html.escape(pdf_name)}"
    return (
        BANNER_MARKER_START
        + "<div style=\"background:#fffbe6;border:1px solid #f0c36d;padding:10px 14px;"
        "margin:0 0 14px 0;border-radius:6px;font:14px/1.45 system-ui,sans-serif;color:#3b2f00\">"
        "<strong>Recovered article.</strong> The HTML above is from Common Crawl (text only)."
        f" Original images and layout were captured in a Sep 2022 iOS PDF: "
        f"<a href=\"{pdf_href}\">{html.escape(pdf_name)}</a>"
        f" &middot; <a href=\"{html.escape(gallery_rel)}\">{image_count} extracted images &amp; links</a>"
        ".</div>"
        + BANNER_MARKER_END
    )


def inject_banner(html_path: Path, banner: str) -> None:
    text = html_path.read_text(encoding="utf-8", errors="replace")
    # strip prior banner if present (idempotent)
    text = re.sub(
        re.escape(BANNER_MARKER_START) + r".*?" + re.escape(BANNER_MARKER_END)
        + r"\s*",
        "",
        text,
        flags=re.DOTALL,
    )
    body_match = re.search(r"<body[^>]*>", text, re.IGNORECASE)
    if body_match:
        idx = body_match.end()
        new_text = text[:idx] + "\n" + banner + "\n" + text[idx:]
    else:
        new_text = banner + "\n" + text
    html_path.write_text(new_text, encoding="utf-8")


def main() -> int:
    rollup = json.loads((ASSETS / "rollup.json").read_text(encoding="utf-8"))
    candidates = html_candidates()
    stripped = strip_all_banners()
    print(f"stripped existing banners from {stripped} html files")
    print()
    matched = 0
    unmatched: list[str] = []
    for entry in rollup:
        slug = entry["slug"]
        manifest = json.loads((ASSETS / slug / "manifest.json").read_text(encoding="utf-8"))
        pdf_stem = entry["pdf"].rsplit(".", 1)[0]
        html_path = resolve_html(pdf_stem, candidates)
        html_name = html_path.name if html_path else None
        build_gallery(slug, manifest, html_name)
        if html_path:
            gallery_rel = f"_pdf_assets/{slug}/gallery.html"
            banner = banner_html(
                slug, entry["pdf"], gallery_rel, entry["images_unique"]
            )
            inject_banner(html_path, banner)
            matched += 1
            print(f"  [+] {entry['pdf']:45s} -> {html_name}")
        else:
            unmatched.append(entry["pdf"])
            print(f"  [-] {entry['pdf']:45s} -> (no HTML match; gallery only)")
    print()
    print(f"matched {matched}/{len(rollup)} PDFs to HTML files")
    if unmatched:
        print("unmatched:")
        for u in unmatched:
            print("  -", u)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
