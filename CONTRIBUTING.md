# Contributing

[中文说明](#中文说明)

## Repository contract

Each distributable skill must live at `skills/<skill-name>` and include a valid `SKILL.md`. The folder name and the frontmatter `name` must match. Keep supporting files inside the same skill directory so GitHub path installation is self-contained.

Do not add generated output, `.DS_Store`, caches, symlinks, machine-specific absolute paths, or placeholder scaffold content. Preserve executable permissions on command-line scripts.

## Manual two-way synchronization

The repository and a local Codex skills directory are peers. Before changing files, choose and record one direction for each skill: local-to-repository or repository-to-local. Never use an unreviewed whole-directory overwrite when both sides changed.

1. Start from a clean, understood worktree and identify the latest release tag.
2. Compare the two current copies without changing either side:

   ```bash
   diff -ru --exclude=.DS_Store --exclude=__pycache__ /path/to/local/skills/<skill-name> skills/<skill-name>
   ```

   `diff` exits with status 1 when it finds differences; that is expected during inspection.

3. Materialize the latest tagged copy in a temporary directory, then compare both current copies with that common baseline:

   ```bash
   git archive <latest-tag> skills/<skill-name> | tar -x -C /path/to/temporary-directory
   diff -ru /path/to/temporary-directory/skills/<skill-name> /path/to/local/skills/<skill-name>
   diff -ru /path/to/temporary-directory/skills/<skill-name> skills/<skill-name>
   ```

4. If only one side changed, manually copy the reviewed files from that side in the declared direction.
5. If both sides changed, merge in the repository worktree file by file. Validate the merged result before copying it back to the local skills directory.
6. Repeat the direct comparison, inspect `git diff --summary` for mode changes, update `CHANGELOG.md`, and run all checks.

Never hard-code a contributor's home directory in committed files. Use caller-supplied paths in local commands.

## Validation

```bash
uv sync --locked
uv run python scripts/validate_skills.py
uv run pytest
```

For each new or changed skill, also run the current `quick_validate.py` bundled with Codex's `skill-creator` against that skill directory.

## Versioning

Use a patch release for compatible fixes, a minor release for new skills or compatible capabilities, and a major release for removals, renames, path changes, or incompatible workflow changes. Do not move or recreate published tags.

Before release, move the prepared changelog entry from `Unreleased` to the release date, run the complete local validation, and review the diff. Committing, tagging, pushing, and remote installation checks require explicit authorization.
## 中文说明

### 仓库契约

每个可分发 Skill 必须位于 `skills/<skill-name>` 并包含有效的 `SKILL.md`；目录名必须与 frontmatter 中的 `name` 一致。所有辅助文件都应保留在同一个 Skill 目录内，使 GitHub 路径安装具备自包含性。

不要提交生成物、`.DS_Store`、缓存、软链接、本机专属绝对路径或未完成的脚手架占位内容。命令行脚本必须保留可执行权限。

### 双向人工同步

仓库与本机 Codex Skills 目录是对等副本。修改文件前，必须为每个 Skill 选择并记录一个同步方向：本机到仓库，或仓库到本机。当两侧都发生变化时，禁止未经审核地覆盖整个目录。

1. 从状态明确的干净工作树开始，并确认最近的发布标签。
2. 使用上方的 `diff -ru` 命令只读比较两个当前副本；发现差异时退出码 1 属于正常结果。
3. 使用上方的 `git archive` 命令把最近标签解压到临时目录，分别比较本机副本与仓库副本相对共同基线的变化。
4. 只有一侧变化时，按声明方向人工复制审核过的文件。
5. 两侧均变化时，在仓库工作树中逐文件合并；校验通过后再回写本机目录。
6. 再次比较内容，使用 `git diff --summary` 检查权限变化，更新 `CHANGELOG.md`，并运行全部校验。

提交文件中不得硬编码贡献者的主目录；本地命令应由调用者提供路径。

### 校验与版本

运行上方列出的 `uv` 校验命令，并对每个新增或修改的 Skill 执行 Codex `skill-creator` 所附的当前 `quick_validate.py`。

兼容性修复使用 Patch 版本；新增 Skill 或兼容性能力使用 Minor 版本；删除、重命名、路径变化或不兼容工作流使用 Major 版本。发布前应把准备中的日志条目改为实际发布日期，运行完整本地校验并检查差异。提交、打标签、推送和远程安装检查均需要明确授权。
