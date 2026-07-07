# Portfolio assets

**Manifest:** [`draft/image-manifest.md`](../../draft/image-manifest.md) — every image, narrative beat, Figma source, redaction note.

## Drop PNG exports here

Export from `Portfolio 2026.fig` at **2× PNG**. Use the exact filename from the manifest (e.g. `firefox/overview.png`). The site uses `<picture>` — PNG replaces SVG placeholder automatically.

## Regenerate SVG placeholders

```bash
python3 site/scripts/generate-placeholders.py
```

## 30-minute sprint order

1. `cover-hello.png` + `firefox/overview.png` + `firefox/pillars.png`
2. `venmo/cover.png` + `venmo/gap-matrix.png` + `venmo/vision-anywhere.png`
3. Remaining Figma slides from manifest
4. `firefox/nightly/*.png` from Nightly captures
