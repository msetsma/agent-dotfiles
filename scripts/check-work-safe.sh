#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

work_paths=(
  "${repo_root}/docker-compose.work.yml"
  "${repo_root}/config/work"
  "${repo_root}/config/hermes/work.yaml"
)

for path in "${work_paths[@]}"; do
  if [[ ! -e "${path}" ]]; then
    echo "Missing work safety scan path: ${path}" >&2
    exit 1
  fi
done

for pattern in \
  TELEGRAM_ \
  DISCORD_ \
  SLACK_ \
  SIGNAL_ \
  TEAMS_CLIENT \
  GRAPH_ \
  AZURE \
  FOUNDRY \
  WORK_GITHUB_TOKEN \
  AZURE_DEVOPS_PAT \
  CLIENT_SECRET
do
  set +e
  grep -R -F -- "${pattern}" "${work_paths[@]}"
  status=$?
  set -e

  if [[ ${status} -eq 0 ]]; then
    echo "Forbidden work-profile setting found: ${pattern}" >&2
    exit 1
  fi
  if [[ ${status} -ne 1 ]]; then
    echo "Work safety scan failed for pattern: ${pattern}" >&2
    exit 1
  fi
done

set +e
grep -R -F -- "0.0.0.0" "${work_paths[@]}"
status=$?
set -e

if [[ ${status} -eq 0 ]]; then
  echo "Work profile must bind localhost only" >&2
  exit 1
fi
if [[ ${status} -ne 1 ]]; then
  echo "Work safety scan failed for pattern: 0.0.0.0" >&2
  exit 1
fi

echo "work profile safety check passed"
