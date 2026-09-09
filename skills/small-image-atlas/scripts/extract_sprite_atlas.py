#!/usr/bin/env python3
"""Extract alpha-bounded sprites from a transparent PNG and optionally repack them."""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path

try:
    from PIL import Image
except (
    ImportError
) as exc:  # pragma: no cover - exercised by environments without Pillow
    raise SystemExit(
        "Pillow is required. Run with: uv run --no-project --with pillow python "
        "scripts/extract_sprite_atlas.py ..."
    ) from exc


@dataclass(frozen=True)
class Sprite:
    source_bbox: tuple[int, int, int, int]
    image: Image.Image


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Extract sprites from an RGBA PNG using transparent gutters or known grid "
            "slots, then optionally repack them on a fresh transparent canvas."
        )
    )
    parser.add_argument("input", type=Path, help="Source transparent PNG atlas")
    parser.add_argument(
        "--out-dir", type=Path, required=True, help="Directory for crops and manifest"
    )
    parser.add_argument("--mode", choices=("auto", "grid"), default="auto")
    parser.add_argument("--rows", type=int, help="Grid rows; required in grid mode")
    parser.add_argument(
        "--columns", type=int, help="Grid columns; required in grid mode"
    )
    parser.add_argument(
        "--alpha-threshold",
        type=int,
        default=8,
        help="Alpha values above this are foreground (0-254; default: 8)",
    )
    parser.add_argument(
        "--bridge-gap",
        type=int,
        default=4,
        help="Auto mode: merge occupied bands separated by at most this many empty pixels",
    )
    parser.add_argument(
        "--min-area",
        type=int,
        default=16,
        help="Ignore candidates with fewer foreground pixels (default: 16)",
    )
    parser.add_argument(
        "--trim-padding",
        type=int,
        default=0,
        help="Transparent padding retained around each alpha-tight crop",
    )
    parser.add_argument(
        "--expected-count", type=int, help="Fail unless this many sprites are found"
    )
    parser.add_argument("--prefix", default="sprite", help="Output filename prefix")
    parser.add_argument("--manifest-name", default="manifest.json")
    parser.add_argument(
        "--repack", type=Path, help="Optional fresh transparent PNG atlas"
    )
    parser.add_argument(
        "--repack-columns", type=int, help="Columns in the repacked atlas"
    )
    parser.add_argument(
        "--repack-gap",
        type=int,
        default=16,
        help="Transparent gap between repacked cells",
    )
    parser.add_argument(
        "--repack-margin", type=int, default=16, help="Transparent outer margin"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite only the output files this invocation plans to write",
    )
    args = parser.parse_args()

    for name in (
        "alpha_threshold",
        "bridge_gap",
        "min_area",
        "trim_padding",
        "repack_gap",
        "repack_margin",
    ):
        if getattr(args, name) < 0:
            parser.error(f"--{name.replace('_', '-')} must be non-negative")
    if args.alpha_threshold > 254:
        parser.error("--alpha-threshold must be between 0 and 254")
    if args.mode == "grid" and (not args.rows or not args.columns):
        parser.error("--rows and --columns are required in grid mode")
    if args.mode == "auto" and (args.rows is not None or args.columns is not None):
        parser.error("--rows and --columns are only valid in grid mode")
    for name in ("rows", "columns", "expected_count", "repack_columns"):
        value = getattr(args, name)
        if value is not None and value <= 0:
            parser.error(f"--{name.replace('_', '-')} must be positive")
    if not args.prefix or "/" in args.prefix or "\\" in args.prefix:
        parser.error("--prefix must be a non-empty filename prefix")
    if Path(args.manifest_name).name != args.manifest_name:
        parser.error("--manifest-name must be a filename, not a path")
    return args


def has_alpha(image: Image.Image) -> bool:
    return image.mode in {"RGBA", "LA"} or "transparency" in image.info


def foreground(alpha: Image.Image, threshold: int) -> bytearray:
    return bytearray(1 if value > threshold else 0 for value in alpha.tobytes())


def occupied_runs(flags: Sequence[bool], bridge_gap: int) -> list[tuple[int, int]]:
    raw: list[tuple[int, int]] = []
    start: int | None = None
    for index, value in enumerate(flags):
        if value and start is None:
            start = index
        elif not value and start is not None:
            raw.append((start, index))
            start = None
    if start is not None:
        raw.append((start, len(flags)))

    merged: list[tuple[int, int]] = []
    for current in raw:
        if merged and current[0] - merged[-1][1] <= bridge_gap:
            merged[-1] = (merged[-1][0], current[1])
        else:
            merged.append(current)
    return merged


