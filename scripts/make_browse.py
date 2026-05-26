"""Generate a clean browseable index of the recovered K0BG.com pages."""

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "recovered" / "k0bg.com"
MANIFEST = Path(__file__).resolve().parent / "recovered" / "_manifest.json"
ASSETS = ROOT / "_pdf_assets"

TAG = re.compile(r"<[^>]+>")
WS = re.compile(r"\s+")
T = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)


# CC HTML filename -> (pdf filename, slug used under _pdf_assets/)
# Built from splice_assets.PDF_TO_HTML; keep this in sync.
HTML_TO_PDF: dict[str, tuple[str, str]] = {
    "abcs.html": ("ABCs.pdf", "abcs"),
    "alternator.html": ("Alternators & Batteries.pdf", "alternators-and-batteries"),
    "insure.html": ("Amateur Mobile Insurance.pdf", "amateur-mobile-insurance"),
    "options.html": ("Amateur Radio VHF Options.pdf", "amateur-radio-vhf-options"),
    "amplifiers.html": ("Amplifiers, Commercial.pdf", "amplifiers-commercial"),
    "caphats.html": ("Antenna Cap Hat.pdf", "antenna-cap-hat"),
    "coil.html": ("Antenna Coil Adjustment Procedure.pdf", "antenna-coil-adjustment-procedure"),
    "controllers.html": ("Antenna Controllers.pdf", "antenna-controllers"),
    "eff.html": ("Antenna Efficiency.pdf", "antenna-efficiency"),
    "match.html": ("Antenna Matching.pdf", "antenna-matching"),
    "antmount.html": ("Antenna Mounts.pdf", "antenna-mounts"),
    "myths.html": ("Antenna Myths.pdf", "antenna-myths"),
    "problems.html": ("Antenna Problems.pdf", "antenna-problems"),
    "shootout.html": ("Antenna Shootouts.pdf", "antenna-shootouts"),
    "antennas.html": ("Antenna, Commercial.pdf", "antenna-commercial"),
    "audio.html": ("Audio Filtering & Speakers.pdf", "audio-filtering-and-speakers"),
    "couplers.html": ("Auto-Couplers.pdf", "auto-couplers"),
    "bonding.html": ("Bonding.pdf", "bonding"),
    "cabling.html": ("Cables & Interfacing.pdf", "cables-and-interfacing"),
    "coax.html": ("Coax & PL259s.pdf", "coax-and-pl259s"),
    "common.html": ("Common Mode Currents.pdf", "common-mode-currents"),
    "static.html": ("Controlling Static.pdf", "controlling-static"),
    "electronics.html": ("Digital Electronics.pdf", "digital-electronics"),
    "glossary.html": ("Glossary of K0BG.pdf", "glossary-of-k0bg"),
    "ground.html": ("Grounds, RF & DC.pdf", "grounds-rf-and-dc"),
    "things.html": ("Home Brew Things.pdf", "home-brew-things"),
    "choke.html": ("How To Wind A Choke.pdf", "how-to-wind-a-choke"),
    "hybrid.html": ("Hybrid Automobiles.pdf", "hybrid-automobiles"),
    "ignition.html": ("Ignition Notes on RFI.pdf", "ignition-notes-on-rfi"),
    "install.html": ("Installation Notes.pdf", "installation-notes"),
    "index.html": (None, "k-bg-com"),  # home page; resolved by runtime mojibake fix
    "miniature.html": ("Miniature Radios.pdf", "miniature-radios"),
    "neat.html": ("Neat Gadgets.pdf", "neat-gadgets"),
    "otrrv.html": ("OTR & RV.pdf", "otr-and-rv"),
    "portable.html": ("Portable Operation.pdf", "portable-operation"),
    "rfi.html": ("RFI Problems.pdf", "rfi-problems"),
    "safety.html": ("Safe Mobile Operation.pdf", "safe-mobile-operation"),
    "signal.html": ("Signal To Noise Ratio.pdf", "signal-to-noise-ratio"),
    "beads.html": ("The Proper Split Beads to Suppress RFI.pdf", "the-proper-split-beads-to-suppress-rfi"),
    "audioxmit.html": ("Transmit Audio.pdf", "transmit-audio"),
    "tricks.html": ("Tricks of the Trade.pdf", "tricks-of-the-trade"),
    "what.html": ("What I Use.pdf", "what-i-use"),
    "wiring.html": ("Wiring & Grounding.pdf", "wiring-and-grounding"),
}


