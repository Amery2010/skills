#!/usr/bin/env python3
"""Validate the distributable skill contract for this repository."""

from __future__ import annotations

import argparse
import ast
import re
import stat
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

ALLOWED_FRONTMATTER_KEYS = {
    "allowed-tools",
    "description",
    "license",
    "metadata",
    "name",
}
BAD_BASENAMES = {
    ".DS_Store",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
}
FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", re.DOTALL)
MARKDOWN_LINK_RE = re.compile(
    r"!?\[[^\]]*\]\((?P<target><[^>]+>|[^)\s]+)(?:\s+['\"][^)]*['\"])?\)"
)
MACHINE_PATH_RE = re.compile(
    r"(?:/Users/[^/\s]+/|/home/[^/\s]+/|[A-Za-z]:\\Users\\[^\\\s]+\\)"
)
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
README_SKILL_PATH_RE = re.compile(r"skills/(?P<name>[a-z0-9]+(?:-[a-z0-9]+)*)/?")
README_NON_SKILL_SEGMENTS = {"blob", "tree"}
TEXT_SUFFIXES = {".md", ".py", ".txt", ".yaml", ".yml"}


def display_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def parse_frontmatter(skill_md: Path, root: Path, errors: list[str]) -> dict[str, object] | None:
    label = display_path(skill_md, root)
    try:
        content = skill_md.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"{label}: cannot read UTF-8 content: {exc}")
        return None

    match = FRONTMATTER_RE.match(content)
    if not match:
        errors.append(f"{label}: missing or malformed YAML frontmatter")
        return None

    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        errors.append(f"{label}: invalid YAML frontmatter: {exc}")
        return None

    if not isinstance(frontmatter, dict):
        errors.append(f"{label}: frontmatter must be a mapping")
        return None

    unexpected = sorted(set(frontmatter) - ALLOWED_FRONTMATTER_KEYS)
    if unexpected:
        errors.append(f"{label}: unexpected frontmatter keys: {', '.join(unexpected)}")

    name = frontmatter.get("name")
    if not isinstance(name, str) or not name.strip():
        errors.append(f"{label}: 'name' must be a non-empty string")
    else:
        normalized_name = name.strip()
        if len(normalized_name) > 64 or not NAME_RE.fullmatch(normalized_name):
            errors.append(
                f"{label}: name must be at most 64 characters of lowercase letters, "
                "digits, and single hyphens"
            )
        if normalized_name != skill_md.parent.name:
            errors.append(
                f"{label}: frontmatter name '{normalized_name}' does not match "
                f"directory '{skill_md.parent.name}'"
            )

    description = frontmatter.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append(f"{label}: 'description' must be a non-empty string")
    elif len(description.strip()) > 1024 or "<" in description or ">" in description:
        errors.append(
            f"{label}: description must be at most 1024 characters and contain no angle brackets"
        )

    if re.search(r"\[TODO:[^\]]*\]", content, re.IGNORECASE):
        errors.append(f"{label}: unfinished scaffold placeholder found")

    return frontmatter


def validate_markdown_links(markdown: Path, skill_dir: Path, root: Path, errors: list[str]) -> None:
    label = display_path(markdown, root)
    try:
        content = markdown.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"{label}: cannot read UTF-8 content: {exc}")
        return

    skill_root = skill_dir.resolve()
    for match in MARKDOWN_LINK_RE.finditer(content):
        target = match.group("target").strip("<>")
        if target.startswith("#"):
            continue
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc:
            continue
        relative_path = unquote(parsed.path)
        if not relative_path:
            continue
        candidate = (markdown.parent / relative_path).resolve()
        if not candidate.is_relative_to(skill_root):
            errors.append(f"{label}: link escapes the skill directory: {target}")
        elif not candidate.exists():
            errors.append(f"{label}: broken relative link: {target}")


def validate_openai_yaml(skill_dir: Path, skill_name: str, root: Path, errors: list[str]) -> None:
    metadata_path = skill_dir / "agents" / "openai.yaml"
    if not metadata_path.exists():
        return
    label = display_path(metadata_path, root)
    try:
        data = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        errors.append(f"{label}: invalid YAML: {exc}")
        return
    if not isinstance(data, dict):
        errors.append(f"{label}: metadata must be a mapping")
        return
    interface = data.get("interface")
    if not isinstance(interface, dict):
        errors.append(f"{label}: 'interface' must be a mapping")
        return
    default_prompt = interface.get("default_prompt")
    if not isinstance(default_prompt, str) or not default_prompt.strip():
        errors.append(f"{label}: interface.default_prompt must be a non-empty string")
    elif f"${skill_name}" not in default_prompt:
        errors.append(
            f"{label}: interface.default_prompt must reference '${skill_name}'"
        )


