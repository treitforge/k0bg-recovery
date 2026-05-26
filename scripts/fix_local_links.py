"""Rewrite hard-coded k0bg.com URLs in the recovered site so they resolve locally.

The recovered HTML contains hundreds of absolute URLs back to the defunct
k0bg.com domain - article-to-article links, image click-to-enlarge anchors,
the "Home" link, etc. After this script runs, all of those become relative
paths that resolve against the locally-hosted copy.

Examples of rewrites:
  http://www.k0bg.com/                       -> index.html
  http://www.k0bg.com/options.html           -> options.html
  http://www.k0bg.com/images/amp/sg500.jpg   -> images/amp/sg500.jpg
  //images/otr/K5HAB1.jpg                    -> images/otr/K5HAB1.jpg

If a target file doesn't exist locally, the rewritten URL still 404s, but
at least it stays same-origin and consistent with the rest of the recovered
content - it never bounces visitors to the defunct domain.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


KOBG_HOST = re.compile(r'https?://(?:www\.)?k0bg\.com(/[^"\'\s>)]*)?', re.IGNORECASE)
PROTOCOL_RELATIVE_IMAGES = re.compile(r'(?<=["\'\s])//images/')


def rewrite_text(text: str) -> tuple[str, int]:
    count = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal count
        count += 1
        path = m.group(1) or ""
        path = path.lstrip("/")
        if not path:
            return "index.html"
        return path

    text = KOBG_HOST.sub(repl, text)
    new_text, n_proto = PROTOCOL_RELATIVE_IMAGES.subn("images/", text)
    return new_text, count + n_proto


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("site/k0bg.com"),
        help="Directory containing the recovered HTML files.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report what would be rewritten without writing files.",
    )
    args = parser.parse_args()

    root: Path = args.root
    if not root.is_dir():
        print(f"error: --root {root} is not a directory", file=sys.stderr)
        return 2

    html_files = sorted(root.glob("*.html"))
    total_rewrites = 0
    touched_files = 0
    for path in html_files:
        original = path.read_text(encoding="utf-8", errors="replace")
        rewritten, n = rewrite_text(original)
        if n == 0:
            continue
        total_rewrites += n
        touched_files += 1
        if args.dry_run:
            print(f"  [dry-run] {path.name}: {n} rewrites")
        else:
            path.write_text(rewritten, encoding="utf-8")
            print(f"  {path.name}: {n} rewrites")

    print(
        f"\n{'(dry-run) ' if args.dry_run else ''}"
        f"Rewrote {total_rewrites} k0bg.com URLs across {touched_files} files "
        f"(scanned {len(html_files)} HTML files in {root})."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
