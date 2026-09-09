from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = REPOSITORY_ROOT / "scripts" / "validate_skills.py"


def copy_repository(tmp_path: Path) -> Path:
    destination = tmp_path / "repository"
    return Path(
        shutil.copytree(
            REPOSITORY_ROOT,
            destination,
            ignore=shutil.ignore_patterns(
                ".git", ".venv", ".pytest_cache", ".ruff_cache", "__pycache__"
            ),
        )
    )


def run_validator(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), "--root", str(root)],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )


def assert_invalid(root: Path, expected_message: str) -> None:
    result = run_validator(root)
    assert result.returncode == 1
    assert expected_message in result.stderr


def test_repository_contract_is_valid() -> None:
    result = run_validator(REPOSITORY_ROOT)
    assert result.returncode == 0, result.stderr
    assert "Validated 3 skills" in result.stdout


@pytest.mark.parametrize(
    ("replacement", "expected_message"),
    [
        ("name: Prompt Improver", "name must be at most 64 characters"),
        ("name: prompt-reviewer", "does not match directory 'prompt-improver'"),
    ],
)
def test_rejects_invalid_or_mismatched_name(
    tmp_path: Path, replacement: str, expected_message: str
) -> None:
    root = copy_repository(tmp_path)
    skill_md = root / "skills" / "prompt-improver" / "SKILL.md"
    skill_md.write_text(
        skill_md.read_text(encoding="utf-8").replace(
            "name: prompt-improver", replacement, 1
        ),
        encoding="utf-8",
    )
    assert_invalid(root, expected_message)


def test_rejects_broken_relative_link(tmp_path: Path) -> None:
    root = copy_repository(tmp_path)
    skill_md = root / "skills" / "prompt-improver" / "SKILL.md"
    skill_md.write_text(
        skill_md.read_text(encoding="utf-8")
        + "\n[Missing reference](references/does-not-exist.md)\n",
        encoding="utf-8",
    )
    assert_invalid(root, "broken relative link")


def test_rejects_relative_link_that_escapes_skill(tmp_path: Path) -> None:
    root = copy_repository(tmp_path)
    skill_md = root / "skills" / "prompt-improver" / "SKILL.md"
    skill_md.write_text(
        skill_md.read_text(encoding="utf-8") + "\n[Outside](../../README.md)\n",
        encoding="utf-8",
    )
    assert_invalid(root, "link escapes the skill directory")


def test_rejects_malformed_frontmatter(tmp_path: Path) -> None:
    root = copy_repository(tmp_path)
    skill_md = root / "skills" / "prompt-improver" / "SKILL.md"
    skill_md.write_text(
        skill_md.read_text(encoding="utf-8").replace(
            "name: prompt-improver", "name: [prompt-improver", 1
        ),
        encoding="utf-8",
    )
    assert_invalid(root, "invalid YAML frontmatter")


def test_rejects_machine_specific_path(tmp_path: Path) -> None:
    root = copy_repository(tmp_path)
    skill_md = root / "skills" / "prompt-improver" / "SKILL.md"
    skill_md.write_text(
        skill_md.read_text(encoding="utf-8") + "\n/Users/example/private/file.txt\n",
        encoding="utf-8",
    )
    assert_invalid(root, "machine-specific absolute path found")


def test_rejects_default_prompt_for_another_skill(tmp_path: Path) -> None:
    root = copy_repository(tmp_path)
    metadata = root / "skills" / "prompt-improver" / "agents" / "openai.yaml"
    metadata.write_text(
        metadata.read_text(encoding="utf-8").replace(
            "$prompt-improver", "$another-skill", 1
        ),
        encoding="utf-8",
    )
    assert_invalid(root, "interface.default_prompt must reference '$prompt-improver'")


def test_rejects_non_executable_shebang_script(tmp_path: Path) -> None:
    root = copy_repository(tmp_path)
    script = (
        root
        / "skills"
        / "small-image-atlas"
        / "scripts"
        / "extract_sprite_atlas.py"
    )
    script.chmod(0o644)
    assert_invalid(root, "shebang entrypoint must be executable")


def test_rejects_machine_local_artifact(tmp_path: Path) -> None:
    root = copy_repository(tmp_path)
    artifact = root / "skills" / "prompt-improver" / ".DS_Store"
    artifact.write_bytes(b"not repository content")
    assert_invalid(root, "machine-local artifact is not allowed")


@pytest.mark.skipif(not hasattr(os, "symlink"), reason="symlinks are unavailable")
def test_rejects_symlink(tmp_path: Path) -> None:
    root = copy_repository(tmp_path)
    target = tmp_path / "outside.txt"
    target.write_text("outside", encoding="utf-8")
    link = root / "skills" / "prompt-improver" / "outside-link.txt"
    link.symlink_to(target)
    assert_invalid(root, "symlinks are not allowed")


def test_each_readme_must_list_every_skill(tmp_path: Path) -> None:
    root = copy_repository(tmp_path)
    readme = root / "README.md"
    readme.write_text(
        readme.read_text(encoding="utf-8").replace(
            "skills/frontend-ui-aesthetics", "catalog/frontend-ui-aesthetics"
        ),
        encoding="utf-8",
    )
    assert_invalid(root, "README.md: missing skill paths: frontend-ui-aesthetics")
