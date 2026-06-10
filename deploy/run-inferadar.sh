#!/usr/bin/env bash
#
# Markdown stage of the InfeRadar pipeline (runs on the internal server).
#
# GitHub Actions generates the changelog JSON in the cloud, because its built-in
# token can read ROCm repos that block classic PATs. This script pulls that JSON
# and writes the high-signal markdown digests via the internal LLM gateway, then
# commits and pushes ONLY the .md files. JSON (Actions) and markdown (here) are
# disjoint files, so the two writers never conflict; we pull --rebase before
# pushing and retry a few times in case Actions pushed concurrently.
#
# Usage:
#   deploy/run-inferadar.sh                          # summarize the latest window
#   deploy/run-inferadar.sh 2026-06-06 2026-06-10    # a specific window (both dates)
#
# Config (environment, normally via /etc/inferadar/inferadar.env):
#   INFERADAR_LLM_BASE_URL, INFERADAR_LLM_API_KEY, INFERADAR_LLM_MODEL
#   INFERADAR_LLM_AUTH_HEADER, INFERADAR_LLM_AUTH_PREFIX, INFERADAR_LLM_MAX_TOKENS
#   PYTHON                   python interpreter with inferadar installed (default: python3)
#   INFERADAR_ENV_FILE       env file to source for manual runs (default: /etc/inferadar/inferadar.env)
#   INFERADAR_SKIP_PUSH=1    generate + commit but do not push (testing)
#
# Note: this stage does NOT call the GitHub API (no GITHUB_TOKEN needed). It only
# needs the LLM gateway config and git push credentials (SSH deploy key, or an
# HTTPS remote with a stored token).
set -euo pipefail

START="${1:-}"
END="${2:-}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_DIR}"

log() { printf '[%s] %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*"; }

# Load the env file only when the gateway config isn't already present (manual
# runs). Under systemd the EnvironmentFile already populates these.
ENV_FILE="${INFERADAR_ENV_FILE:-/etc/inferadar/inferadar.env}"
if [[ -z "${INFERADAR_LLM_BASE_URL:-}" && -f "${ENV_FILE}" ]]; then
  log "Sourcing ${ENV_FILE}"
  set -a
  # shellcheck disable=SC1090
  source "${ENV_FILE}"
  set +a
fi

PYTHON="${PYTHON:-python3}"

# Commit/rebase identity via env vars (no git config changes, and rebases never
# fail on an unknown identity).
export GIT_AUTHOR_NAME="inferadar-bot"
export GIT_AUTHOR_EMAIL="inferadar-bot@users.noreply.github.com"
export GIT_COMMITTER_NAME="inferadar-bot"
export GIT_COMMITTER_EMAIL="inferadar-bot@users.noreply.github.com"

if [[ -n "${START}" && -z "${END}" ]] || [[ -z "${START}" && -n "${END}" ]]; then
  log "ERROR: provide both START and END dates, or neither"
  exit 2
fi

log "Markdown stage start (repo: ${REPO_DIR}, python: ${PYTHON})"

# 1) Sync to the latest committed JSON (whatever Actions pushed).
log "git pull --rebase"
git pull --rebase --autostash origin main

# 2) Generate markdown for JSON that lacks an up-to-date .md (idempotent).
sum_args=(--changelogs-dir changelogs)
if [[ -n "${START}" && -n "${END}" ]]; then
  sum_args+=(--start "${START}" --end "${END}")
else
  sum_args+=(--window latest)
fi
log "inferadar-summarize ${sum_args[*]}"
"${PYTHON}" -m inferadar.summarize "${sum_args[@]}"

# 3) Commit only the markdown (disjoint from the Actions JSON commits).
if [[ -z "$(git status --porcelain -- changelogs)" ]]; then
  log "No new summaries to commit."
  exit 0
fi
git add changelogs/
git commit -m "Add changelog summaries"

if [[ "${INFERADAR_SKIP_PUSH:-0}" == "1" ]]; then
  log "INFERADAR_SKIP_PUSH=1 set; not pushing."
  exit 0
fi

# 4) Push, rebasing onto any concurrent Actions JSON push (disjoint = clean).
for attempt in 1 2 3; do
  if git push; then
    log "Pushed."
    log "Markdown stage done."
    git log --oneline -1
    exit 0
  fi
  log "Push rejected (attempt ${attempt}); rebasing on latest and retrying."
  git pull --rebase --autostash origin main
  sleep 3
done
log "ERROR: push still failing after retries."
exit 1
