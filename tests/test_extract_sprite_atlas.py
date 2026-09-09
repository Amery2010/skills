from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    REPOSITORY_ROOT
    / "skills"
    / "small-image-atlas"
    / "scripts"
    / "extract_sprite_atlas.py"
)


def run_script(*args: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *(str(arg) for arg in args)],
        check=False,
        capture_output=True,
        text=True,
    )


def make_auto_atlas(path: Path) -> None:
    image = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle((10, 10, 29, 29), fill=(255, 0, 0, 255))
    draw.rectangle((70, 10, 94, 34), fill=(0, 255, 0, 220))
    draw.rectangle((10, 70, 34, 94), fill=(0, 0, 255, 255))
    draw.rectangle((75, 75, 99, 99), fill=(255, 255, 0, 180))
    image.save(path, format="PNG")


def test_auto_mode_extracts_row_major_sprites_and_repack(tmp_path: Path) -> None:
    source = tmp_path / "auto.png"
    output = tmp_path / "extracted"
    repacked = tmp_path / "repacked.png"
    make_auto_atlas(source)

    result = run_script(
        source,
        "--out-dir",
        output,
        "--mode",
        "auto",
        "--expected-count",
        4,
        "--repack",
        repacked,
        "--repack-columns",
        2,
    )

    assert result.returncode == 0, result.stderr
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["sprite_count"] == 4
    assert [entry["file"] for entry in manifest["sprites"]] == [
        "sprite-01.png",
        "sprite-02.png",
        "sprite-03.png",
        "sprite-04.png",
    ]
    assert [entry["source_bbox"][:2] for entry in manifest["sprites"]] == [
        [10, 10],
        [70, 10],
        [10, 70],
        [75, 75],
    ]
    assert manifest["repacked"]["columns"] == 2

    for entry in manifest["sprites"]:
        with Image.open(output / entry["file"]) as sprite:
            assert sprite.mode == "RGBA"
            assert sprite.getchannel("A").getbbox() is not None

    with Image.open(repacked) as image:
        assert image.mode == "RGBA"
        assert image.getchannel("A").getbbox() is not None


def test_grid_mode_keeps_disconnected_parts_in_each_cell(tmp_path: Path) -> None:
    source = tmp_path / "grid.png"
    output = tmp_path / "grid-output"
    image = Image.new("RGBA", (120, 60), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle((5, 10, 14, 19), fill=(255, 0, 0, 255))
    draw.rectangle((35, 35, 44, 44), fill=(255, 0, 0, 255))
    draw.rectangle((65, 8, 74, 17), fill=(0, 255, 0, 255))
    draw.rectangle((100, 38, 109, 47), fill=(0, 255, 0, 255))
    image.save(source, format="PNG")

    result = run_script(
        source,
        "--out-dir",
        output,
        "--mode",
        "grid",
        "--rows",
        1,
        "--columns",
        2,
        "--expected-count",
        2,
    )

    assert result.returncode == 0, result.stderr
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["sprite_count"] == 2
    assert manifest["sprites"][0]["source_bbox"] == [5, 10, 45, 45]
    assert manifest["sprites"][1]["source_bbox"] == [65, 8, 110, 48]


def test_expected_count_mismatch_fails_before_writing(tmp_path: Path) -> None:
    source = tmp_path / "source.png"
    output = tmp_path / "output"
    image = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
    ImageDraw.Draw(image).rectangle((10, 10, 20, 20), fill=(255, 255, 255, 255))
    image.save(source, format="PNG")

    result = run_script(source, "--out-dir", output, "--expected-count", 2)

    assert result.returncode == 1
    assert "Detected 1 sprites, expected 2" in result.stderr
    assert not output.exists()


def test_non_alpha_png_is_rejected(tmp_path: Path) -> None:
    source = tmp_path / "rgb.png"
    Image.new("RGB", (20, 20), (255, 255, 255)).save(source, format="PNG")

    result = run_script(source, "--out-dir", tmp_path / "output")

    assert result.returncode == 1
    assert "Input PNG has no alpha channel" in result.stderr


def test_existing_outputs_are_not_overwritten_without_force(tmp_path: Path) -> None:
    source = tmp_path / "source.png"
    output = tmp_path / "output"
    image = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
    ImageDraw.Draw(image).rectangle((10, 10, 20, 20), fill=(255, 255, 255, 255))
    image.save(source, format="PNG")

    first = run_script(source, "--out-dir", output, "--expected-count", 1)
    second = run_script(source, "--out-dir", output, "--expected-count", 1)

    assert first.returncode == 0, first.stderr
    assert second.returncode == 1
    assert "Refusing to overwrite existing output(s)" in second.stderr
