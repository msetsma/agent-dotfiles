from pathlib import Path
from typing import Any, cast
from urllib.parse import urlparse

import yaml  # type: ignore[import-untyped]

ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: str) -> dict[str, Any]:
    return cast("dict[str, Any]", yaml.safe_load((ROOT / path).read_text()))


def load_env_example(path: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in (ROOT / path).read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        key, separator, value = line.partition("=")

        assert separator == "="
        assert key not in values

        values[key] = value

    return values


def flatten_config_fragments(value: object) -> list[str]:
    if isinstance(value, dict):
        fragments: list[str] = []
        for key, child in value.items():
            fragments.append(str(key))
            fragments.extend(flatten_config_fragments(child))
        return fragments
    if isinstance(value, list):
        fragments = []
        for item in value:
            fragments.extend(flatten_config_fragments(item))
        return fragments
    return [str(value)]


def effective_work_config_fragments() -> list[str]:
    base = load_yaml("config/hermes/base.yaml")
    work = load_yaml("config/hermes/work.yaml")
    work_env = (ROOT / "config/work/env.example").read_text()

    return flatten_config_fragments(base) + flatten_config_fragments(work) + [work_env]


def test_hermes_version_pin_is_documented_in_base_config() -> None:
    config = load_yaml("config/hermes/base.yaml")

    assert config["hermes_agent_version"] == "0.16.0"
    assert config["hermes_agent_release_tag"] == "v2026.6.5"


def test_work_profile_blocks_external_messaging_and_graph() -> None:
    work = load_yaml("config/hermes/work.yaml")

    assert work["profile"] == "work"
    assert work["messaging"]["enabled"] is False
    assert work["runtime"]["host"] == "127.0.0.1"
    assert "microsoft_graph" not in work


def test_personal_and_work_env_examples_do_not_contain_real_secrets() -> None:
    personal = (ROOT / "config/personal/env.example").read_text()
    work = (ROOT / "config/work/env.example").read_text()

    forbidden_fragments = [
        "sk" + "-",
        "ghp" + "_",
        "pat" + "_",
        "BEGIN PRIVATE" + " KEY",
        "client" + "_secret=",
    ]

    for fragment in forbidden_fragments:
        assert fragment not in personal
        assert fragment not in work


def test_work_egress_allowlist_is_explicit() -> None:
    allowlist = (ROOT / "config/work/egress-allowlist.txt").read_text().splitlines()

    assert allowlist == ["127.0.0.1", "localhost"]


def test_work_env_example_is_mock_local_only() -> None:
    work_env = load_env_example("config/work/env.example")

    assert set(work_env) == {
        "HERMES_PROFILE",
        "HERMES_HOME",
        "OPENAI_API_KEY",
        "OPENAI_BASE_URL",
        "SANITIZED_MAIL_FIXTURE_HOST_PATH",
        "SANITIZED_TRANSCRIPT_FIXTURE_HOST_PATH",
        "SANITIZED_ONEDRIVE_FIXTURE_HOST_PATH",
    }
    assert work_env["HERMES_PROFILE"] == "work"
    assert work_env["HERMES_HOME"] == "/opt/data/work"
    assert work_env["OPENAI_API_KEY"] == "mock"
    assert work_env["OPENAI_BASE_URL"] == "http://127.0.0.1:18080/v1"
    assert urlparse(work_env["OPENAI_BASE_URL"]).hostname in {"127.0.0.1", "localhost"}
    assert work_env["SANITIZED_MAIL_FIXTURE_HOST_PATH"] == ""
    assert work_env["SANITIZED_TRANSCRIPT_FIXTURE_HOST_PATH"] == ""
    assert work_env["SANITIZED_ONEDRIVE_FIXTURE_HOST_PATH"] == ""


def test_work_profile_uses_sanitized_manual_export_fixtures() -> None:
    work = load_yaml("config/hermes/work.yaml")

    assert work["sources"] == {
        "sanitized_mail_fixture_dir": "/sources/fixtures/mail",
        "sanitized_transcript_fixture_dir": "/sources/fixtures/transcripts",
        "sanitized_onedrive_fixture_dir": "/sources/fixtures/onedrive",
    }


def test_work_config_has_no_external_messaging_graph_or_real_credentials() -> None:
    fragments = "\n".join(effective_work_config_fragments()).upper()

    forbidden_fragments = [
        "TELEGRAM",
        "DISCORD",
        "SLACK",
        "SIGNAL",
        "TEAMS_CLIENT",
        "GRAPH",
        "CLIENT_SECRET",
        "AZURE",
        "AZURE_DEVOPS_PAT",
        "AZURE_AI_FOUNDRY",
        "FOUNDRY",
        "PRODUCTION_PROVIDER",
        "WORK_GITHUB_TOKEN",
        "AZURE_OPENAI",
        "TOKEN",
        "GHP_",
        "PAT_",
        "SK-",
        "BEGIN PRIVATE" + " KEY",
    ]

    for fragment in forbidden_fragments:
        assert fragment not in fragments
