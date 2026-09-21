# Changelog

All notable changes to this repository are documented in this file.

The repository uses semantic versioning for its public skill paths and workflows.

## [0.2.0]

### Changed

- Added project-scoped Codex instructions in `AGENTS.md` and custom-agent configuration under `.codex/`.
- Streamlined all three skills and aligned their invocation prompts with scoped workflows and evidence-based handoffs.
- Added product-contract preservation and explicit browser-verification limits to `frontend-ui-aesthetics`.
- Added post-rewrite contract checks, template integration guidance, and baseline evaluation reporting to `prompt-improver`.
- Clarified existing-atlas workflows, segmentation limits, transparency checks, and asset-name mapping in `small-image-atlas` without changing the extraction script or manifest schema.

## [0.1.0] - Unreleased

This version is prepared locally and is not published until the `v0.1.0` tag exists on GitHub.

### Added

- Added the `frontend-ui-aesthetics` standalone skill.
- Added the `prompt-improver` standalone skill and its strategy and evaluation references.
- Added the `small-image-atlas` standalone skill and deterministic extraction script.
- Added bilingual installation documentation, repository validation, helper tests, and CI.
- Documented conflict-aware manual synchronization between repository and local skill copies.

[Unreleased]: https://github.com/Amery2010/skills/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Amery2010/skills/releases/tag/v0.1.0
