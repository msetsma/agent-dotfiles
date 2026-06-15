# Architecture

## Profile isolation

Personal and work are two deployment profiles over one codebase. They must use separate Hermes homes, separate data directories, separate compose project names, and separate runtime secrets.

Compose invocations must set explicit project names so profile resources do not share networks, containers, or named volumes:

- Work: `docker compose -p hermes-work --profile work -f docker-compose.yml -f docker-compose.work.yml ...`
- Personal: `docker compose -p hermes-personal --profile personal -f docker-compose.yml -f docker-compose.personal.yml ...`

## Separate Hermes homes

- Personal profile runtime state lives in the Docker named volume `hermes-personal-state`, mounted at `HERMES_HOME=/opt/data/personal`.
- Work profile runtime state lives in the Docker named volume `hermes-work-state`, mounted at `HERMES_HOME=/opt/data/work`.
- Tests and smoke scripts may still use repo-local generated paths such as `state/test`.
- Repo-local `state/`, `data/`, and `logs/` remain ignored by git for future generated host state and logs.

## Phase 1 Runtime

Phase 1 runs Hermes Agent `0.16.0`, pinned to upstream release tag `v2026.6.5`, behind Docker Compose profile files. Smoke tests use `services/mock_model`, a local OpenAI-compatible endpoint, so the work laptop can validate orchestration without sending data to external model providers.

## RAG is a later phase

The RAG service, ingest watcher, Qdrant schema, chunking, retrieval fusion, and eval harness are not implemented in Phase 1. They are the next major implementation plan after the foundation is reproducible and CI is green.

## Work restrictions

The work profile is read-only and localhost-only during Phase 1. It must not define Telegram, Discord, Slack, Signal, Teams bot, or Microsoft Graph application settings. Future work integrations use local exports, existing read-only credentials, and allowlisted wrapper scripts.