def validate_python_scripts(skill_dir: Path, root: Path, errors: list[str]) -> None:
    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.is_dir():
        return
    for script in sorted(scripts_dir.rglob("*.py")):
        label = display_path(script, root)
        try:
            source = script.read_text(encoding="utf-8")
            ast.parse(source, filename=label)
        except (OSError, UnicodeError, SyntaxError) as exc:
            errors.append(f"{label}: invalid Python source: {exc}")
            continue
        if source.startswith("#!") and not script.stat().st_mode & (
            stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
        ):
            errors.append(f"{label}: shebang entrypoint must be executable")


def validate_tree_hygiene(skills_dir: Path, root: Path, errors: list[str]) -> None:
    for path in sorted(skills_dir.rglob("*")):
        label = display_path(path, root)
        if path.is_symlink():
            errors.append(f"{label}: symlinks are not allowed in distributable skills")
            continue
        if path.name in BAD_BASENAMES or path.suffix == ".pyc":
            errors.append(f"{label}: generated or machine-local artifact is not allowed")
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
            try:
                content = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as exc:
                errors.append(f"{label}: cannot read UTF-8 content: {exc}")
                continue
            match = MACHINE_PATH_RE.search(content)
            if match:
                errors.append(
                    f"{label}: machine-specific absolute path found: {match.group(0)}"
                )


def validate_readmes(root: Path, skill_names: set[str], errors: list[str]) -> None:
    skills_dir = root / "skills"
    for filename in ("README.md", "README.zh-CN.md"):
        readme = root / filename
        if not readme.is_file():
            errors.append(f"{filename}: required documentation file is missing")
            continue
        content = readme.read_text(encoding="utf-8")
        validate_markdown_links(readme, root, root, errors)
        listed_names = {
            match.group("name")
            for match in README_SKILL_PATH_RE.finditer(content)
            if match.group("name") not in README_NON_SKILL_SEGMENTS
        }
        missing = sorted(skill_names - listed_names)
        if missing:
            errors.append(f"{filename}: missing skill paths: {', '.join(missing)}")
        for listed_name in sorted(listed_names):
            if not (skills_dir / listed_name / "SKILL.md").is_file():
                errors.append(
                    f"{filename}: listed path has no SKILL.md: skills/{listed_name}"
                )


def validate_repository(root: Path) -> tuple[list[str], list[str]]:
    root = root.resolve()
    skills_dir = root / "skills"
    errors: list[str] = []
    skill_names: list[str] = []

    if not skills_dir.is_dir():
        return [], ["skills/: required directory is missing"]

    validate_tree_hygiene(skills_dir, root, errors)

    for child in sorted(skills_dir.iterdir()):
        if child.is_dir() and not child.is_symlink() and not (child / "SKILL.md").is_file():
            errors.append(
                f"{display_path(child, root)}: top-level skill directory has no SKILL.md"
            )

    skill_files = sorted(skills_dir.rglob("SKILL.md"))
    if not skill_files:
        errors.append("skills/: no SKILL.md files found")

    for skill_md in skill_files:
        skill_dir = skill_md.parent
        if skill_dir.parent != skills_dir:
            errors.append(
                f"{display_path(skill_md, root)}: skills must live directly under skills/"
            )
            continue
        frontmatter = parse_frontmatter(skill_md, root, errors)
        if not frontmatter:
            continue
        name = frontmatter.get("name")
        if not isinstance(name, str) or not name.strip():
            continue
        skill_name = name.strip()
        skill_names.append(skill_name)
        for markdown in sorted(skill_dir.rglob("*.md")):
            validate_markdown_links(markdown, skill_dir, root, errors)
        validate_openai_yaml(skill_dir, skill_name, root, errors)
        validate_python_scripts(skill_dir, root, errors)

    duplicates = sorted({name for name in skill_names if skill_names.count(name) > 1})
    if duplicates:
        errors.append(f"skills/: duplicate skill names: {', '.join(duplicates)}")

    validate_readmes(root, set(skill_names), errors)
    return sorted(set(skill_names)), errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root (defaults to the parent of scripts/)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    skill_names, errors = validate_repository(args.root)
    if errors:
        print("Skill repository validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Validated {len(skill_names)} skills: {', '.join(skill_names)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
