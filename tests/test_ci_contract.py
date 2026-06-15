import json
from pathlib import Path
from typing import Any, cast

import yaml  # type: ignore[import-untyped]

ROOT = Path(__file__).resolve().parents[1]


def find_step(steps: list[dict[str, Any]], name: str) -> dict[str, Any]:
    for step in steps:
        if step.get("name") == name:
            return step

    raise AssertionError(f"Missing CI step: {name}")


def test_devcontainer_uses_pinned_python_311_base_and_uv() -> None:
    dockerfile = (ROOT / ".devcontainer/Dockerfile").read_text()

    assert (
        "FROM ghcr.io/astral-sh/uv:0.9.17"
        "@sha256:5cb6b54d2bc3fe2eb9a8483db958a0b9eebf9edff68adedb369df8e7b98711a2 "
        "AS uv"
    ) in dockerfile
    assert (
        "FROM mcr.microsoft.com/devcontainers/python:1-3.11-bookworm"
        "@sha256:b726eb94f42fcddb10056835f2c474c9f9e12e717ba2b2d2f9a8b1d78feeb68b"
    ) in dockerfile
    assert "COPY --from=uv /uv /uvx /usr/local/bin/" in dockerfile
    assert "curl -LsSf https://astral.sh/uv/install.sh | sh" not in dockerfile
    assert "/root/.local/bin" not in dockerfile


def test_devcontainer_config_matches_project_tooling() -> None:
    config = json.loads((ROOT / ".devcontainer/devcontainer.json").read_text())

    assert config["name"] == "hermes-assistant"
    assert config["build"] == {"dockerfile": "Dockerfile"}
    assert "ghcr.io/devcontainers/features/docker-outside-of-docker:1" in config["features"]
    assert config["postCreateCommand"] == "uv sync --dev"
    assert config["customizations"]["vscode"]["extensions"] == [
        "charliermarsh.ruff",
        "ms-python.python",
        "ms-python.mypy-type-checker",
    ]


def test_ci_workflow_runs_local_foundation_checks() -> None:
    workflow_text = (ROOT / ".github/workflows/ci.yml").read_text()
    workflow = cast("dict[str, Any]", yaml.safe_load(workflow_text))
    steps = cast("list[dict[str, Any]]", workflow["jobs"]["test"]["steps"])

    assert workflow["name"] == "ci"
    assert workflow["permissions"] == {"contents": "read"}
    assert "push:" in workflow_text
    assert 'branches: ["main"]' in workflow_text
    assert "pull_request:" in workflow_text
    assert workflow["jobs"]["test"]["runs-on"] == "ubuntu-latest"
    assert steps[0]["uses"] == "actions/checkout@v5"
    assert find_step(steps, "Install uv") == {
        "name": "Install uv",
        "uses": "astral-sh/setup-uv@v7",
        "with": {"version": "0.9.17"},
    }
    assert find_step(steps, "Set up Python") == {
        "name": "Set up Python",
        "uses": "actions/setup-python@v6",
        "with": {"python-version": "3.11"},
    }
    assert find_step(steps, "Install dependencies")["run"] == "uv sync --dev"
    assert find_step(steps, "Ruff")["run"] == "uv run ruff check ."
    assert find_step(steps, "Mypy")["run"] == "uv run mypy"
    assert find_step(steps, "Pytest")["run"] == "uv run pytest -q"
    assert find_step(steps, "Work safety guard")["run"] == "./scripts/check-work-safe.sh"
    assert find_step(steps, "Compose build")["run"] == (
        "docker compose -p hermes-work --profile work "
        "-f docker-compose.yml -f docker-compose.work.yml build"
    )
    assert "docker compose --profile work" not in workflow_text
