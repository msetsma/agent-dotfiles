import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_script(path: str) -> str:
    return (ROOT / path).read_text()


def test_smoke_scripts_exist_and_are_executable() -> None:
    for path in [
        "scripts/check-work-safe.sh",
        "scripts/smoke-work.sh",
        "scripts/smoke-personal.sh",
    ]:
        script = ROOT / path

        assert script.exists()
        assert os.access(script, os.X_OK)


def test_work_safety_guard_rejects_external_work_settings() -> None:
    script = read_script("scripts/check-work-safe.sh")

    for forbidden in [
        "TELEGRAM_",
        "DISCORD_",
        "SLACK_",
        "SIGNAL_",
        "TEAMS_CLIENT",
        "GRAPH_",
        "AZURE",
        "FOUNDRY",
        "WORK_GITHUB_TOKEN",
        "AZURE_DEVOPS_PAT",
        "CLIENT_SECRET",
    ]:
        assert forbidden in script

    assert "work profile safety check passed" in script
    assert "docker-compose.work.yml" in script
    assert "config/work" in script
    assert "config/hermes/work.yaml" in script
    assert "repo_root=" in script
    assert "grep -R -F --" in script
    assert "status=$?" in script
    assert "Work safety scan failed for pattern:" in script


def test_work_safety_guard_runs_from_outside_repo_root() -> None:
    result = subprocess.run(
        [str(ROOT / "scripts/check-work-safe.sh")],
        cwd="/tmp",
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert "work profile safety check passed" in result.stdout


def test_work_safety_guard_fails_when_scan_paths_are_missing(tmp_path: Path) -> None:
    fixture = tmp_path / "repo"
    shutil.copytree(ROOT / "scripts", fixture / "scripts")

    result = subprocess.run(
        [str(fixture / "scripts/check-work-safe.sh")],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "Missing work safety scan path:" in result.stderr


def test_smoke_scripts_use_explicit_project_names_and_local_mock() -> None:
    work = read_script("scripts/smoke-work.sh")
    personal = read_script("scripts/smoke-personal.sh")

    assert "docker compose -p hermes-work --profile work" in work
    assert "docker compose -p hermes-personal --profile personal" in personal
    assert "mock-work-safe" in work
    assert "mock-work-safe" in personal
    assert "foundation smoke passed" in work
    assert "foundation smoke passed" in personal
    assert "hermes -z" in work
    assert "hermes -z" in personal
    assert "hermes doctor" not in work
    assert "hermes doctor" not in personal


def test_work_smoke_verifies_no_agent_cron() -> None:
    script = read_script("scripts/smoke-work.sh")

    assert "hermes cron create" in script
    assert "--no-agent" in script
    assert "marker=\"foundation cron fired ${run_id}\"" in script
    assert "--name \"${job_name}\"" in script
    assert "hermes cron run \"${job_name}\"" in script
    assert "foundation cron fired" in script
