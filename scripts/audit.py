"""Audit FixInProduction/k0bg-rebuilt against the Common Crawl originals.

Produces AUDIT-vs-rebuilt.md inside the recovery workspace.

Pairing strategy:
  1. Hand-curated filename hints (rebuilt name -> original name).
  2. Fall back to best document-shingle Jaccard match.

Per pair we report:
  * Title (original vs rebuild)
  * Word counts and expansion ratio rebuild/original
  * Document 5-gram shingle Jaccard
  * Section coverage: original "Contents: A ; B ; C" tokens that appear in
    the rebuild prose
  * Sentence-level missing (original sentences with no echo in rebuild) and
    candidate fabrications (rebuild sentences with no support in original)

Orphan originals (no rebuild counterpart) and weak rebuild matches (no
plausible original) are listed separately. The rebuild's own AUDIT.md
claims are spot-checked.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ORIG_DIR = HERE / "recovered" / "k0bg.com"
REBUILT_DIR = HERE / "rebuilt"
REPORT_PATH = HERE / "AUDIT-vs-rebuilt.md"

TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")
SENT_SPLIT_RE = re.compile(r"(?<=[\.!?])\s+(?=[A-Z0-9\"\(])")
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.I | re.S)
SCRIPT_STYLE_RE = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.I | re.S)
NAV_RE = re.compile(r"<nav[^>]*>.*?</nav>", re.I | re.S)
HEADER_RE = re.compile(r"<header[^>]*>.*?</header>", re.I | re.S)
FOOTER_RE = re.compile(r"<footer[^>]*>.*?</footer>", re.I | re.S)
CONTENTS_RE = re.compile(r"Contents\s*:\s*([^.]+?)(?:\s{2,}|;\s*[A-Z][a-z]+\s+[A-Z])", re.I)

REBUILT_TO_ORIGINAL: dict[str, str | None] = {
    "abcs.html": "abcs.html",
    "alternators-batteries.html": "alternator.html",
    "amplifiers.html": "amplifiers.html",
    "antenna-cap-hat.html": "caphats.html",
    "antenna-commercial.html": "antennas.html",
    "antenna-controllers.html": "controllers.html",
    "antenna-efficiency.html": "eff.html",
    "antenna-matching.html": "match.html",
    "antenna-mounts.html": "antmount.html",
    "antenna-myths.html": "myths.html",
    "antenna-problems.html": "problems.html",
    "antenna-shootouts.html": "shootout.html",
    "audio-filtering.html": "audio.html",
    "auto-couplers.html": "couplers.html",
    "bonding.html": "bonding.html",
    "cables-interfacing.html": "cabling.html",
    "coax-pl259.html": "coax.html",
    "coil-adjustment.html": "coil.html",
    "common-mode.html": "common.html",
    "controlling-static.html": "static.html",
    "digital-electronics.html": "electronics.html",
    "glossary.html": "glossary.html",
    "grounds.html": "ground.html",
    "home-brew.html": "things.html",
    "how-to-wind-choke.html": "choke.html",
    "hybrid-ev.html": "hybrid.html",
    "installation.html": "install.html",
    "insurance.html": "insure.html",
    "miniature-radios.html": "miniature.html",
    "neat-gadgets.html": "neat.html",
    "otr-rv.html": "otrrv.html",
    "portable-operation.html": "portable.html",
    "rfi.html": "rfi.html",
    "safety.html": "safety.html",
    "signal-noise-ratio.html": "signal.html",
    "transmit-audio.html": "audioxmit.html",
    "tricks.html": "tricks.html",
    "vhf-options.html": "options.html",
    "what-i-use.html": "what.html",
    "wiring.html": "wiring.html",
}


def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return p.read_text(encoding="latin-1", errors="replace")


def extract_title(raw: str) -> str:
    m = TITLE_RE.search(raw)
    title = ""
    if m:
        title = html.unescape(WS_RE.sub(" ", TAG_RE.sub("", m.group(1)))).strip()
    if not title or title.lower() == "template":
        m = H1_RE.search(raw)
        if m:
            title = html.unescape(WS_RE.sub(" ", TAG_RE.sub("", m.group(1)))).strip()
    return title


def visible_text(raw: str) -> str:
    cleaned = SCRIPT_STYLE_RE.sub(" ", raw)
    cleaned = NAV_RE.sub(" ", cleaned)
    cleaned = HEADER_RE.sub(" ", cleaned)
    cleaned = FOOTER_RE.sub(" ", cleaned)
    txt = TAG_RE.sub(" ", cleaned)
    txt = html.unescape(txt)
    return WS_RE.sub(" ", txt).strip()


def section_topics(text: str) -> list[str]:
    m = CONTENTS_RE.search(text)
    if not m:
        return []
    raw = m.group(1)
    parts = [p.strip(" ;") for p in raw.split(";")]
    return [p for p in parts if 2 <= len(p) <= 80]


def sentences(text: str) -> list[str]:
    if not text:
        return []
    raw = SENT_SPLIT_RE.split(text)
    out: list[str] = []
    for s in raw:
        s = s.strip()
        if len(s) >= 25:
            out.append(s)
    return out


def norm(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    return WS_RE.sub(" ", s).strip()


def shingles(s: str, n: int = 6) -> set[str]:
    toks = norm(s).split()
    if len(toks) < n:
        return {" ".join(toks)} if toks else set()
    return {" ".join(toks[i : i + n]) for i in range(len(toks) - n + 1)}


def doc_shingles(text: str, n: int = 5) -> set[str]:
    toks = norm(text).split()
    if len(toks) < n:
        return {" ".join(toks)} if toks else set()
    return {" ".join(toks[i : i + n]) for i in range(len(toks) - n + 1)}


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def section_coverage(orig_sections: list[str], rb_text: str) -> tuple[int, int, list[str]]:
    rb_low = rb_text.lower()
    missing: list[str] = []
    hit = 0
    for sec in orig_sections:
        sec_norm = re.sub(r"[^a-z0-9 ]+", " ", sec.lower())
        toks = [t for t in sec_norm.split() if len(t) > 2]
        if not toks:
            hit += 1
            continue
        if all(t in rb_low for t in toks):
            hit += 1
        else:
            missing.append(sec)
    return hit, len(orig_sections), missing


def load_article(path: Path) -> dict:
    raw = read_text(path)
    text = visible_text(raw)
    return {
        "path": path,
        "name": path.name,
        "title": extract_title(raw),
        "text": text,
        "words": len(text.split()),
        "sentences": sentences(text),
        "doc_shings": doc_shingles(text),
        "sections": section_topics(text),
    }


def main() -> None:
    rebuilt_articles_dir = REBUILT_DIR / "articles"
    rebuilt_files = sorted(rebuilt_articles_dir.glob("*.html"))
    original_files = sorted(ORIG_DIR.glob("*.html"))

    rebuilt = {f.name: load_article(f) for f in rebuilt_files}
    originals = {}
    for f in original_files:
        art = load_article(f)
        if art["words"] >= 100:
            originals[art["name"]] = art

    used_orig: set[str] = set()
    pairings: list[dict] = []
    for rb_name, rb in rebuilt.items():
        hint = REBUILT_TO_ORIGINAL.get(rb_name)
        orig = None
        source = "none"
        if hint and hint in originals:
            orig = originals[hint]
            source = "hint"
        if orig is None:
            best = (0.0, None)
            for o in originals.values():
                s = jaccard(rb["doc_shings"], o["doc_shings"])
                if s > best[0]:
                    best = (s, o)
            if best[1] is not None and best[0] >= 0.05:
                orig = best[1]
                source = f"shingle ({best[0]:.2f})"
        if orig is not None:
            used_orig.add(orig["name"])
        pairings.append({"rebuilt": rb, "original": orig, "source": source})

    pair_details: list[dict] = []
    for p in pairings:
        rb = p["rebuilt"]
        orig = p["original"]
        if orig is None:
            pair_details.append({"pairing": p, "note": "NO MATCH"})
            continue
        doc_j = jaccard(rb["doc_shings"], orig["doc_shings"])
        orig_shings_per_sent = [shingles(s) for s in orig["sentences"]]
        rb_shings_per_sent = [shingles(s) for s in rb["sentences"]]

        missing: list[tuple[float, str]] = []
        for s, sh in zip(orig["sentences"], orig_shings_per_sent):
            if not sh:
                continue
            best = 0.0
            for rsh in rb_shings_per_sent:
                j = jaccard(sh, rsh)
                if j > best:
                    best = j
                    if j >= 0.4:
                        break
            if best < 0.30:
                missing.append((round(best, 2), s))

        fabricated: list[tuple[float, str]] = []
        for s, sh in zip(rb["sentences"], rb_shings_per_sent):
            if not sh:
                continue
            best = 0.0
            for osh in orig_shings_per_sent:
                j = jaccard(sh, osh)
                if j > best:
                    best = j
                    if j >= 0.4:
                        break
            if best < 0.20:
                fabricated.append((round(best, 2), s))

        covered_sents = sum(
            1
            for sh in orig_shings_per_sent
            if sh and any(jaccard(sh, rsh) >= 0.30 for rsh in rb_shings_per_sent)
        )
        sent_coverage = covered_sents / max(1, sum(1 for sh in orig_shings_per_sent if sh))

        sec_hit, sec_total, sec_missing = section_coverage(orig["sections"], rb["text"])

        pair_details.append(
            {
                "pairing": p,
                "doc_jaccard": doc_j,
                "sent_coverage": sent_coverage,
                "missing": missing,
                "fabricated": fabricated,
                "sec_hit": sec_hit,
                "sec_total": sec_total,
                "sec_missing": sec_missing,
                "expansion": rb["words"] / max(1, orig["words"]),
            }
        )

    orphan_originals = [o for n, o in originals.items() if n not in used_orig]

    matched = [pd for pd in pair_details if "sent_coverage" in pd]
    avg_cov = sum(pd["sent_coverage"] for pd in matched) / max(1, len(matched))
    high_expansion = [pd for pd in matched if pd["expansion"] > 1.5]
    low_coverage = [pd for pd in matched if pd["sent_coverage"] < 0.40]

    out: list[str] = []
    out.append("# K0BG.com: Common-Crawl recovery vs FixInProduction/k0bg-rebuilt audit")
    out.append("")
    out.append("## Top-line numbers")
    out.append("")
    out.append(f"- Recovered originals (>= 100 words): **{len(originals)}**")
    out.append(f"- Mapped rebuilt articles: **{len(matched)} / {len(rebuilt_files)}**")
    out.append(f"- Mean sentence coverage across mapped pairs: **{avg_cov:.0%}**")
    out.append(f"- Articles with sentence coverage < 40%: **{len(low_coverage)}**")
    out.append(f"- Articles with expansion > 1.5x (rebuild much larger than original): **{len(high_expansion)}**")
    out.append(f"- Orphan originals (recovered but not mapped to any rebuilt page): **{len(orphan_originals)}**")
    out.append("")
    out.append("## How to read this audit")
    out.append("")
    out.append(
        "**Original source:** 49 Common Crawl crawls (2008-2026), 4,953 raw index rows -> "
        f"**{len(originals)} unique HTML articles >= 100 words** after canonicalisation. "
        "The Wayback Machine has zero captures of k0bg.com because the site historically blocked "
        "the IA crawler; Common Crawl is the only large-scale archive that holds the real content."
    )
    out.append("")
    out.append(
        "**Candidate under test:** [`FixInProduction/k0bg-rebuilt`]"
        f"(https://github.com/FixInProduction/k0bg-rebuilt) ({len(rebuilt_files)} articles in `articles/`)."
    )
    out.append("")
    out.append("Per mapped pair we compute:")
    out.append("")
    out.append("- **Doc Jaccard** - 5-gram document shingle overlap.")
    out.append("- **Sentence coverage** - fraction of original sentences with a 6-gram Jaccard >= 0.30 echo in the rebuild.")
    out.append("- **Section coverage** - fraction of original `Contents: A ; B ; C` headings whose meaningful tokens all appear in the rebuild's prose.")
    out.append("- **Expansion** - rebuild words / original words. Values >> 1 indicate the rebuild added prose with no source. Values < 1 indicate the rebuild dropped material.")
    out.append("- **Missing sentences** / **candidate fabrications** - sentence-level lists for spot inspection.")
    out.append("")
    out.append("> WARNING: None of these metrics replace a human read-through. They surface where to look first.")
    out.append("")

    out.append("## 1. Article mapping and high-level scores")
    out.append("")
    out.append("| Rebuilt article | Original | Doc J | Sent cov | Section cov | Expansion | Rebuilt words | Original words |")
    out.append("|---|---|---:|---:|---:|---:|---:|---:|")
    for pd in pair_details:
        p = pd["pairing"]
        rb = p["rebuilt"]
        orig = p["original"]
        if orig is None:
            out.append(
                f"| `{rb['name']}` | _(no original)_ | - | - | - | - | {rb['words']} | - |"
            )
        else:
            sec_frac = f"{pd['sec_hit']}/{pd['sec_total']}" if pd["sec_total"] else "-"
            out.append(
                f"| `{rb['name']}` | `{orig['name']}` | {pd['doc_jaccard']:.2f} | "
                f"{pd['sent_coverage']:.0%} | {sec_frac} | {pd['expansion']:.2f}x | "
                f"{rb['words']} | {orig['words']} |"
            )
    out.append("")

    detailed = sorted(
        [pd for pd in pair_details if "sent_coverage" in pd],
        key=lambda x: (x["sent_coverage"], -len(x["fabricated"])),
    )

    out.append("## 2. Per-article detail (most divergent first)")
    out.append("")
    for pd in detailed:
        p = pd["pairing"]
        rb = p["rebuilt"]
        orig = p["original"]
        out.append(f"### `{rb['name']}` <- `{orig['name']}`")
        out.append("")
        sec_frac = f"{pd['sec_hit']}/{pd['sec_total']}" if pd["sec_total"] else "-"
        out.append(
            f"- Doc Jaccard **{pd['doc_jaccard']:.2f}** | "
            f"sentence coverage **{pd['sent_coverage']:.0%}** | "
            f"section coverage **{sec_frac}** | "
            f"expansion **{pd['expansion']:.2f}x** "
            f"({rb['words']} rebuilt words vs {orig['words']} original)"
        )
        out.append(f"- Original title: {orig['title']!r}")
        out.append(f"- Rebuild title:  {rb['title']!r}")
        if pd["sec_missing"]:
            shown = ", ".join(f"`{s}`" for s in pd["sec_missing"][:12])
            extra = " ..." if len(pd["sec_missing"]) > 12 else ""
            out.append(
                f"- **Section headings from original missing from rebuild** "
                f"({len(pd['sec_missing'])}): {shown}{extra}"
            )
        if pd["missing"]:
            out.append("")
            out.append(
                f"**Original sentences absent from rebuild** "
                f"(showing up to 8 of {len(pd['missing'])}):"
            )
            out.append("")
            for jscore, s in pd["missing"][:8]:
                out.append(f"  - (J={jscore}) {s}")
        if pd["fabricated"]:
            out.append("")
            out.append(
                f"**Rebuild sentences not traceable to original** "
                f"(showing up to 8 of {len(pd['fabricated'])}):"
            )
            out.append("")
            for jscore, s in pd["fabricated"][:8]:
                out.append(f"  - (J={jscore}) {s}")
        out.append("")

    out.append("## 3. Recovered originals with no rebuilt counterpart")
    out.append("")
    out.append(
        "These >= 100-word pages exist in the Common Crawl recovery but no rebuilt "
        "article maps to them. They are content the rebuild dropped, merged into another "
        "article, or never had at all (biography, links, gallery pages, older sub-articles, "
        "image collections, etc.). Many are genuine Alan Applegate prose worth resurrecting."
    )
    out.append("")
    out.append("| Original | Words | Title |")
    out.append("|---|---:|---|")
    for o in sorted(orphan_originals, key=lambda x: -x["words"]):
        title = (o["title"] or "").replace("|", "\\|")[:80]
        out.append(f"| `{o['name']}` | {o['words']} | {title} |")
    out.append("")

    out.append("## 4. Rebuilt articles with no recovered original")
    out.append("")
    weak = [pd for pd in pair_details if pd["pairing"]["original"] is None]
    if weak:
        out.append(
            "These rebuilt articles have no Common Crawl original to verify against. "
            "They are the most likely to contain unverifiable / AI-generated content."
        )
        out.append("")
        out.append("| Rebuilt article | Title | Words |")
        out.append("|---|---|---:|")
        for pd in weak:
            rb = pd["pairing"]["rebuilt"]
            out.append(f"| `{rb['name']}` | {rb['title']} | {rb['words']} |")
    else:
        out.append("_(none - every rebuilt article was mapped to an original)_")
    out.append("")

    out.append("## 5. Spot checks against the rebuild's own AUDIT.md")
    out.append("")
    audit_md_path = REBUILT_DIR / "AUDIT.md"
    audit_md = read_text(audit_md_path) if audit_md_path.exists() else ""

    coil_pd = next(
        (pd for pd in pair_details if pd["pairing"]["rebuilt"]["name"] == "coil-adjustment.html"),
        None,
    )
    out.append("### 5a. `coil-adjustment.html` - rebuild AUDIT.md flagged this as fully AI-generated")
    out.append("")
    if coil_pd and "sent_coverage" in coil_pd:
        out.append(
            f"- Doc Jaccard **{coil_pd['doc_jaccard']:.2f}** | "
            f"sentence coverage **{coil_pd['sent_coverage']:.0%}** | "
            f"expansion **{coil_pd['expansion']:.2f}x** "
            f"({coil_pd['pairing']['rebuilt']['words']} rebuilt words vs "
            f"{coil_pd['pairing']['original']['words']} original)"
        )
        if coil_pd["sent_coverage"] < 0.10 and coil_pd["expansion"] > 1.5:
            verdict = (
                "**CONFIRMED.** Coverage is essentially nil and the rebuild is "
                f"{coil_pd['expansion']:.1f}x longer than the original. The bulk of the "
                "rebuilt coil-adjustment text is not traceable to the recovered `coil.html`. "
                "Treat its measurements and procedures as fabricated."
            )
        elif coil_pd["sent_coverage"] < 0.30:
            verdict = (
                "**LARGELY CONFIRMED.** Very low sentence coverage means most rebuild prose is "
                "paraphrased or invented; verify every numeric claim against the recovered original."
            )
        else:
            verdict = (
                "**PARTIALLY REFUTED.** Some coverage of the original is detectable; "
                "spot-check the unique numeric claims."
            )
        out.append("")
        out.append(verdict)
    else:
        out.append("_(coil-adjustment pairing missing)_")
    out.append("")

    out.append("### 5b. `glossary.html` - rebuild AUDIT.md noted missing 'Strapping' entry")
    out.append("")
    orig_g = originals.get("glossary.html")
    rb_g = rebuilt.get("glossary.html")
    if orig_g and rb_g:
        orig_has = "strapping" in orig_g["text"].lower()
        rb_has = "strapping" in rb_g["text"].lower()
        out.append(f"- Original glossary contains 'Strapping': **{orig_has}**")
        out.append(f"- Rebuild glossary contains 'Strapping': **{rb_has}**")
        if orig_has and not rb_has:
            text = orig_g["text"]
            i = text.lower().find("strapping")
            ctx = text[max(0, i - 200) : i + 400]
            out.append("")
            out.append("Original context:")
            out.append("")
            out.append("> " + ctx.replace("\n", " "))
    else:
        out.append("_(glossary file missing from one side)_")
    out.append("")

    out.append("## 6. Rebuild's AUDIT.md (verbatim)")
    out.append("")
    out.append("```")
    out.append(audit_md.strip())
    out.append("```")

    REPORT_PATH.write_text("\n".join(out), encoding="utf-8")
    print(f"wrote {REPORT_PATH}")
    print(f"  rebuilt articles: {len(rebuilt_files)}")
    print(f"  originals  (>=100 words): {len(originals)}")
    print(f"  pairs with matched original: {len(matched)}")
    print(f"  orphan originals: {len(orphan_originals)}")
    print(f"  mean sentence coverage: {avg_cov:.0%}")
    print(f"  high-expansion pairs (>1.5x): {len(high_expansion)}")
    print(f"  low-coverage pairs (<40%): {len(low_coverage)}")


if __name__ == "__main__":
    main()