def article_title(raw: str, fallback: str) -> str:
    m = T.search(raw)
    if not m:
        return fallback
    title = html.unescape(WS.sub(" ", TAG.sub("", m.group(1)))).strip()
    if not title or title.lower() == "template":
        return fallback
    return title


def resolve_homepage_pdf() -> str | None:
    pdf_dir = ROOT / "_pdf"
    if not pdf_dir.exists():
        return None
    for p in pdf_dir.glob("*.pdf"):
        if re.match(r"K.{1,3}BG\.COM\.pdf", p.name, re.IGNORECASE):
            return p.name
    return None


def main() -> None:
    files = sorted(ROOT.glob("*.html"))
    rows = []
    for f in files:
        if f.name == "_browse.html":
            continue
        if f.name.endswith(".cc-original.html"):
            continue
        raw = f.read_text(encoding="utf-8", errors="replace")
        rows.append((f.name, article_title(raw, f.stem), f.stat().st_size))

    manifest = {}
    if MANIFEST.exists():
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8")).get("recovered", {})

    def meta(name: str):
        key = f"k0bg.com/{name}"
        info = manifest.get(key, {})
        return info.get("crawl", ""), info.get("timestamp", "")

    # gallery image counts + merge results
    image_counts: dict[str, int] = {}
    rollup_path = ASSETS / "rollup.json"
    if rollup_path.exists():
        for entry in json.loads(rollup_path.read_text(encoding="utf-8")):
            image_counts[entry["slug"]] = entry["images_unique"]

    merge_by_html: dict[str, dict] = {}
    merge_report = Path(__file__).resolve().parent / "merge-report.json"
    if merge_report.exists():
        for r in json.loads(merge_report.read_text(encoding="utf-8")):
            merge_by_html[r["html"]] = r

    homepage_pdf = resolve_homepage_pdf()

    parts = [
        "<!DOCTYPE html>",
        "<html><head><meta charset=\"utf-8\"><title>K0BG.com recovered articles</title>",
        "<style>",
        "body{font-family:Georgia,serif;max-width:1240px;margin:1.5em auto;padding:0 1em;color:#222}",
        "h1{border-bottom:2px solid #444}",
        ".note{background:#fffbe6;padding:.8em 1em;border-left:4px solid #d4a700;border-radius:4px;margin:1em 0}",
        "table{border-collapse:collapse;width:100%}",
        "td,th{padding:.3em .6em;border-bottom:1px solid #ddd;vertical-align:top}",
        "th{background:#f0f0f0;text-align:left}",
        ".small{color:#777;font-size:.85em}",
        "a{color:#0645ad;text-decoration:none}a:hover{text-decoration:underline}",
        ".pdf,.gal,.orig{font-size:.85em}",
        ".gal{color:#2a7a2a}",
        ".orig{color:#a04040}",
        ".merge-ok{background:#e6ffea;color:#22863a;font-weight:600;padding:.05em .4em;border-radius:3px}",
        ".merge-partial{background:#fff5b1;color:#735c0f;font-weight:600;padding:.05em .4em;border-radius:3px}",
        ".merge-none{color:#999}",
        "</style></head><body>",
        "<h1>K0BG.com &mdash; archival recovery</h1>",
        f"<p>{len(rows)} HTML pages reconstructed from 87 Common Crawl crawls (2008-2026). "
        "The Wayback Machine has zero captures of this domain because the site historically "
        "blocked the IA crawler.</p>",
        "<div class=\"note\"><strong>Images merged inline.</strong> Of 469 <code>&lt;img&gt;</code> "
        "tags across the 43 PDF-matched articles, <strong>464 now display real images</strong> "
        "extracted from the iOS PDFs (captured Sep 30 &ndash; Oct 1, 2022 via Safari Share &rarr; "
        "Save PDF &rarr; Dropbox). Mapping is positional: the k-th <code>&lt;img&gt;</code> in "
        "the CC HTML aligns to the k-th image in the PDF (Safari rendered top-to-bottom). "
        "Original <code>src</code> is preserved as <code>data-original-src</code> on every "
        "swapped tag so you can audit. The pre-merge CC version of each HTML is kept as "
        "<code>&lt;name&gt;.cc-original.html</code>.</div>",
        "<div class=\"note\">The 41 articles without a PDF are CC text-only with broken images. "
        "A background CC per-URL image scan is also running; any hits will land under "
        "<code>images/</code>.</div>",
        "<div class=\"note\">The site stylesheet <code>twoColLiqLtHdr.css</code> was not "
        "captured, so HTML renders unstyled, but prose, banner, and images are all intact. "
        "<a href=\"index.html\">Original index.html</a> &middot; "
        "<a href=\"indexleft.html\">Original left-nav</a></div>",
        "<table><thead><tr><th>File</th><th>Title</th><th>Merge</th><th>PDF</th><th>Gallery</th>"
        "<th>CC orig</th><th>Imgs</th><th>Size</th><th>Source crawl</th><th>Captured</th></tr></thead><tbody>",
    ]

    for name, title, size in rows:
        crawl, ts = meta(name)
        pdf_link = ""
        gallery_link = ""
        orig_link = ""
        img_count = ""
        merge_cell = "<span class=\"merge-none\">&mdash;</span>"

        entry = HTML_TO_PDF.get(name)
        if entry:
            pdf_name, slug = entry
            if name == "index.html" and pdf_name is None:
                pdf_name = homepage_pdf
            if pdf_name and (ROOT / "_pdf" / pdf_name).exists():
                pdf_link = f"<a class=\"pdf\" href=\"_pdf/{html.escape(pdf_name)}\">PDF</a>"
            gallery_path = ASSETS / slug / "gallery.html"
            if gallery_path.exists():
                gallery_link = f"<a class=\"gal\" href=\"_pdf_assets/{slug}/gallery.html\">gallery</a>"
                img_count = str(image_counts.get(slug, ""))
            m = merge_by_html.get(name)
            if m:
                if m["leftover"] == 0:
                    merge_cell = f"<span class=\"merge-ok\" title=\"{m['swapped']} swapped, 0 leftover\">{m['swapped']}/{m['swapped']}</span>"
                else:
                    tot = m["swapped"] + m["leftover"]
                    merge_cell = (
                        f"<span class=\"merge-partial\" "
                        f"title=\"{m['swapped']} swapped, {m['leftover']} left broken\">"
                        f"{m['swapped']}/{tot}</span>"
                    )
            cc_orig = ROOT / f"{Path(name).stem}.cc-original.html"
            if cc_orig.exists():
                orig_link = f"<a class=\"orig\" href=\"{cc_orig.name}\">CC raw</a>"

        parts.append(
            f"<tr><td><a href=\"{name}\">{name}</a></td>"
            f"<td>{html.escape(title)}</td>"
            f"<td>{merge_cell}</td>"
            f"<td>{pdf_link}</td>"
            f"<td>{gallery_link}</td>"
            f"<td>{orig_link}</td>"
            f"<td class=\"small\">{img_count}</td>"
            f"<td class=\"small\">{size:,}</td>"
            f"<td class=\"small\">{html.escape(crawl)}</td>"
            f"<td class=\"small\">{html.escape(ts)}</td></tr>"
        )
    parts.append("</tbody></table></body></html>")

    (ROOT / "_browse.html").write_text("\n".join(parts), encoding="utf-8")
    print(f"wrote _browse.html with {len(rows)} entries")


if __name__ == "__main__":
    main()
