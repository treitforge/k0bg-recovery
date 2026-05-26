"""Recover k0bg.com pages from Common Crawl WARC chunks.

Reads every cc-index/*.jsonl file, picks the freshest 200-status capture per
canonical URL, then range-fetches the WARC chunk from data.commoncrawl.org,
gunzips the outer WARC framing, strips the inner HTTP response headers, decodes
any inner Content-Encoding, and writes the body to recovered/<path>.

Writes recovered/_manifest.json mapping each output file to its source crawl,
timestamp, and digest.
"""

from __future__ import annotations

import concurrent.futures as cf
import gzip
import io
import json
import os
import re
import sys
import time
import zlib
from pathlib import Path
from urllib.parse import urlparse

import requests

HERE = Path(__file__).resolve().parent
INDEX_DIR = HERE / "cc-index"
OUT_DIR = HERE / "recovered"
MANIFEST_PATH = OUT_DIR / "_manifest.json"

ACCEPT_MIME_PREFIXES = ("text/html", "text/plain", "application/pdf", "image/")
USER_AGENT = "k0bg-recovery/1.0 (research; contact via github.com/treitforge)"
MAX_WORKERS = 6
RETRIES = 4


def load_records():
    for path in sorted(INDEX_DIR.glob("*.jsonl")):
        with path.open("r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line or not line.startswith("{"):
                    continue
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue


def canonical_key(url: str) -> str | None:
    try:
        p = urlparse(url)
    except ValueError:
        return None
    host = p.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    if not host.endswith("k0bg.com"):
        return None
    path = p.path or "/"
    if path == "":
        path = "/"
    return f"{host}{path}"


def pick_freshest(records):
    best: dict[str, dict] = {}
    for rec in records:
        if rec.get("status") != "200":
            continue
        mime = (rec.get("mime-detected") or rec.get("mime") or "").lower()
        if not any(mime.startswith(p) for p in ACCEPT_MIME_PREFIXES):
            continue
        url = rec.get("url")
        key = canonical_key(url)
        if key is None:
            continue
        ts = rec.get("timestamp", "")
        cur = best.get(key)
        if cur is None or ts > cur.get("timestamp", ""):
            best[key] = rec
    return best


def safe_output_path(key: str) -> Path:
    host, sep, path = key.partition("/")
    if path in ("", "/"):
        rel = Path("k0bg.com") / "index.html"
    else:
        # strip any query (the index strips it already, but be defensive)
        path = path.split("?", 1)[0]
        # ban traversal
        parts = [p for p in path.split("/") if p not in ("", ".", "..")]
        rel = Path("k0bg.com").joinpath(*parts) if parts else Path("k0bg.com/index.html")
        if not rel.suffix and parts:
            rel = rel / "index.html"
    return OUT_DIR / rel


def split_http(blob: bytes) -> tuple[dict[str, str], bytes]:
    # Find end of HTTP response headers
    sep = blob.find(b"\r\n\r\n")
    if sep == -1:
        return {}, blob
    head = blob[:sep].decode("latin-1", errors="replace")
    body = blob[sep + 4 :]
    headers: dict[str, str] = {}
    lines = head.split("\r\n")
    for ln in lines[1:]:
        if ":" in ln:
            k, _, v = ln.partition(":")
            headers[k.strip().lower()] = v.strip()
    return headers, body


def maybe_decode_chunked(body: bytes) -> bytes:
    out = bytearray()
    i = 0
    while i < len(body):
        nl = body.find(b"\r\n", i)
        if nl == -1:
            return bytes(out) + body[i:]
        try:
            size = int(body[i:nl].split(b";", 1)[0].strip(), 16)
        except ValueError:
            return bytes(out) + body[i:]
        i = nl + 2
        if size == 0:
            return bytes(out)
        out.extend(body[i : i + size])
        i += size + 2
    return bytes(out)


def decompress_body(headers: dict[str, str], body: bytes) -> bytes:
    if headers.get("transfer-encoding", "").lower() == "chunked":
        body = maybe_decode_chunked(body)
    enc = headers.get("content-encoding", "").lower()
    try:
        if enc == "gzip":
            body = gzip.decompress(body)
        elif enc == "deflate":
            try:
                body = zlib.decompress(body)
            except zlib.error:
                body = zlib.decompress(body, -zlib.MAX_WBITS)
    except Exception:
        pass
    return body


def split_warc(blob: bytes) -> bytes:
    # The WARC chunk holds: WARC headers \r\n\r\n  HTTP response  \r\n\r\n
    # We split on the first \r\n\r\n to skip WARC headers.
    sep = blob.find(b"\r\n\r\n")
    if sep == -1:
        return blob
    return blob[sep + 4 :]


def fetch_one(session: requests.Session, rec: dict) -> dict:
    filename = rec["filename"]
    offset = int(rec["offset"])
    length = int(rec["length"])
    url_full = f"https://data.commoncrawl.org/{filename}"
    headers = {
        "User-Agent": USER_AGENT,
        "Range": f"bytes={offset}-{offset + length - 1}",
    }
    last_err = None
    for attempt in range(RETRIES):
        try:
            resp = session.get(url_full, headers=headers, timeout=60)
            if resp.status_code in (200, 206):
                raw = resp.content
                try:
                    decompressed = gzip.decompress(raw)
                except OSError:
                    decompressed = raw
                http_blob = split_warc(decompressed)
                hh, body = split_http(http_blob)
                body = decompress_body(hh, body)
                return {"ok": True, "rec": rec, "headers": hh, "body": body}
            last_err = f"http {resp.status_code}"
        except Exception as exc:
            last_err = repr(exc)
        time.sleep(1.5 * (attempt + 1))
    return {"ok": False, "rec": rec, "error": last_err}


def main():
    print(f"loading index files from {INDEX_DIR}")
    records = list(load_records())
    print(f"  raw records: {len(records)}")
    best = pick_freshest(records)
    print(f"  unique canonical URLs (200/html|txt|pdf|img): {len(best)}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Optional limit via CLI arg
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    items = sorted(best.items())
    if limit > 0:
        items = items[:limit]
        print(f"  limiting to first {limit}")

    manifest: dict[str, dict] = {}
    failures: list[dict] = []

    with requests.Session() as sess, cf.ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {pool.submit(fetch_one, sess, rec): key for key, rec in items}
        done = 0
        for fut in cf.as_completed(futures):
            done += 1
            key = futures[fut]
            res = fut.result()
            rec = res["rec"]
            if not res.get("ok"):
                failures.append({"key": key, "error": res.get("error"), "filename": rec.get("filename")})
                if done % 25 == 0 or done == len(futures):
                    print(f"  [{done}/{len(futures)}] (FAIL) {key}: {res.get('error')}")
                continue
            body = res["body"]
            if not body:
                failures.append({"key": key, "error": "empty body", "filename": rec.get("filename")})
                continue
            out_path = safe_output_path(key)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_bytes(body)
            mime = (rec.get("mime-detected") or rec.get("mime") or "").lower()
            manifest[str(out_path.relative_to(OUT_DIR)).replace(os.sep, "/")] = {
                "url": rec.get("url"),
                "crawl": rec.get("filename", "").split("/")[1] if rec.get("filename") else None,
                "timestamp": rec.get("timestamp"),
                "mime": mime,
                "digest": rec.get("digest"),
                "length": rec.get("length"),
                "filename": rec.get("filename"),
                "offset": rec.get("offset"),
                "bytes_written": len(body),
            }
            if done % 25 == 0 or done == len(futures):
                print(f"  [{done}/{len(futures)}] wrote {out_path.relative_to(HERE)} ({len(body)} bytes)")

    MANIFEST_PATH.write_text(
        json.dumps(
            {"recovered": manifest, "failures": failures, "total_unique_urls": len(best)},
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    print(f"wrote manifest: {MANIFEST_PATH} ({len(manifest)} recovered, {len(failures)} failed)")


if __name__ == "__main__":
    main()
