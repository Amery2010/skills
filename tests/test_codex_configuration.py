from __future__ import annotations

import tomllib
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CODEX_ROOT = REPOSITORY_ROOT / ".codex"
AGENT_NAMES = ("astra_worker", "sol_expert", "luna_worker", "luna_fast")


def load_toml(path: Path) -> dict[str, object]:
    with path.open("rb") as stream:
        return tomllib.load(stream)


def test_project_codex_configuration_has_expected_defaults() -> None:
    config = load_toml(CODEX_ROOT / "config.toml")

    assert config["model"] == "gpt-6-astra"
    assert config["agents"] == {
        "enabled": True,
        "max_concurrent_threads_per_session": 6,
        "default_subagent_model": "gpt-5.6-luna",
        "default_subagent_reasoning_effort": "max",
        "interrupt_message": True,
    }


def test_custom_agents_have_required_fields_and_matching_names() -> None:
    for agent_name in AGENT_NAMES:
        agent_path = CODEX_ROOT / "agents" / f"{agent_name}.toml"
        agent = load_toml(agent_path)

        assert agent["name"] == agent_name
        for field in ("description", "developer_instructions"):
            assert isinstance(agent[field], str)
            assert agent[field].strip()


def test_project_configuration_excludes_archive_metadata() -> None:
    paths = {
        path.relative_to(CODEX_ROOT).as_posix()
        for path in CODEX_ROOT.rglob("*")
        if path.is_file()
    }

    assert ".DS_Store" not in paths
    assert not any(path.startswith("__MACOSX/") for path in paths)


def test_repository_instructions_are_present() -> None:
    instructions = (REPOSITORY_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    codex_instructions = (CODEX_ROOT / "AGENTS.md").read_text(encoding="utf-8")

    assert codex_instructions == instructions
    assert "## Development policy" in instructions
    assert "## Multi-agent orchestration" in instructions
    assert "### Completion" in instructions
