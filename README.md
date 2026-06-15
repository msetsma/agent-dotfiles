# Hermes Assistant

A two-profile Hermes Agent foundation for a persistent personal/work assistant.

## Work-safe default

This repository is being developed on a work computer. The default validation path uses a mock model endpoint and sanitized config. It does not call Anthropic, Azure AI Foundry, Telegram, Microsoft Graph, Outlook, Teams, OneDrive, Azure DevOps, or GitHub.

## Profiles

- `personal`: local Hermes runtime configured for the future personal assistant profile.
- `work`: local Hermes runtime configured for corporate-machine development with no external messaging gateway and no Microsoft Graph app registration flow.

## Quickstart

```bash
uv sync --dev
uv run ruff check .
uv run mypy
uv run pytest
```

Run the work-safe smoke stack:

```bash
docker compose -p hermes-work --profile work -f docker-compose.yml -f docker-compose.work.yml up --build --abort-on-container-exit --exit-code-from hermes-work
```

Run the personal smoke stack only on a personal machine or when using synthetic prompts:

```bash
docker compose -p hermes-personal --profile personal -f docker-compose.yml -f docker-compose.personal.yml up --build --abort-on-container-exit --exit-code-from hermes-personal
```

## Current Phase

Phase 1 establishes repo standards, pinned Hermes runtime wiring, compose profiles, a mock model endpoint, and CI. RAG, ingestion, personal connectors, work connectors, and portfolio polish come after this foundation is green.

## Phase 1 Verification

The foundation is complete when these commands pass:

```bash
uv run ruff check .
uv run mypy
uv run pytest -q
./scripts/check-work-safe.sh
./scripts/smoke-work.sh
```

On a work computer, `./scripts/smoke-work.sh` is the required runtime check because it uses only the local mock model endpoint and sanitized work profile config.
