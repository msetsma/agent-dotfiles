from pathlib import Path
from typing import Any, cast
from urllib.parse import urlparse

import yaml  # type: ignore[import-untyped]

ROOT = Path(__file__).resolve().parents[1]


def load_compose(path: str) -> dict[str, Any]:
    return cast("dict[str, Any]", yaml.safe_load((ROOT / path).read_text()))


def test_dockerignore_excludes_high_risk_local_files() -> None:
    dockerignore = set((ROOT / ".dockerignore").read_text().splitlines())

    expected_exclusions = {
        ".git",
        ".venv",
        ".hermes/",
        ".env",
        ".env.*",
        "state/",
        "data/",
        "logs/",
        "__pycache__/",
        ".pytest_cache/",
        ".ruff_cache/",
        ".mypy_cache/",
        "build/",
        "dist/",
        "*.egg-info/",
        ".DS_Store",
        ".idea/",
        ".vscode/",
        "*.pem",
        "*.key",
        "id_*",
    }

    assert expected_exclusions <= dockerignore


def test_base_compose_does_not_set_project_name() -> None:
    compose = load_compose("docker-compose.yml")

    assert "name" not in compose


def test_base_compose_defines_mock_model() -> None:
    compose = load_compose("docker-compose.yml")
    services = compose["services"]

    assert "mock-model" in services
    assert services["mock-model"]["ports"] == ["127.0.0.1:18080:8080"]


def test_all_host_exposed_ports_bind_to_localhost() -> None:
    compose_paths = [
        "docker-compose.yml",
        "docker-compose.personal.yml",
        "docker-compose.work.yml",
    ]

    for compose_path in compose_paths:
        services = load_compose(compose_path)["services"]
        for service_name, service in services.items():
            for port in service.get("ports", []):
                assert port.startswith("127.0.0.1:"), (
                    f"{compose_path}:{service_name} exposes {port!r} outside localhost"
                )


def test_no_service_uses_host_networking() -> None:
    compose_paths = [
        "docker-compose.yml",
        "docker-compose.personal.yml",
        "docker-compose.work.yml",
    ]

    for compose_path in compose_paths:
        services = load_compose(compose_path)["services"]
        for service_name, service in services.items():
            assert service.get("network_mode") != "host", (
                f"{compose_path}:{service_name} must not use host networking"
            )


def test_hermes_profile_commands_are_local_only_smoke_checks() -> None:
    smoke_command = [
        "python",
        "-c",
        "import importlib.metadata; print(importlib.metadata.version('hermes-agent'))",
    ]

    personal = load_compose("docker-compose.personal.yml")["services"]["hermes-personal"]
    work = load_compose("docker-compose.work.yml")["services"]["hermes-work"]

    assert personal["command"] == smoke_command
    assert work["command"] == smoke_command

    for service in [personal, work]:
        command = " ".join(service["command"]).lower()
        assert "doctor" not in command
        assert "curl" not in command


def test_personal_profile_uses_separate_hermes_home() -> None:
    compose = load_compose("docker-compose.personal.yml")
    service = compose["services"]["hermes-personal"]

    assert "personal" in service["profiles"]
    assert "HERMES_HOME=/opt/data/personal" in service["environment"]
    assert "hermes-personal-state:/opt/data/personal" in service["volumes"]
    assert "hermes-personal-state" in compose["volumes"]


def test_work_profile_is_localhost_only_and_separate() -> None:
    compose = load_compose("docker-compose.work.yml")
    service = compose["services"]["hermes-work"]

    assert "work" in service["profiles"]
    assert "HERMES_HOME=/opt/data/work" in service["environment"]
    assert "hermes-work-state:/opt/data/work" in service["volumes"]
    assert "hermes-work-state" in compose["volumes"]
    assert service["ports"] == ["127.0.0.1:19119:9119"]


def test_work_profile_does_not_define_external_messaging_env() -> None:
    compose = load_compose("docker-compose.work.yml")
    environment = "\n".join(compose["services"]["hermes-work"]["environment"]).upper()

    forbidden = [
        "TELEGRAM_",
        "DISCORD_",
        "SLACK_",
        "SIGNAL_",
        "TEAMS_CLIENT",
        "GRAPH_",
        "AZURE",
        "FOUNDRY",
        "PAT",
        "TOKEN",
        "SECRET",
        "CLIENT_SECRET",
    ]

    for fragment in forbidden:
        assert fragment not in environment


