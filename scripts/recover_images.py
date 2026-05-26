"""Find image URLs referenced by recovered HTML and try per-URL CC lookups.

The original broad CC index (url=k0bg.com/*) was capped at 2000 rows per crawl
and surfaced only 2 image URLs. Exact per-URL lookups may find deeper captures.
For anything found, we range-fetch the WARC chunk and write to disk under
recovered/k0bg.com/images/.
"""

from __future__ import annotations

import concurrent.futures as cf
import gzip
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import requests

HERE = Path(__file__).resolve().parent
RECOVERED_DIR = HERE / "recovered" / "k0bg.com"
CC_COLLINFO = HERE / "cc-collinfo.json"
REPORT_PATH = HERE / "images-recovery-report.json"

IMG_RE = re.compile(r"""<img[^>]+src=["']([^"']+)["']""", re.I)
HREF_RE = re.compile(r"""<a[^>]+href=["']([^"']+\.(?:jpg|jpeg|gif|png|pdf|wav|aif|mp3))["']""", re.I)
USER_AGENT = "k0bg-recovery/1.0 (+research)"
MAX_INDEX_WORKERS = 4
MAX_WARC_WORKERS = 6
RETRIES = 3


def collect_image_refs() -> set[str]:
    urls: set[str] = set()
    for html_file in RECOVERED_DIR.glob("*.html"):
        text = html_file.read_text(encoding="utf-8", errors="replace")
        for pat in (IMG_RE, HREF_RE):
            for m in pat.finditer(text):
                src = m.group(1).strip()
                if src.startswith(("data:", "javascript:", "mailto:", "#")):
                    continue
                if src.startswith("//"):
                    src = "http:" + src
                if src.startswith("/"):
                    src = "http://www.k0bg.com" + src
                if src.startswith("http"):
                    p = urlparse(src)
                    if "k0bg.com" not in p.netloc.lower():
                        continue
                else:
                    src = "http://www.k0bg.com/" + src.lstrip("./")
                urls.add(src)
    return urls


def url_to_outpath(url: str) -> Path:
    p = urlparse(url)
    path = p.path.lstrip("/")
    parts = [pp for pp in path.split("/") if pp not in ("", ".", "..")]
    if not parts:
        return RECOVERED_DIR / "index.bin"
    return RECOVERED_DIR.joinpath(*parts)


def cc_lookup_url(session: requests.Session, crawl: str, url: str) -> list[dict]:
    api = f"https://index.commoncrawl.org/{crawl}-index"
    params = {"url": url, "output": "json", "limit": "5"}
    for attempt in range(RETRIES):
        try:
            r = session.get(api, params=params, timeout=30, headers={"User-Agent": USER_AGENT})
            if r.status_code == 404:
                return []
            if r.status_code == 200:
                rows = []
                for line in r.text.splitlines():
                    line = line.strip()
                    if line.startswith("{"):
                        try:
                            rows.append(json.loads(line))
                        except json.JSONDecodeError:
                            pass
                return rows
            if r.status_code == 429:
                time.sleep(5 * (attempt + 1))
                continue
        except Exception:
            time.sleep(2 * (attempt + 1))
    return []


def split_warc_to_body(blob: bytes) -> bytes | None:
    sep = blob.find(b"\r\n\r\n")
    if sep == -1:
        return None
    http_blob = blob[sep + 4 :]
    sep2 = http_blob.find(b"\r\n\r\n")
    if sep2 == -1:
        return None
    body = http_blob[sep2 + 4 :]
    return body


def fetch_warc(session: requests.Session, rec: dict) -> bytes | None:
    filename = rec["filename"]
    offset = int(rec["offset"])
    length = int(rec["length"])
    url = f"https://data.commoncrawl.org/{filename}"
    headers = {"User-Agent": USER_AGENT, "Range": f"bytes={offset}-{offset + length - 1}"}
    for attempt in range(RETRIES):
        try:
            r = session.get(url, headers=headers, timeout=60)
            if r.status_code in (200, 206):
                raw = r.content
                try:
                    decompressed = gzip.decompress(raw)
                except OSError:
                    decompressed = raw
                body = split_warc_to_body(decompressed)
                if body:
                    return body
            if r.status_code == 429:
                time.sleep(5 * (attempt + 1))
                continue
        except Exception:
            time.sleep(2 * (attempt + 1))
    return None


def main() -> None:
    urls = sorted(collect_image_refs())
    print(f"found {len(urls)} unique k0bg.com asset references in 84 recovered HTML pages")

    # Skip ones we already have on disk
    missing = [u for u in urls if not url_to_outpath(u).exists()]
    print(f"missing locally: {len(missing)}")

    collinfo = json.loads(CC_COLLINFO.read_text(encoding="utf-8"))
    crawls = [c["id"] for c in collinfo if c["id"].startswith("CC-MAIN-")]
    # Walk newest-first; stop scanning further crawls for a URL once we have a 200.
    crawls = sorted(crawls, reverse=True)
    print(f"will scan {len(crawls)} crawls per missing URL (newest first)")

    found: dict[str, dict] = {}
    failures: list[str] = []

    def lookup_url(url: str) -> tuple[str, dict | None]:
        with requests.Session() as s:
            for crawl in crawls:
                rows = cc_lookup_url(s, crawl, url)
                hit = None
                for r in rows:
                    if r.get("status") == "200":
                        hit = r
                        break
                if hit:
                    return url, hit
        return url, None

    print("phase 1: per-URL Common Crawl index lookups ...")
    with cf.ThreadPoolExecutor(max_workers=MAX_INDEX_WORKERS) as pool:
        futures = {pool.submit(lookup_url, u): u for u in missing}
        done = 0
        for fut in cf.as_completed(futures):
            done += 1
            url, hit = fut.result()
            if hit:
                found[url] = hit
            if done % 25 == 0 or done == len(futures):
                print(f"  [{done}/{len(futures)}] lookups complete, {len(found)} hits so far")

    print(f"phase 1 done: {len(found)} of {len(missing)} URLs have a 200-status CC capture")

    if not found:
        REPORT_PATH.write_text(
            json.dumps({"total_refs": len(urls), "missing": len(missing), "found": 0, "failures": missing}, indent=2),
            encoding="utf-8",
        )
        print("nothing to fetch; wrote report.")
        return

    print("phase 2: range-fetching WARC chunks ...")
    fetched = 0
    with requests.Session() as sess, cf.ThreadPoolExecutor(max_workers=MAX_WARC_WORKERS) as pool:
        futures = {pool.submit(fetch_warc, sess, rec): url for url, rec in found.items()}
        done = 0
        for fut in cf.as_completed(futures):
            done += 1
            url = futures[fut]
            body = fut.result()
            if body is None:
                failures.append(url)
                continue
            out = url_to_outpath(url)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(body)
            fetched += 1
            if done % 25 == 0 or done == len(futures):
                print(f"  [{done}/{len(futures)}] fetched, {fetched} written")

    REPORT_PATH.write_text(
        json.dumps(
            {
                "total_refs": len(urls),
                "missing": len(missing),
                "found_in_cc": len(found),
                "fetched": fetched,
                "failures_fetching": failures,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"done: {fetched} new files written, report at {REPORT_PATH}")


if __name__ == "__main__":
    main()
