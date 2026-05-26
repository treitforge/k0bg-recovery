# K0BG.COM Recovery

A community reconstruction of Alan Applegate's (K0BG) **K0BG.COM** mobile HF amateur radio reference site, rebuilt from public archival sources after the original site went offline in 2022.

**Live mirror:** <https://rtreit.com/k0bg-com/>
**About / methodology / disclaimer:** <https://rtreit.com/k0bg-com/about-reconstruction.html>

> This project has **no affiliation** with Alan Applegate or his family. It is preserved here by Randy Treit (KC7AVA) as a courtesy to fellow hams. If Alan or anyone authorized to represent the original work would like the recovered content taken down or hosted elsewhere, please [open an issue](https://github.com/treitforge/k0bg-recovery/issues/new) or email `randyt@outlook.com` and it will be removed immediately.

## What's in here

```
site/k0bg.com/      Recovered, navigable HTML site (open index.html in a browser)
  _pdf/             Original Sep 2022 iOS Safari "Save to Dropbox" PDF captures (43 files)
  _pdf_assets/      Per-article images extracted from the PDFs
  images/           Site images recovered from the PDF cache, mapped to original paths
  twoColLiqLtHdr.css   Faithful reconstruction of Alan's Dreamweaver CS3 stylesheet
  *.html            One file per recovered article (84 pages total)
  about-reconstruction.html   Methodology + disclaimer page (used by the live mirror)

scripts/            The recovery pipeline (Python 3)
  recover.py                Common Crawl CDX index harvester
  recover_images.py         Deep CDX scan for missing image assets
  extract_pdf_assets.py     Extract images & links from each PDF using pdfminer/pdfium
  splice_assets.py          Merge PDF-extracted assets into per-article HTML pages
  merge_images.py           First-pass image merge (legacy)
  merge_images_v2.py        Hungarian aspect-ratio image matcher (current pipeline driver)
  fix_layout.py             Post-merge HTML structure fixer
                            (banner placement, body close, container nesting, Sep-2022 trim)
  make_browse.py            Generate _browse.html debug index
  audit.py                  Compare recovered output against external reconstructions
  wb_sample.py              Wayback Machine sampling helper

AUDIT-vs-rebuilt.md  Comparison against the FixInProduction/k0bg-rebuilt PDF-only effort
LICENSE              MIT for the pipeline; recovered content stays Alan's IP
```

## How it was rebuilt

1. **HTML text** was harvested from [Common Crawl](https://commoncrawl.org/) CDX captures across multiple years (2008–2025). Common Crawl was the only public archive with substantive coverage — k0bg.com had blocked the Wayback Machine via `robots.txt`.
2. **Images** were extracted from a 43-PDF archival capture of the live site (iOS 15.7 Safari, 30 Sep 2022 per the embedded PDF metadata). I did not capture these PDFs myself — I obtained them from the [`PDF/` directory of FixInProduction/k0bg-rebuilt](https://github.com/FixInProduction/k0bg-rebuilt/tree/main/PDF), where they are bundled as part of that project. They are reproduced under `site/k0bg.com/_pdf/` here for convenience. Images were then matched back into the corresponding HTML pages using the Hungarian algorithm on aspect ratios.
3. **CSS** was reconstructed from scratch. Common Crawl does not capture CSS responses and Wayback had zero captures, so `twoColLiqLtHdr.css` here is a faithful rebuild of the Dreamweaver CS3 "Two-Column Liquid, Left Sidebar, Header and Footer" starter template that Alan used, tuned against the rendered September 2022 PDF.
4. **Home page layout** was visually validated page-by-page against the rendered iOS PDF until it matched.

The home page was deliberately trimmed to the September 2022 state — earlier Common Crawl captures included a "Hosted by iPower / Please Support Our Troops" footer block that Alan had already removed before the final PDF capture, and the image for that block was not preserved by any archive.

## Limitations

- The PDF cache covers 43 of the longer articles. Roughly 42 additional pages exist as recovered text only, without inline images.
- The reconstructed CSS may differ subtly from Alan's live stylesheet. No archive ever captured the original.
- A handful of older-capture images (Flag Troop sidebar, old iPower banner) are not present in any source.

## Running the pipeline

The scripts require Python 3.10+ and the packages used by `extract_pdf_assets.py` and `recover.py` (`pypdf`, `pypdfium2`, `requests`, `beautifulsoup4`). Raw inputs (Common Crawl WARC slices, the source PDF cache) are not bundled in this repo because of their size; the scripts include enough comments to retrace the process.

A typical end-to-end rebuild looks like:

```powershell
# 1. Harvest HTML from CC (writes per-capture JSONL into cc-index/)
python scripts/recover.py

# 2. Extract images from each PDF into _pdf_assets/<slug>/
python scripts/extract_pdf_assets.py

# 3. Splice PDF-extracted images into the per-page HTML
python scripts/splice_assets.py

# 4. Run the aspect-ratio image matcher + post-layout fixer
python scripts/merge_images_v2.py
```

`merge_images_v2.py` is idempotent and re-invokes `fix_layout.py` at the end of every run.

## Related

- [FixInProduction/k0bg-rebuilt](https://github.com/FixInProduction/k0bg-rebuilt) — a separate community reconstruction effort. **Credit:** the 43-PDF archival capture of the live K0BG.COM site bundled in their [`PDF/` directory](https://github.com/FixInProduction/k0bg-rebuilt/tree/main/PDF) is the source of the images used in this reconstruction (all 43 PDFs under `site/k0bg.com/_pdf/` are byte-identical to theirs). Their own text reconstruction takes a different approach — Google-cached page fragments plus community-knowledge synthesis, with explicitly added "Modern Considerations" sections — and is textually independent from the Common Crawl HTML harvested here. See `AUDIT-vs-rebuilt.md` for a sentence-level comparison against the Common Crawl originals.

## Credit

All technical content under `site/k0bg.com/` was authored by Alan Applegate, K0BG.
The recovery pipeline and this README are by Randy Treit, KC7AVA.

73 &middot; *de KC7AVA*
