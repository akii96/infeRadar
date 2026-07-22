# InfeRadar

InfeRadar tracks merged and newly opened PRs across several LLM inference engine
repositories, bins them into deterministic labels as JSON changelogs, and
generates a high-signal markdown digest per repo from that JSON via an
OpenAI-compatible LLM endpoint.

Supported repositories:
- [ROCm/AITER](https://github.com/ROCm/aiter)
- [vllm-project/vllm](https://github.com/vllm-project/vllm)
- [sgl-project/sglang](https://github.com/sgl-project/sglang)
- [ROCm/ATOM](https://github.com/ROCm/ATOM)

The JSON is deterministic: labels come from editable path and title rules in
repository-specific YAML files, with no LLM involved; PR bodies are intentionally
ignored to avoid over-classifying copied context, checklists, and broad
release-note text. The markdown digests are derived from that JSON and live right
next to it, so each `.md` is paired one-to-one with its `.json` source of truth.

## Architecture

Generation runs in two stages so each runs where it has the access it needs:

- A GitHub Actions workflow generates the deterministic JSON for all repos and
  commits it. It uses only the built-in `GITHUB_TOKEN` (no custom secrets).
- A scheduled job reads that JSON and writes the markdown digests via the LLM
  endpoint, committing only the `.md` files. This runs wherever the endpoint and
  its credentials live, off GitHub.

The two stages touch disjoint files (JSON vs `.md`), so they never conflict; the
markdown stage does a `git pull --rebase` before pushing. No LLM credentials are
ever stored in GitHub.

## Local usage (JSON)

```bash
python -m pip install -e ".[test]"

# all configured repos
inferadar --repos-config repos.yaml --output-dir changelogs
# a single repo, or a specific window
inferadar --repo ROCm/aiter --output-dir changelogs
inferadar --repos-config repos.yaml --start 2026-05-08 --end 2026-05-15 --output-dir changelogs
```

Set `GITHUB_TOKEN` (or `GH_TOKEN`) to raise GitHub API rate limits. Some orgs
block classic PATs, so the client falls back to anonymous access for those owners
(configurable via `INFERADAR_GITHUB_RAW_OWNERS`, default `ROCm`); their busier
repos are best generated in GitHub Actions, whose built-in token can read them.

## Markdown summaries

`inferadar-summarize` reads each changelog JSON and writes a digest next to it
(`changelogs/<window>/<repo>.md`). It is idempotent: a `.md` is only
(re)generated when its recorded JSON SHA-256 fingerprint differs, or with
`--force`. Digests created before fingerprints were introduced are recognized
by their source `generated_at` value.

```bash
python -m pip install -e ".[llm]"

inferadar-summarize --changelogs-dir changelogs            # all windows, missing/stale only
inferadar-summarize --changelogs-dir changelogs --since 2026-06-28
inferadar-summarize --window latest --force                # rebuild the newest window
inferadar-summarize --start 2026-06-01 --end 2026-06-08    # one specific window
inferadar-summarize --only AITER --window latest           # a single repo
```

The endpoint is configured entirely via environment variables. Any
OpenAI-compatible `/chat/completions` endpoint works; nothing is hard-coded.
Keep these values in a local environment file, never in the repo (see
[`deploy/inferadar.env.example`](deploy/inferadar.env.example)).

| Variable | Required | Notes |
| --- | --- | --- |
| `INFERADAR_LLM_BASE_URL` | yes | Base URL incl. version path; client POSTs to `{BASE_URL}/chat/completions` |
| `INFERADAR_LLM_API_KEY` | yes | Credential for the endpoint |
| `INFERADAR_LLM_MODEL` | yes | Model name served by the endpoint |
| `INFERADAR_LLM_AUTH_HEADER` | no | Auth header name (default `Authorization`) |
| `INFERADAR_LLM_AUTH_PREFIX` | no | Value prefix (default `Bearer `; use an empty value on POSIX or `__EMPTY__` on Windows for a bare key) |
| `INFERADAR_LLM_TIMEOUT` | no | Read timeout seconds (default 300) |
| `INFERADAR_LLM_MAX_TOKENS` | no | Output token budget (default 64000) |
| `INFERADAR_LLM_MAX_TOKENS_CAP` | no | Ceiling for the empty-content retry (default 64000) |
| `INFERADAR_LLM_EMPTY_RETRIES` | no | Extra attempts on empty content, escalating the budget (default 2) |
| `INFERADAR_LLM_HTTP_RETRIES` | no | Extra attempts on transient network/408/409/425/429/5xx failures (default 3) |
| `INFERADAR_LLM_RETRY_BASE_SECONDS` | no | Initial exponential-backoff delay (default 2 seconds, capped at 30) |

Reasoning models can spend part of the output budget on hidden "thinking", which
may leave zero visible text on a tight budget; the default budget is generous and
the client retries with a doubled budget (up to `INFERADAR_LLM_MAX_TOKENS_CAP`)
if a response comes back empty. Match `INFERADAR_LLM_MAX_TOKENS` /
`INFERADAR_LLM_MAX_TOKENS_CAP` to your model's maximum output.

Each digest has a fixed shape: a `## TL;DR` (which model families got the most
attention, the most needle-moving performance PRs), `## Most important PRs` (the
top few, written up), then `## More changes by area` where the long tail is
grouped into collapsed `<details>` boxes by type of work, one line per PR. The
visible content (outside the boxes) is sized for a ~60-75 second read.

Notification-safe by design: digests contain no `@mentions`, PR references are
emitted as full-URL links, and commit messages are sanitized, so generating and
committing summaries never pings a PR author.

## Output layout

```text
changelogs/
└── 2026-06-01_to_2026-06-08/
    ├── AITER.json   + AITER.md
    ├── vllm.json    + vllm.md
    ├── sglang.json  + sglang.md
    └── ATOM.json    + ATOM.md
```

Each JSON artifact includes the query window, state counts, primary and auxiliary
label counts, PR metadata, changed files, commit SHAs, labels, and capped rule
reasons. Merged PRs receive the `merged` label; PRs opened during the same window
receive `open_pr`.

## Configuration

Repositories are configured in `repos.yaml`, each with its own rules file:

```yaml
repos:
  - name: AITER
    github: ROCm/AITER
    rules: rules/rules-aiter.yaml
  - name: vllm
    github: vllm-project/vllm
    rules: rules/rules-vllm.yaml
```

## Deployment

- `.github/workflows/generate-changelogs.yml` generates and commits the JSON for
  all repos on a schedule and on manual dispatch, using only the built-in token.
- `.github/workflows/ci.yml` runs `pytest` on push, pull request, and dispatch.
- The markdown stage runs off GitHub on a schedule (`deploy/run-inferadar.sh`,
  with a sample systemd service/timer in `deploy/`). It needs the LLM endpoint
  config and a git push credential; see the comments in `deploy/` for setup.

### Windows laptop automation

Windows uses a native PowerShell backlog runner and a per-user Scheduled Task:

```powershell
cd C:\infeRadar
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\deploy\install-windows-task.ps1

# Fill in the gateway values in the private file printed by the installer, then:
Enable-ScheduledTask -TaskName "InfeRadar Markdown Summaries"
Start-ScheduledTask -TaskName "InfeRadar Markdown Summaries"
```

The private config is `%LOCALAPPDATA%\InfeRadar\inferadar.env`; its ACL is
restricted to the current user. Set `INFERADAR_SUMMARY_SINCE` there to keep
intentional historical/manual JSON windows out of the backlog. Logs are written
under `%LOCALAPPDATA%\InfeRadar\logs`.

The task runs at logon and every 24 hours, starts missed work when Windows is
available again, and ignores overlapping invocations. Each run scans every
eligible JSON rather than only the latest window, commits successful summaries
even when another file fails, and leaves failures in the backlog for a later
retry. It can therefore catch up after sleep, shutdown, VPN loss, gateway
outage, or a transient push failure. It cannot execute while the laptop is off,
and VPN-dependent work waits until the laptop is awake and the VPN is connected.

Useful commands:

```powershell
Get-ScheduledTask -TaskName "InfeRadar Markdown Summaries"
Get-ScheduledTaskInfo -TaskName "InfeRadar Markdown Summaries"
Start-ScheduledTask -TaskName "InfeRadar Markdown Summaries"
Get-Content "$env:LOCALAPPDATA\InfeRadar\logs\stage2-$(Get-Date -Format yyyy-MM-dd).log" -Wait

# One-repository smoke test; creates a local commit but does not push it.
.\deploy\run-inferadar.ps1 -Only AITER -Limit 1 -SkipPush
```

## Security

- LLM endpoint credentials live only in the local environment file on the
  machine that runs the markdown stage; they are never GitHub secrets, never
  committed, and never printed.
- GitHub Actions uses only the built-in `GITHUB_TOKEN` (no custom secrets), so a
  fork pull request has nothing to exfiltrate.
- Generated markdown has no `@mentions` and links PRs by full URL; commit
  messages are sanitized, so committing never cross-references or notifies a PR.
