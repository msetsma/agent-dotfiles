import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_required_foundation_files_exist() -> None:
    required = [
        "AGENTS.md",
        "README.md",
        "ARCHITECTURE.md",
        "pyproject.toml",
        ".python-version",
        "docker-compose.yml",
        "docker-compose.personal.yml",
        "docker-compose.work.yml",
        ".github/workflows/ci.yml",
    ]

    missing = [path for path in required if not (ROOT / path).exists()]

    assert missing == []


def test_python_project_is_strict_and_pinned() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text())

    assert pyproject["project"]["requires-python"] == ">=3.11,<3.12"
    assert (
        "hermes-agent[anthropic,azure-identity,cron,web]==0.16.0"
        in pyproject["project"]["dependencies"]
    )
    assert pyproject["tool"]["ruff"]["line-length"] == 100
    assert pyproject["tool"]["mypy"]["strict"] is True


def test_readme_documents_work_safe_defaults() -> None:
    readme = (ROOT / "README.md").read_text()

    assert "Work-safe default" in readme
    assert "mock model endpoint" in readme
    assert "docker compose -p hermes-work --profile work" in readme


def test_architecture_documents_profile_isolation() -> None:
    architecture = (ROOT / "ARCHITECTURE.md").read_text()

    assert "Profile isolation" in architecture
    assert "Separate Hermes homes" in architecture
    assert "RAG is a later phase" in architecture
