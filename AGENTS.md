# Agent Instructions

Your job is to be correct, not agreeable. Say when a proposed direction is unsafe, non-ideal, or not supported by the code.

## Project Posture

- This repo defines a personal/work assistant on Hermes Agent.
- This is not a coding assistant and must not become one.
- Personal and work profiles must stay isolated.
- Work profile development on a corporate laptop must default to local mocks and sanitized config.
- Do not put secrets, real work exports, real transcripts, or personal API keys in git.
- Do not add Microsoft Graph app registration flows, write scopes, or external messaging gateways to the work profile.

## Engineering Standards

- Use `uv` for Python dependency management.
- Run `uv run ruff check .`, `uv run mypy`, and `uv run pytest` before claiming completion.
- Prefer small focused files and testable services.
- Keep generated state under ignored `data/`, `state/`, or `logs/` directories.
