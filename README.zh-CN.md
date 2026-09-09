# Amery 的 Skills

[English](README.md)

这是一个公开的独立 Agent Skills 集合，可通过 Codex 内置的 `$skill-installer` 从 GitHub 安装。每个 Skill 都位于稳定的 `skills/<skill-name>` 路径，并遵循 [OpenAI 文档](https://learn.chatgpt.com/docs/build-skills)所述的 Agent Skills 目录格式。

## 可用 Skills

| Skill | 适用场景 | 运行说明 |
| --- | --- | --- |
| [`frontend-ui-aesthetics`](skills/frontend-ui-aesthetics/) | 设计具有强烈艺术指导、视觉表现和交互品质的营销站、作品集、编辑专题、活动页和沉浸式 Web 体验。 | 没有仓库级运行依赖；实际项目可能需要 Lucide 和项目自身的前端工具链。 |
| [`prompt-improver`](skills/prompt-improver/) | 审核和改写 LLM 提示词，同时保留目标、接口和授权边界。 | 纯指令型 Skill，包含策略和评估参考资料。 |
| [`small-image-atlas`](skills/small-image-atlas/) | 批量生成透明小型栅格素材，按 Alpha 边界提取，并可重新打包图集。 | 需要 Python、`uv`、Pillow，以及生成源图时可用的 `imagegen` 能力。包含可执行 Python 脚本，安装前应先检查。 |

## 安装

使用 GitHub tree URL 调用内置安装器，Skill 将被安装到 Codex 的 Skills 目录。

从 `main` 安装最新版：

```text
$skill-installer install https://github.com/Amery2010/skills/tree/main/skills/prompt-improver
```

在 `v0.1.0` 标签发布后安装固定版本：

```text
$skill-installer install https://github.com/Amery2010/skills/tree/v0.1.0/skills/prompt-improver
```

一次安装三个 Skill：

```text
$skill-installer install from Amery2010/skills at ref main with paths skills/frontend-ui-aesthetics, skills/prompt-improver, and skills/small-image-atlas
```

安装器不会覆盖已经存在的目标目录。更新前，请先备份或移动准备替换的已安装 Skill，再安装目标分支或标签。新安装的 Skill 会在下一轮对话中可用；若仍未出现，请重启 Codex。

## 版本策略

`main` 表示最新的已审核状态；`v0.1.0` 等发布标签是不可变的安装锚点。

仓库遵循语义化版本规则：

- Patch：兼容性的指令、文档或脚本修复。
- Minor：新增 Skill 或向后兼容的能力扩展。
- Major：删除或重命名 Skill、改变路径，或引入不兼容的工作流变化。

版本内容见 [CHANGELOG.md](CHANGELOG.md)。

## 开发与同步

运行仓库校验：

```bash
uv sync --locked
uv run python scripts/validate_skills.py
uv run pytest
```

仓库副本与本机 Codex Skills 目录都可能产生有意修改。请遵循 [CONTRIBUTING.md](CONTRIBUTING.md) 中基于冲突判断的人工同步流程；仓库不提供自动双向覆盖。

## 安全说明

Skill 可能包含可执行脚本，以及会影响 Agent 行为的指令。安装前请检查 Skill 的完整目录，尤其是 `scripts/` 下的文件。仓库自动检查只验证打包契约与确定性辅助脚本行为，不能替代对 Skill 指令和可执行内容的人工审核。

## 许可证

本项目采用 [MIT License](LICENSE)。
