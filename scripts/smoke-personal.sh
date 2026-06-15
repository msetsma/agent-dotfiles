#!/usr/bin/env bash
set -euo pipefail

compose=(docker compose -p hermes-personal --profile personal -f docker-compose.yml -f docker-compose.personal.yml)

cleanup() {
  "${compose[@]}" down --remove-orphans >/dev/null 2>&1 || true
}
trap cleanup EXIT

"${compose[@]}" build
"${compose[@]}" up --abort-on-container-exit --exit-code-from hermes-personal

turn_output="$(
  "${compose[@]}" run --rm hermes-personal \
    hermes -z "Return exactly: foundation smoke passed" \
    --provider openai-api \
    --model mock-work-safe \
    --ignore-user-config \
    --ignore-rules
)"

printf '%s\n' "${turn_output}" | grep -F "foundation smoke passed"
