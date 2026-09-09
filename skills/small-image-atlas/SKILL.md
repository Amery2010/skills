---
name: small-image-atlas
description: Generate many small, independently usable raster assets as transparent PNG sprite atlases, extract them by alpha bounds, and optionally repack them with controlled gutters. Use for batches of icons, items, tokens, stickers, UI ornaments, or small 2D game assets; do not use for large standalone images, scenes, posters, covers, or hero art.
---

# Small Image Atlas

Produce batches of small raster assets through one or more transparent sprite atlases. Keep the atlas source, deterministic extractions, and an optional clean repack so downstream work can use either the individual PNGs or the sheet.

## Scope

Use this workflow when the requested images are independently usable small assets that can remain legible while sharing a normal image-generation canvas. Treat scene-level composition, readable prose, photographic detail, or standalone display resolution as a large-image requirement and route that work outside this skill. For a mixed request, use this workflow only for its small-asset subset.

Prefer one atlas when the assets share a visual language. Split the request into a few coherent atlases when one sheet would make subjects too small, crowd the gutters, or mix incompatible styles. Preserve the user's requested asset count and grouping.

## Workflow

1. Make an asset manifest before generation.
   - Record the exact count, a short identifier for each asset, and the row-major order.
   - Choose rows, columns, canvas size, approximate item size, outer margin, and gutter.
   - Reserve transparent gutters of at least 16 px or one eighth of the intended item width, whichever is larger. Increase this for soft glows, particles, shadows, or irregular silhouettes.
   - Keep identifiers in the manifest; do not render labels or numbers into the atlas.

2. Generate the atlas as one composite raster asset.
   - Use the installed `imagegen` skill for the actual image-generation or edit call.
   - Ask for exactly the manifest count in a strict row-major grid, with one centered subject per non-overlapping slot.
   - Require a genuinely transparent background and preserved alpha, not a checkerboard, white field, or background-colored imitation.
   - Require fully isolated silhouettes, generous empty gutters, consistent scale, viewpoint, lighting, palette, and rendering style.
   - Keep every subject and its effects inside its slot. Exclude scenery, captions, borders, grid lines, watermarks, and shadows or effects that cross into another slot.
   - Treat the atlas as the requested composite asset. Generate separate images only when an atlas attempt cannot preserve isolation or the user explicitly requests separate sources.

3. Inspect before extracting.
   - View the full-resolution PNG and compare every slot with the manifest.
   - Check count, order, duplicates, omissions, clipping, style drift, and gutters.
   - Confirm the file has an alpha channel; a visually plain background is not sufficient.

4. Extract by transparent bounds.
   - Run `scripts/extract_sprite_atlas.py` with `--expected-count` so a segmentation mismatch fails visibly.
   - Start with `--mode auto` when full transparent row and column gutters clearly separate the sprites.
   - Use `--mode grid --rows <R> --columns <C>` when a sprite contains disconnected internal pieces, soft effects, or holes that confuse automatic gutter detection. Grid mode still trims each slot to its alpha boundary.
   - If the detected count is wrong, inspect the source and adjust `--bridge-gap` or `--alpha-threshold`, switch to grid mode, or regenerate with wider gutters. Do not silently merge, discard, or relabel unexpected regions.

5. Repack only when useful.
   - Add `--repack <path.png>` to place the extracted sprites on a fresh transparent canvas with deterministic margins and gutters.
   - Preserve row-major manifest order. Use individual extractions directly when a new sheet adds no downstream value.

6. Verify the deliverables.
   - The extracted count equals the manifest count.
   - Every crop contains one complete intended asset and no pixels from a neighbor.
   - Alpha is preserved; no opaque matte, checkerboard, label, or grid line remains.
   - The optional repack has non-overlapping sprites and visibly transparent gutters.
   - The manifest maps every output filename to its source bounding box and order.

## Commands

Automatic transparent-gutter extraction:

```bash
uv run --no-project --with pillow python \
  <skill-dir>/scripts/extract_sprite_atlas.py \
  atlas.png --out-dir extracted --mode auto --expected-count 12
```

Grid-assisted extraction and optional repack:

```bash
uv run --no-project --with pillow python \
  <skill-dir>/scripts/extract_sprite_atlas.py \
  atlas.png --out-dir extracted --mode grid --rows 3 --columns 4 \
  --expected-count 12 --repack repacked.png --repack-gap 24
```

The script refuses non-alpha inputs and existing output files unless `--force` is explicitly supplied. It writes `manifest.json` beside the extracted PNGs. Use `--trim-padding` to retain transparent breathing room around each tight alpha crop, and use `--bridge-gap` only in automatic mode to bridge short fully transparent gaps inside one sprite.

## Handoff

Report the source atlas, individual-output directory, manifest, optional repacked atlas, final generation prompt, extraction mode, expected versus extracted count, and any remaining visual uncertainty. Do not represent static inspection as in-engine or device validation.
