"""Post-merge HTML layout fixer for K0BG recovery.

Common-Crawl-captured HTML has three structural quirks that hurt rendering:

1. The provenance banner injected by ``splice_assets.py`` ends up *before*
   ``<!DOCTYPE>`` / ``<html>`` because the original HTML starts right at the
   ``<!DOCTYPE>``. Browsers tolerate this but render it as pre-doc content.

2. None of the recovered pages have a ``<body>`` tag. Browsers auto-insert
   one, but that means the banner is in head territory until <body> implicitly
   opens.

3. ``index.html`` (and ``error.html``) have broken div nesting: ``</div>``
   closes ``.container`` immediately after ``.header`` and ``.sidebar1`` is
   left as a sibling of ``.container`` instead of a child. This makes the
   sidebar float against the viewport-left.

This script normalizes all merged HTML in place so the banner sits inside
``<body>`` and so the container actually contains the sidebar.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "recovered" / "k0bg.com"
BANNER_RE = re.compile(
    r"<!--\s*KOBG_PROVENANCE_BANNER_START\s*-->.*?<!--\s*KOBG_PROVENANCE_BANNER_END\s*-->",
    re.DOTALL,
)


def relocate_banner(text: str) -> str:
    """Move the banner block to just after the (possibly inserted) <body> tag."""
    m = BANNER_RE.search(text)
    if not m:
        return text
    banner = m.group(0)
    text = BANNER_RE.sub("", text, count=1)

    if re.search(r"<body\b[^>]*>", text, re.IGNORECASE):
        return re.sub(
            r"(<body\b[^>]*>)",
            lambda mm: mm.group(1) + banner,
            text,
            count=1,
            flags=re.IGNORECASE,
        )
    if re.search(r"</head>", text, re.IGNORECASE):
        return re.sub(
            r"(</head>)",
            lambda mm: mm.group(1) + "<body>" + banner,
            text,
            count=1,
            flags=re.IGNORECASE,
        )
    if re.search(r"<html\b[^>]*>", text, re.IGNORECASE):
        return re.sub(
            r"(<html\b[^>]*>)",
            lambda mm: mm.group(1) + "<body>" + banner,
            text,
            count=1,
            flags=re.IGNORECASE,
        )
    return banner + text


def ensure_body_close(text: str) -> str:
    """If <body> was opened but </body> is missing, close it before </html>."""
    if "<body" not in text.lower():
        return text
    if "</body" in text.lower():
        return text
    if re.search(r"</html>", text, re.IGNORECASE):
        return re.sub(r"</html>", "</body></html>", text, count=1, flags=re.IGNORECASE)
    return text + "</body>"


def fix_container_nesting(text: str) -> str:
    """For pages where .sidebar1 is a sibling of .container, wrap it inside.

    Pattern in source:
        <div class="container">
          <div class="header"> ... </div>
        </div>                                  <-- container closes too early
        <div class="sidebar1"> ... </div>
        [possibly more siblings]
        </html>

    Target:
        <div class="container">
          <div class="header"> ... </div>
          <div class="sidebar1"> ... </div>
        </div>
    """
    # Only touch documents that actually have both .container and .sidebar1
    if 'class="container"' not in text or 'class="sidebar1"' not in text:
        return text

    # Find the closing </div> that ends .container, just before <div class="sidebar1">
    # (allow whitespace/newlines between)
    pattern = re.compile(
        r'(</div>)(\s*)(<div\s+class="sidebar1")',
        re.IGNORECASE,
    )
    m = pattern.search(text)
    if not m:
        return text
    # Drop that </div> so .sidebar1 is now nested inside .container
    fixed = text[: m.start(1)] + m.group(2) + m.group(3) + text[m.end(3):]

    # Now we need to add a </div> back at the end to close .container.
    # Insert it just before </html> (or append if missing).
    if re.search(r"</html>", fixed, re.IGNORECASE):
        fixed = re.sub(r"</html>", "</div></html>", fixed, count=1, flags=re.IGNORECASE)
    else:
        fixed = fixed + "</div>"
    return fixed


def trim_homepage_to_sep2022(text: str) -> str:
    """Remove content that was not on the home page as captured in Sep 2022.

    The K0BG.COM.pdf (iOS Safari capture, Sep 2022) is our most recent
    ground-truth snapshot of the home page. Its right-column content ends
    at "Established April, 27, 2004".

    Common Crawl, however, captured an earlier version of the home page that
    also contained a "Hosted by iPower / Logo Artwork by Mark Myers / Please
    Support Our Troops / [Flag Troop image]" block. Alan removed that block
    before the site went down, so it is not part of the page we are
    recovering. Additionally, the Flag Troop image (images/troop.jpg) was
    never captured by any PDF or by Common Crawl, so it cannot be sourced.

    Trim from immediately after "Established April, 27, 2004" up to (but not
    including) the closing </div> of the .header content column (signalled
    by the start of <div class="sidebar1">).
    """
    pattern = re.compile(
        r'(Established April,\s*27,\s*2004\s*)'
        r'.*?'
        r'(\s*</div>\s*<div\s+class="sidebar1")',
        re.DOTALL | re.IGNORECASE,
    )
    return pattern.sub(r"\1\2", text)


def fix_one(path: Path) -> dict:
    src = path.read_text(encoding="utf-8", errors="replace")
    out = src
    out = relocate_banner(out)
    out = fix_container_nesting(out)
    if path.name == "index.html":
        out = trim_homepage_to_sep2022(out)
    out = ensure_body_close(out)
    if out != src:
        path.write_text(out, encoding="utf-8")
        return {"file": path.name, "changed": True}
    return {"file": path.name, "changed": False}


def main() -> None:
    files = [p for p in ROOT.glob("*.html") if not p.name.endswith(".cc-original.html")]
    changed = 0
    for p in sorted(files):
        r = fix_one(p)
        if r["changed"]:
            changed += 1
            print(f"  fixed {r['file']}")
    print(f"\nfixed {changed} / {len(files)} HTML files")


if __name__ == "__main__":
    main()
