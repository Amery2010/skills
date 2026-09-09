# Amery's Skills

[简体中文](README.zh-CN.md)

A public collection of standalone agent skills that can be installed from GitHub with Codex's `$skill-installer`. Each skill lives at a stable `skills/<skill-name>` path and follows the Agent Skills directory format documented by [OpenAI](https://learn.chatgpt.com/docs/build-skills).

## Available skills

| Skill | Use it for | Runtime notes |
| --- | --- | --- |
| [`frontend-ui-aesthetics`](skills/frontend-ui-aesthetics/) | Designing visually ambitious, art-directed marketing, portfolio, editorial, campaign, and immersive web experiences. | No repository-level runtime dependency. Projects using it may need Lucide and their existing frontend toolchain. |
| [`prompt-improver`](skills/prompt-improver/) | Auditing and rewriting LLM prompts while preserving intent, interfaces, and authorization boundaries. | Instruction-only, with supporting strategy and evaluation references. |
| [`small-image-atlas`](skills/small-image-atlas/) | Generating batches of small transparent raster assets, extracting them by alpha bounds, and optionally repacking them. | Requires Python, `uv`, Pillow, and an available `imagegen` capability when generating source artwork. Includes an executable Python script; inspect it before installation. |

## Install

Invoke the built-in installer with a GitHub tree URL. This installs the skill into your Codex skills directory.

Latest version from `main`:

```text
$skill-installer install https://github.com/Amery2010/skills/tree/main/skills/prompt-improver
```

Pinned release after the `v0.1.0` tag is published:

```text
$skill-installer install https://github.com/Amery2010/skills/tree/v0.1.0/skills/prompt-improver
```

To install all three skills in one request:

```text
$skill-installer install from Amery2010/skills at ref main with paths skills/frontend-ui-aesthetics, skills/prompt-improver, and skills/small-image-atlas
```

The installer refuses to overwrite an existing destination directory. Before updating, back up or move the installed skill you intend to replace, then install the desired branch or tag. A newly installed skill is available on the next turn; restart Codex if it does not appear.

## Versions

`main` is the latest reviewed state. Release tags such as `v0.1.0` are immutable installation anchors.

Repository releases follow semantic versioning:

- Patch: compatible instruction, documentation, or script fixes.
- Minor: new skills or backward-compatible capability additions.
- Major: removed or renamed skills, path changes, or incompatible workflow changes.

See [CHANGELOG.md](CHANGELOG.md) for release contents.

## Development and synchronization

Run the repository checks with:

```bash
uv sync --locked
uv run python scripts/validate_skills.py
uv run pytest
```

The repository copy and a local Codex skills directory may both receive intentional changes. Follow the conflict-aware, manual synchronization procedure in [CONTRIBUTING.md](CONTRIBUTING.md); no automatic bidirectional overwrite is provided.

## Security

A skill can contain executable scripts and instructions that influence an agent's behavior. Review a skill's complete directory before installation, especially files under `scripts/`. This repository's automated checks validate packaging and deterministic helper behavior, but they are not a substitute for reviewing what a skill instructs or executes.

## License

Released under the [MIT License](LICENSE).