def partition_bounds(
    runs: Sequence[tuple[int, int]], length: int
) -> list[tuple[int, int]]:
    """Assign each occupied run a non-overlapping share of adjacent empty gutters."""
    bounds: list[tuple[int, int]] = []
    for index, (start, end) in enumerate(runs):
        lower = 0 if index == 0 else (runs[index - 1][1] + start) // 2
        upper = length if index == len(runs) - 1 else (end + runs[index + 1][0]) // 2
        bounds.append((lower, upper))
    return bounds


def tight_bbox(
    mask: Sequence[int],
    width: int,
    candidate: tuple[int, int, int, int],
) -> tuple[tuple[int, int, int, int] | None, int]:
    left, top, right, bottom = candidate
    min_x = right
    min_y = bottom
    max_x = left - 1
    max_y = top - 1
    count = 0
    for y in range(top, bottom):
        offset = y * width
        for x in range(left, right):
            if mask[offset + x]:
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)
                count += 1
    if not count:
        return None, 0
    return (min_x, min_y, max_x + 1, max_y + 1), count


def with_padding(
    bbox: tuple[int, int, int, int],
    padding: int,
    bounds: tuple[int, int, int, int],
) -> tuple[int, int, int, int]:
    left, top, right, bottom = bbox
    bound_left, bound_top, bound_right, bound_bottom = bounds
    return (
        max(bound_left, left - padding),
        max(bound_top, top - padding),
        min(bound_right, right + padding),
        min(bound_bottom, bottom + padding),
    )


def extract_auto(
    image: Image.Image,
    mask: Sequence[int],
    bridge_gap: int,
    min_area: int,
    trim_padding: int,
) -> list[Sprite]:
    width, height = image.size
    row_flags = [any(mask[y * width : (y + 1) * width]) for y in range(height)]
    sprites: list[Sprite] = []

    row_runs = occupied_runs(row_flags, bridge_gap)
    for (top, bottom), (bound_top, bound_bottom) in zip(
        row_runs, partition_bounds(row_runs, height)
    ):
        column_flags = [
            any(mask[y * width + x] for y in range(top, bottom)) for x in range(width)
        ]
        column_runs = occupied_runs(column_flags, bridge_gap)
        for (left, right), (bound_left, bound_right) in zip(
            column_runs, partition_bounds(column_runs, width)
        ):
            bbox, area = tight_bbox(mask, width, (left, top, right, bottom))
            if bbox is None or area < min_area:
                continue
            padded = with_padding(
                bbox,
                trim_padding,
                (bound_left, bound_top, bound_right, bound_bottom),
            )
            sprites.append(Sprite(padded, image.crop(padded)))
    return sprites


def grid_edges(length: int, slots: int) -> list[int]:
    return [round(index * length / slots) for index in range(slots + 1)]


def extract_grid(
    image: Image.Image,
    mask: Sequence[int],
    rows: int,
    columns: int,
    min_area: int,
    trim_padding: int,
) -> list[Sprite]:
    width, height = image.size
    x_edges = grid_edges(width, columns)
    y_edges = grid_edges(height, rows)
    sprites: list[Sprite] = []
    for row in range(rows):
        for column in range(columns):
            cell = (
                x_edges[column],
                y_edges[row],
                x_edges[column + 1],
                y_edges[row + 1],
            )
            bbox, area = tight_bbox(mask, width, cell)
            if bbox is None or area < min_area:
                continue
            padded = with_padding(bbox, trim_padding, cell)
            sprites.append(Sprite(padded, image.crop(padded)))
    return sprites


def assert_writable(paths: Iterable[Path], force: bool) -> None:
    existing = [str(path) for path in paths if path.exists()]
    if existing and not force:
        joined = "\n  ".join(existing)
        raise SystemExit(
            f"Refusing to overwrite existing output(s):\n  {joined}\nUse --force to replace them."
        )


