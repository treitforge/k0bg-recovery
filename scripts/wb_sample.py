"""Quick sample test: does Wayback Machine have any captures of k0bg.com inline image URLs?"""

from __future__ import annotations

import json
import random

import requests

from recover_images import collect_image_refs


def main() -> None:
    urls = sorted(collect_image_refs())
    random.seed(42)
    sample = random.sample(urls, min(20, len(urls)))
    hits = 0
    for u in sample:
        try:
            r = requests.get("https://archive.org/wayback/available", params={"url": u}, timeout=10)
            snaps = r.json().get("archived_snapshots", {})
        except Exception as e:
            print(f"  err  {u}: {e}")
            continue
        if snaps:
            hits += 1
            snap_url = list(snaps.values())[0].get("url", "")[:120]
            print(f"  HIT  {u}  ->  {snap_url}")
        else:
            print(f"  miss {u}")
    print(f"\n{hits}/{len(sample)} sample image URLs found in Wayback")


if __name__ == "__main__":
    main()
