---
name: small-image-atlas
description: Generate batches of small transparent raster assets, extract existing PNG atlases by alpha bounds, and optionally repack them with controlled gutters. Use for icons, items, tokens, stickers, UI ornaments, or independent small 2D game assets. Do not use for large scenes, hero art, or animation-frame alignment.
---

# Small Image Atlas

Deliver independently usable PNG assets with a verifiable mapping from requested items to extracted files. Keep the source atlas, deterministic crops, and an optional repack. Independent crops do not establish consistent pivots or frame alignment for animation.

## Choose the Workflow

- **New assets:** prepare an asset plan, generate a sheet, inspect it, then extract.
- **Existing atlas:** inspect the supplied source and its item order, then extract without regenerating usable artwork.
- **Repack:** extract only if needed and create a new sheet when the downstream consumer benefits from it.

Use this workflow for assets that remain legible while sharing a generation canvas. Handle large standalone artwork separately. Split a batch only when one sheet would crowd subjects or mix incompatible styles, preserving the requested count and grouping.

For generation or visual edits, use the available image-generation capability and follow its instructions; read the installed `imagegen` skill when available. If generation is unavailable, complete the plan or extract a usable supplied atlas and report the missing capability. Local extraction and repacking use the bundled script; they do not require a generation tool.

## Plan and Inspect

Before generation or extraction, record an asset plan with stable identifiers, exact count, descriptions, row-major slot order, rows/columns when applicable, canvas size, and intended output scale. For a supplied atlas, use its observed layout and verify item identities against the user's supplied names. Record intentional empty slots. Keep identifiers in the plan, not painted into the image.

Request one centered subject per equal-sized grid cell, consistent scale, viewpoint, lighting, palette, and rendering style. Require actual transparency, fully isolated silhouettes, and effects contained inside each cell. Exclude scenery, labels, grid lines, borders, and background imitations of transparency. As a starting point, reserve gutters of at least 16 px or one eighth of the intended item width, whichever is larger; increase them for soft effects and irregular silhouettes.

Inspect the full-resolution PNG against the plan before extraction: count, order, duplicates, omissions, clipping, consistency, and clear gutters. Check both that transparency is supported and that the expected background/gutters actually contain transparent pixels. An RGBA file can still have an opaque matte or painted checkerboard; the script does not detect those defects.

## Extract

Use [scripts/extract_sprite_atlas.py](scripts/extract_sprite_atlas.py) with `--expected-count` and a fresh output directory. Choose segmentation from the source layout:

| Source layout | Mode | Limitation |
| --- | --- | --- |
| Assets separated by clear horizontal bands and vertical gutters within each band | `auto` | Segments occupied bands, not semantic objects; disconnected pieces can split and narrow gutters can merge |
| Known regular grid, especially with disconnected pieces or effects inside each cell | `grid` with rows and columns | Divides the entire canvas into equal cells; cannot infer custom offsets, unequal cells, or repair a subject crossing a cell edge |

Both modes trim detected candidates to their foreground bounds. Grid mode visits cells in row-major order but skips empty or undersized cells, so an output index is not necessarily the original slot number. Compare every crop with the plan even when the count matches.

If segmentation fails, diagnose the source before retrying:

- Adjust `--bridge-gap` only in auto mode; increasing it can join parts of one asset or accidentally merge neighbors.
- `--alpha-threshold` counts only pixels with alpha strictly greater than the threshold for detection and crop bounds; it does not remove a matte or rewrite alpha values inside a crop. Lower it when faint effects are being clipped, then inspect the resulting gutters.
- `--min-area` filters candidates by foreground-pixel count. For intentionally tiny assets, inspect whether filtering caused an omission rather than weakening the expected count.
- Switch to grid only for an actual regular grid. For overlapping subjects or unusable transparency, repair/regenerate the source through the image tool when available and within scope.

Keep the expected count tied to the user's request. Do not merge, discard, or relabel regions merely to make extraction pass. Repeat generation only after identifying a concrete correction; report unresolved defects if the available workflow cannot fix them.

## Commands and Output Contract

Automatic extraction:

```bash
uv run --no-project --with pillow python \
  <skill-dir>/scripts/extract_sprite_atlas.py \
  atlas.png --out-dir extracted --mode auto --expected-count 12
```

Grid extraction with optional repack:

```bash
uv run --no-project --with pillow python \
  <skill-dir>/scripts/extract_sprite_atlas.py \
  atlas.png --out-dir extracted --mode grid --rows 3 --columns 4 \
  --expected-count 12 --repack repacked.png --repack-gap 24
```

Resolve `<skill-dir>` to the loaded skill directory. Inspect `--help` for additional options rather than guessing flags. The script accepts PNGs with alpha or transparency metadata, checks the expected count before writing, and refuses existing planned output paths unless `--force` is supplied. Use `--force` only for an intended replacement; it does not clean stale files from an earlier run. A failure during writing may leave partial outputs, so inspect them before retrying.

`--trim-padding` retains source pixels around the detected bounds, limited by each candidate's assigned region or grid cell; it does not guarantee a fixed transparent border. Repacking centers crops in uniform cells without scaling them. Choose repack columns, margins, and gaps for the consumer rather than assuming the source layout is retained.

The generated `manifest.json` contains sequential indices, filenames, source crop boxes, sizes, selected extraction settings, and optional repack placements. Bounding boxes use `[left, top, right, bottom]` with exclusive right/bottom edges; source boxes include retained padding. The manifest omits some parameters, including source grid dimensions and `min-area`, so retain the actual extraction command for reproducibility. It does not assign semantic asset names or retain original grid-slot numbers. Complete the separate asset plan by mapping each identifier and source slot to the verified output filename and manifest index; keep the generated manifest schema intact.

## Verify and Hand Off

Confirm that every planned item has one correct output, every crop is complete and free of neighboring pixels, transparency and soft effects survive, and the optional repack has clear gutters. Count equality alone does not establish identity or visual quality.

Provide links to the source, output directory, generated manifest, completed asset plan, and optional repack. Report the generation prompt when used, extraction command/settings, expected versus extracted count, and unresolved visual issues. Distinguish static asset inspection from in-engine or device validation.