def save_repack(
    sprites: Sequence[Sprite],
    output: Path,
    columns: int | None,
    gap: int,
    margin: int,
) -> dict[str, object]:
    count = len(sprites)
    columns = columns or math.ceil(math.sqrt(count))
    rows = math.ceil(count / columns)
    cell_width = max(sprite.image.width for sprite in sprites)
    cell_height = max(sprite.image.height for sprite in sprites)
    atlas_width = margin * 2 + columns * cell_width + max(0, columns - 1) * gap
    atlas_height = margin * 2 + rows * cell_height + max(0, rows - 1) * gap
    atlas = Image.new("RGBA", (atlas_width, atlas_height), (0, 0, 0, 0))
    placements: list[dict[str, object]] = []
    for index, sprite in enumerate(sprites):
        row, column = divmod(index, columns)
        cell_x = margin + column * (cell_width + gap)
        cell_y = margin + row * (cell_height + gap)
        x = cell_x + (cell_width - sprite.image.width) // 2
        y = cell_y + (cell_height - sprite.image.height) // 2
        atlas.alpha_composite(sprite.image, (x, y))
        placements.append(
            {
                "index": index + 1,
                "bbox": [x, y, x + sprite.image.width, y + sprite.image.height],
            }
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    atlas.save(output, format="PNG")
    return {
        "path": str(output.resolve()),
        "size": [atlas_width, atlas_height],
        "rows": rows,
        "columns": columns,
        "cell_size": [cell_width, cell_height],
        "gap": gap,
        "margin": margin,
        "placements": placements,
    }


def main() -> int:
    args = parse_args()
    if not args.input.is_file():
        raise SystemExit(f"Input file does not exist: {args.input}")

    with Image.open(args.input) as source:
        if source.format != "PNG":
            raise SystemExit(
                f"Input must be a PNG, got: {source.format or 'unknown format'}"
            )
        if not has_alpha(source):
            raise SystemExit(
                "Input PNG has no alpha channel; a transparent atlas is required."
            )
        image = source.convert("RGBA")

    alpha = image.getchannel("A")
    mask = foreground(alpha, args.alpha_threshold)
    if args.mode == "auto":
        sprites = extract_auto(
            image, mask, args.bridge_gap, args.min_area, args.trim_padding
        )
    else:
        sprites = extract_grid(
            image,
            mask,
            args.rows,
            args.columns,
            args.min_area,
            args.trim_padding,
        )

    if not sprites:
        raise SystemExit("No sprites were detected above the alpha threshold.")
    if args.expected_count is not None and len(sprites) != args.expected_count:
        raise SystemExit(
            f"Detected {len(sprites)} sprites, expected {args.expected_count}. "
            "Inspect the atlas, adjust segmentation settings, or regenerate with wider gutters."
        )

    digits = max(2, len(str(len(sprites))))
    output_paths = [
        args.out_dir / f"{args.prefix}-{index:0{digits}d}.png"
        for index in range(1, len(sprites) + 1)
    ]
    manifest_path = args.out_dir / args.manifest_name
    planned_paths = [*output_paths, manifest_path]
    if args.repack:
        planned_paths.append(args.repack)
    resolved_paths = [path.resolve() for path in planned_paths]
    if len(set(resolved_paths)) != len(resolved_paths):
        raise SystemExit("Output paths must be distinct.")
    if args.input.resolve() in resolved_paths:
        raise SystemExit(
            "An output path resolves to the input atlas; choose a separate path."
        )
    assert_writable(planned_paths, args.force)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    entries: list[dict[str, object]] = []
    for index, (sprite, output_path) in enumerate(zip(sprites, output_paths), start=1):
        sprite.image.save(output_path, format="PNG")
        entries.append(
            {
                "index": index,
                "file": output_path.name,
                "source_bbox": list(sprite.source_bbox),
                "size": list(sprite.image.size),
            }
        )

    repack_info = None
    if args.repack:
        repack_info = save_repack(
            sprites,
            args.repack,
            args.repack_columns,
            args.repack_gap,
            args.repack_margin,
        )

    manifest = {
        "version": 1,
        "source": str(args.input.resolve()),
        "source_size": list(image.size),
        "mode": args.mode,
        "alpha_threshold": args.alpha_threshold,
        "bridge_gap": args.bridge_gap if args.mode == "auto" else None,
        "trim_padding": args.trim_padding,
        "expected_count": args.expected_count,
        "sprite_count": len(sprites),
        "sprites": entries,
        "repacked": repack_info,
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    print(f"Extracted {len(sprites)} sprites to {args.out_dir.resolve()}")
    print(f"Manifest: {manifest_path.resolve()}")
    if args.repack:
        print(f"Repacked atlas: {args.repack.resolve()}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
