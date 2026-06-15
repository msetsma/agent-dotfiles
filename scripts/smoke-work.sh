#!/usr/bin/env bash
set -euo pipefail

compose=(docker compose -p hermes-work --profile work -f docker-compose.yml -f docker-compose.work.yml)

cleanup() {
  "${compose[@]}" down --remove-orphans >/dev/null 2>&1 || true
}
trap cleanup EXIT

./scripts/check-work-safe.sh

"${compose[@]}" build
"${compose[@]}" up --abort-on-container-exit --exit-code-from hermes-work

turn_output="$(
  "${compose[@]}" run --rm hermes-work \
    hermes -z "Return exactly: foundation smoke passed" \
    --provider openai-api \
    --model mock-work-safe \
    --ignore-user-config \
    --ignore-rules
)"

printf '%s\n' "${turn_output}" | grep -F "foundation smoke passed"

"${compose[@]}" run --rm --entrypoint /bin/sh hermes-work -lc '
  set -e
  run_id="$(date +%s)"
  job_name="foundation-cron-${run_id}"
  marker="foundation cron fired ${run_id}"
  mkdir -p /opt/data/work/scripts
  printf "%s\n" "#!/usr/bin/env bash" "echo ${marker}" > /opt/data/work/scripts/foundation-cron.sh
  chmod +x /opt/data/work/scripts/foundation-cron.sh
  hermes cron create "30m" "foundation cron" --no-agent --script foundation-cron.sh --name "${job_name}" --deliver local
  hermes cron run "${job_name}"
  hermes cron tick
  grep -R "${marker}" /opt/data/work/cron/output
'
