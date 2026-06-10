#!/usr/bin/env bash
#
# Sequential InfeRadar pipeline for an internal server:
#   git pull  ->  generate JSON (deterministic)  ->  generate markdown (LLM via
#   the internal gateway)  ->  commit JSON + MD together  ->  push.
#
# The markdown step needs the internal LLM gateway, which is unreachable from
# GitHub's cloud, so the whole pipeline runs here. The gateway key lives only in
# the env file on this server and never touches GitHub.
#
# Usage:
#   deploy/run-inferadar.sh                          # default: last 4-day window
#   deploy/run-inferadar.sh 2026-06-01 2026-06-08    # custom window (both dates)
#
# Config (environment, normally via /etc/inferadar/inferadar.env):
#   INFERADAR_LLM_BASE_URL, INFERADAR_LLM_API_KEY, INFERADAR_LLM_MODEL
#   GITHUB_TOKEN              raises GitHub API rate limits for JSON generation
#   PYTHON                   python interpreter with inferadar installed (default: python3)
#   INFERADAR_ENV_FILE       env file to source for manual runs (default: /etc/inferadar/inferadar.env)
#   INFERADAR_SKIP_PUSH=1    generate + commit but do not push (testing)
#   INFERADAR_SKIP_CLEANUP=1 do not delete windows older than 60 days
set -euo pipefail

START="${1:-}"
END="${2:-}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_DIR}"

log() { printf '[%s] %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*"; }

# Load the env file only when the gateway config isn't already present (e.g. for
# manual runs). Under systemd the EnvironmentFile already populates these, so we
# skip sourcing and avoid any shell-vs-systemd parsing differences.
ENV_FILE="${INFERADAR_ENV_FILE:-/etc/inferadar/inferadar.env}"
if [[ -z "${INFERADAR_LLM_BASE_URL:-}" && -f "${ENV_FILE}" ]]; then
  log "Sourcing ${ENV_FILE}"
  set -a
  # shellcheck disable=SC1090
  source "${ENV_FILE}"
  set +a
fi

PYTHON="${PYTHON:-python3}"

if [[ -n "${START}" && -z "${END}" ]] || [[ -z "${START}" && -n "${END}" ]]; then
  log "ERROR: provide both START and END dates, or neither"
  exit 2
fi

log "Pipeline start (repo: ${REPO_DIR}, python: ${PYTHON})"

# 1) Sync so we build on the latest committed changelogs.
log "git pull --ff-only"
git pull --ff-only

# 2) Generate the deterministic JSON (public GitHub API).
gen_args=(--output-dir changelogs --repos-config repos.yaml)
if [[ -n "${START}" && -n "${END}" ]]; then
  gen_args+=(--start "${START}" --end "${END}")
fi
log "Generating JSON: inferadar ${gen_args[*]}"
"${PYTHON}" -m inferadar.cli "${gen_args[@]}"

# 3) Generate markdown from that JSON via the internal gateway. Resilient: a
#    summarize failure must not block committing the JSON source of truth.
sum_args=(--changelogs-dir changelogs)
if [[ -n "${START}" && -n "${END}" ]]; then
  sum_args+=(--start "${START}" --end "${END}")
fi
log "Generating markdown: inferadar-summarize ${sum_args[*]}"
if ! "${PYTHON}" -m inferadar.summarize "${sum_args[@]}"; then
  log "WARNING: markdown generation reported errors; continuing to commit JSON"
fi

# 4) Prune windows older than 60 days (mirrors the original workflow). Skipped
#    for explicit custom-date runs so backfills don't trigger deletions.
if [[ "${INFERADAR_SKIP_CLEANUP:-0}" != "1" && -z "${START}" ]]; then
  log "Pruning changelog windows older than 60 days"
  find changelogs -type d -name "*_to_*" -mtime +60 -exec rm -rf {} + || true
fi

# 5) Commit JSON + MD together with a sanitized message (no '#NNNN' refs, no '@')
#    so committing never cross-references or notifies a PR author.
if [[ -z "$(git status --porcelain -- changelogs)" ]]; then
  log "No changelog changes to commit."
  exit 0
fi
WINDOW="$(ls -dt changelogs/*_to_* 2>/dev/null | head -1 | xargs -r -n1 basename || true)"
MSG="Update changelog and summaries${WINDOW:+ for ${WINDOW}}"
log "Committing: ${MSG}"
git add changelogs/
git -c user.name="inferadar-bot" \
    -c user.email="inferadar-bot@users.noreply.github.com" \
    commit -m "${MSG}"

if [[ "${INFERADAR_SKIP_PUSH:-0}" == "1" ]]; then
  log "INFERADAR_SKIP_PUSH=1 set; not pushing."
  exit 0
fi
log "git push"
git push
log "Pipeline done."
