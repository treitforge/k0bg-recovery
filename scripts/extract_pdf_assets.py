"""Extract embedded images + hyperlinks from rebuilt/PDF/*.pdf.

For each Foo.pdf:
  - extracts every image with pypdf.PageObject.images
  - saves to recovered/k0bg.com/_pdf_assets/<slug>/p<N>_<idx>.<ext>
  - writes manifest.json with per-image position and per-page outbound URLs

The slug matches the convention used in make_browse.py so HTML splicing can join on it.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

from pypdf import PdfReader
from pypdf.generic import ArrayObject, DictionaryObject, IndirectObject

ROOT = Path(__file__).resolve().parent
PDF_DIR = ROOT / "rebuilt" / "PDF"
OUT_DIR = ROOT / "recovered" / "k0bg.com" / "_pdf_assets"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def slugify(name: str) -> str:
    s = name.lower()
    s = re.sub(r"&", " and ", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def collect_page_uris(page) -> list[str]:
    uris: list[str] = []
    annots = page.get("/Annots")
    if not annots:
        return uris
    if isinstance(annots, IndirectObject):
        annots = annots.get_object()
    if not isinstance(annots, (list, ArrayObject)):
        return uris
    for a in annots:
        try:
            obj = a.get_object() if isinstance(a, IndirectObject) else a
        except Exception:
            continue
        if not isinstance(obj, DictionaryObject):
            continue
        action = obj.get("/A")
        if isinstance(action, IndirectObject):
            try:
                action = action.get_object()
            except Exception:
                action = None
        if isinstance(action, DictionaryObject):
            uri = action.get("/URI")
            if uri:
                try:
                    uris.append(str(uri))
                except Exception:
                    pass
    return uris


def extract_one(pdf_path: Path) -> dict:
    name = pdf_path.stem
    slug = slugify(name)
    target = OUT_DIR / slug
    target.mkdir(parents=True, exist_ok=True)

    reader = PdfReader(str(pdf_path))
    pages_meta = []
    seen_hashes: dict[str, str] = {}
    total_images = 0
    total_unique = 0

    for page_idx, page in enumerate(reader.pages, start=1):
        page_imgs = []
        try:
            images = list(page.images)
        except Exception as e:  # noqa: BLE001
            images = []
            print(f"  ! page {page_idx} image enum failed: {e}", file=sys.stderr)
        for img_idx, img in enumerate(images):
            data = img.data
            h = hashlib.sha1(data).hexdigest()[:12]
            total_images += 1
            ext = (img.name.rsplit(".", 1)[-1] if "." in img.name else "img").lower()
            if ext not in ("jpg", "jpeg", "png", "gif", "tif", "tiff", "bmp"):
                ext = "img"
            if h in seen_hashes:
                # duplicate – just record reference
                page_imgs.append(
                    {"index": img_idx, "file": seen_hashes[h], "sha1_12": h, "duplicate": True}
                )
                continue
            fname = f"p{page_idx:02d}_{img_idx:02d}_{h}.{ext}"
            (target / fname).write_bytes(data)
            seen_hashes[h] = fname
            total_unique += 1
            page_imgs.append(
                {"index": img_idx, "file": fname, "sha1_12": h, "bytes": len(data)}
            )
        uris = collect_page_uris(page)
        pages_meta.append({"page": page_idx, "images": page_imgs, "uris": uris})

    manifest = {
        "pdf": pdf_path.name,
        "slug": slug,
        "page_count": len(reader.pages),
        "total_images": total_images,
        "unique_images": total_unique,
        "pages": pages_meta,
    }
    (target / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    return manifest


def main() -> int:
    pdfs = sorted(PDF_DIR.glob("*.pdf"))
    if not pdfs:
        print("no PDFs found", file=sys.stderr)
        return 1
    rollup = []
    for i, p in enumerate(pdfs, start=1):
        print(f"[{i}/{len(pdfs)}] {p.name}", flush=True)
        try:
            m = extract_one(p)
        except Exception as e:  # noqa: BLE001
            print(f"  ! failed: {e}", file=sys.stderr)
            continue
        rollup.append(
            {
                "pdf": m["pdf"],
                "slug": m["slug"],
                "pages": m["page_count"],
                "images_total": m["total_images"],
                "images_unique": m["unique_images"],
                "uris_total": sum(len(p["uris"]) for p in m["pages"]),
            }
        )
    (OUT_DIR / "rollup.json").write_text(
        json.dumps(rollup, indent=2), encoding="utf-8"
    )
    print()
    print("=== rollup ===")
    print(
        f"{len(rollup)} PDFs, "
        f"{sum(r['images_total'] for r in rollup)} images "
        f"({sum(r['images_unique'] for r in rollup)} unique), "
        f"{sum(r['uris_total'] for r in rollup)} URIs"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