def test_work_profile_uses_docker_internal_mock_model_dns_only() -> None:
    compose = load_compose("docker-compose.work.yml")
    environment = compose["services"]["hermes-work"]["environment"]
    values = dict(item.split("=", 1) for item in environment)

    base_url = urlparse(values["OPENAI_BASE_URL"])

    assert values["OPENAI_API_KEY"] == "mock"
    assert base_url.scheme == "http"
    assert base_url.hostname == "mock-model"
    assert base_url.port == 8080
    assert base_url.path == "/v1"


def test_docker_base_images_are_digest_pinned() -> None:
    hermes_dockerfile = (ROOT / "services/hermes/Dockerfile").read_text()
    compose = load_compose("docker-compose.yml")
    mock_dockerfile = compose["services"]["mock-model"]["build"]["dockerfile_inline"]

    pinned_python = (
        "python:3.11-slim-bookworm"
        "@sha256:e2d3af735aff6eeee600b1933bedd99da6645fedf572cc12ef4cc1331f2ceebe"
    )

    assert f"FROM {pinned_python}" in hermes_dockerfile
    assert f"FROM {pinned_python}" in mock_dockerfile


def test_mock_model_inline_dockerfile_runs_as_non_root() -> None:
    compose = load_compose("docker-compose.yml")
    mock_dockerfile = compose["services"]["mock-model"]["build"]["dockerfile_inline"]

    assert "useradd --create-home --uid 10002 mockmodel" in mock_dockerfile
    assert "chown -R mockmodel:mockmodel /app" in mock_dockerfile
    assert "USER mockmodel" in mock_dockerfile
    assert mock_dockerfile.index("USER mockmodel") < mock_dockerfile.index("CMD ")


def test_hermes_image_prepares_non_root_writable_state_paths() -> None:
    hermes_dockerfile = (ROOT / "services/hermes/Dockerfile").read_text()

    assert "USER hermes" in hermes_dockerfile
    assert "ENTRYPOINT" not in hermes_dockerfile
    assert 'CMD ["hermes"]' in hermes_dockerfile
    assert "/opt/data/personal" in hermes_dockerfile
    assert "/opt/data/work" in hermes_dockerfile
    assert "chown -R hermes:hermes /opt/data /workspace" in hermes_dockerfile


def test_docker_dependency_installs_use_requirements_files() -> None:
    hermes_dockerfile = (ROOT / "services/hermes/Dockerfile").read_text()
    hermes_requirements = (ROOT / "services/hermes/requirements.txt").read_text()
    mock_requirements = (ROOT / "services/mock_model/requirements.txt").read_text()
    compose = load_compose("docker-compose.yml")
    mock_dockerfile = compose["services"]["mock-model"]["build"]["dockerfile_inline"]

    assert "COPY services/hermes/requirements.txt /tmp/hermes-requirements.txt" in hermes_dockerfile
    assert "pip install --no-cache-dir -r /tmp/hermes-requirements.txt" in hermes_dockerfile
    assert "hermes-agent[anthropic,azure-identity,cron,web]==0.16.0" in hermes_requirements
    assert "Transitive dependency locking is tracked as a follow-up" in hermes_requirements

    assert (
        "COPY services/mock_model/requirements.txt /tmp/mock-model-requirements.txt"
        in mock_dockerfile
    )
    assert "pip install --no-cache-dir -r /tmp/mock-model-requirements.txt" in mock_dockerfile
    assert "fastapi==0.133.1" in mock_requirements
    assert "uvicorn[standard]==0.41.0" in mock_requirements
    assert "pydantic==2.13.4" in mock_requirements
    assert "Transitive dependency locking is tracked as a follow-up" in mock_requirements


def test_docs_require_explicit_compose_project_names() -> None:
    readme = (ROOT / "README.md").read_text()
    architecture = (ROOT / "ARCHITECTURE.md").read_text()
    docs = readme + "\n" + architecture

    assert (
        "docker compose -p hermes-work --profile work "
        "-f docker-compose.yml -f docker-compose.work.yml"
    ) in docs
    assert (
        "docker compose -p hermes-personal --profile personal "
        "-f docker-compose.yml -f docker-compose.personal.yml"
    ) in docs
    assert "docker compose --profile work" not in docs
    assert "docker compose --profile personal" not in docs
