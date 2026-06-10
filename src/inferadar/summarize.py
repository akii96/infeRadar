"""LLM markdown summaries for InfeRadar changelog JSON.

This reads the deterministic per-repo changelog JSON produced by ``inferadar``
and writes a high-signal markdown digest next to each JSON file (same window
directory, same stem, ``.md`` extension). The digest is designed to be skimmed
in about 60-75 seconds: a high-level summary plus the few most important PRs are
always visible, and the long tail is tucked into collapsed ``<details>`` boxes
grouped by type of work, which do not count toward the read budget.

The LLM is reached through any OpenAI-compatible chat-completions endpoint (for
example an internal company gateway), configured entirely via environment
variables so no provider, base URL, key, or model name is ever hard-coded:

    INFERADAR_LLM_BASE_URL   base URL incl. version path, e.g. https://gw.internal/v1
    INFERADAR_LLM_API_KEY    bearer token for the gateway
    INFERADAR_LLM_MODEL      model name served by the gateway
    INFERADAR_LLM_TIMEOUT    optional read timeout in seconds (default 300)
    INFERADAR_LLM_MAX_TOKENS optional output token budget (default 64000)
    INFERADAR_LLM_MAX_TOKENS_CAP   optional ceiling for the empty-content retry (default 64000)
    INFERADAR_LLM_EMPTY_RETRIES    optional extra attempts on empty content (default 2)

Notification safety: the generated markdown never contains "@" mentions, and PR
references are emitted as full-URL links. Neither @mentions nor full URLs inside
committed repository files create cross-reference pings, so generating and
committing these summaries never notifies a PR author.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Callable

ENV_BASE_URL = "INFERADAR_LLM_BASE_URL"
ENV_API_KEY = "INFERADAR_LLM_API_KEY"
ENV_MODEL = "INFERADAR_LLM_MODEL"
ENV_TIMEOUT = "INFERADAR_LLM_TIMEOUT"
ENV_MAX_TOKENS = "INFERADAR_LLM_MAX_TOKENS"
ENV_MAX_TOKENS_CAP = "INFERADAR_LLM_MAX_TOKENS_CAP"
ENV_EMPTY_RETRIES = "INFERADAR_LLM_EMPTY_RETRIES"
ENV_AUTH_HEADER = "INFERADAR_LLM_AUTH_HEADER"
ENV_AUTH_PREFIX = "INFERADAR_LLM_AUTH_PREFIX"

DEFAULT_TIMEOUT = 300.0
# Default to a generous budget so reasoning models (whose "thinking" tokens count
# against the output budget) don't return empty content. Override per model via
# env; match this to the configured model's maximum output.
DEFAULT_MAX_TOKENS = 64000
# Upper bound the escalating retry will not exceed (keeps us within model limits;
# most served models cap at 64k-128k output). Override via INFERADAR_LLM_MAX_TOKENS_CAP.
DEFAULT_MAX_TOKENS_CAP = 64000
# How many extra attempts (with an escalated budget) to make when the model
# returns empty content. Override via INFERADAR_LLM_EMPTY_RETRIES.
DEFAULT_EMPTY_RETRIES = 2
TEMPERATURE = 0.2
DEFAULT_AUTH_HEADER = "Authorization"
DEFAULT_AUTH_PREFIX = "Bearer "

STATE_LABELS = {"merged", "open_pr"}
MAX_PRS_PER_STATE = 200
MAX_TITLE_CHARS = 160
MAX_LABELS_IN_DISTRIBUTION = 25

WINDOW_DIR_RE = re.compile(r"^\d{4}-\d{2}-\d{2}_to_\d{4}-\d{2}-\d{2}$")

#: A callable that takes (system_prompt, user_message) and returns the model text.
LLMCallable = Callable[[str, str], str]


SYSTEM_PROMPT = """\
You are a senior LLM-inference-engine engineer writing a high-signal change \
digest for ONE repository, for a busy engineer who wants to understand what \
actually moved this period - not read a list of PR titles.

You receive deterministic data extracted from the repo's merged and \
newly-opened pull requests for a date window: per-PR title, number, state \
(merged vs newly opened), code-churn size, and normalized labels (type:*, \
component:*, kernel:*, backend:*, hardware:*, arch:*, model:*), plus aggregate \
label counts.

Write GitHub-flavored markdown with EXACTLY these sections, in order. Do not add \
an H1 title (one is added for you). Omit any section that would be empty.

## TL;DR
3 to 5 bullets. Lead with which model families got the most attention this \
window and the most needle-moving performance work (throughput, latency, \
memory, kernel / MoE / quantization / attention wins). State the overall \
direction. This is the most important part.

## Most important PRs
Up to 5 PRs, highest-signal only (big perf wins, major features, significant \
kernels or architecture). For each: a single bold line starting with the PR \
reference, then 1 to 2 sentences on what it does and why it matters. Do not \
merely restate the title - explain the change.

## More changes by area
Everything else, grouped by type of work into COLLAPSED <details> boxes (one \
per area that has content). Use this exact shape:

<details>
<summary>Area name (N)</summary>

- #1234 one-line description of what it does
- #1235 one-line description

</details>

Choose areas from: Performance, Kernels & attention, MoE & quantization, Model \
support, Parallelism & scheduling, Hardware & arch, API & serving, Tests, \
CI & build, Docs, Bugfixes, Refactors, Other. Use the labels to decide. Every \
remaining PR appears exactly once as a single line. If an area has many \
low-importance PRs (for example tests or CI), you may fold the least \
significant into one summarizing bullet like "- plus N more minor CI updates".

Hard rules:
- READ-TIME BUDGET: the VISIBLE content (TL;DR + Most important PRs, i.e. \
everything OUTSIDE the <details> boxes) must be readable in 60 to 75 seconds - \
keep it under about 350 words total, TL;DR at most 5 bullets, Most important PRs \
at most 5. The collapsed boxes do not count toward this budget.
- Reference every PR as a bare `#1234`. Do NOT write URLs or markdown links - \
they are added automatically. Use only PR numbers present in the provided data; \
never invent numbers, titles, authors, or facts.
- Never use the "@" character or @mentions anywhere. Do not credit authors by \
handle (omit authors).
- Distinguish merged work from newly-opened (in-progress) work where it matters.
- Be concrete and technical (name the kernel, attention variant, quant scheme, \
MoE path, parallelism strategy, hardware/arch, model family). Avoid filler.
- Output only the markdown body. No preamble, no closing remarks.
"""


def _pr_size(pr: dict[str, Any]) -> tuple[int, int, int]:
    """Return (total_churn, additions, deletions) across a PR's changed files."""
    additions = 0
    deletions = 0
    for file_item in pr.get("changed_files", []) or []:
        additions += int(file_item.get("additions", 0) or 0)
        deletions += int(file_item.get("deletions", 0) or 0)
    return additions + deletions, additions, deletions


def _clean_title(title: str) -> str:
    flat = " ".join(str(title).split())
    if len(flat) > MAX_TITLE_CHARS:
        flat = flat[: MAX_TITLE_CHARS - 1].rstrip() + "\u2026"
    return flat


def _pr_labels(pr: dict[str, Any]) -> list[str]:
    return sorted(set(pr.get("labels", []) or []) - STATE_LABELS)


def _pr_line(pr: dict[str, Any]) -> str:
    churn, adds, dels = _pr_size(pr)
    files = len(pr.get("changed_files", []) or [])
    commits = len(pr.get("commit_shas", []) or [])
    labels = ", ".join(_pr_labels(pr)) or "(none)"
    return (
        f'- #{pr.get("number")} "{_clean_title(pr.get("title", ""))}" '
        f"| size:{churn} (+{adds}/-{dels}), files:{files}, commits:{commits} "
        f"| {labels}"
    )


def render_input(artifact: dict[str, Any], *, max_prs: int = MAX_PRS_PER_STATE) -> str:
    """Flatten one changelog JSON artifact into a compact prompt message."""
    summary = artifact.get("summary", {}) or {}
    state_counts = summary.get("state_counts", {}) or {}
    label_counts = summary.get("label_counts", {}) or {}
    merged = int(state_counts.get("merged", 0) or 0)
    opened = int(state_counts.get("open_pr", 0) or 0)

    model_counts = sorted(
        (
            (label, count)
            for label, count in label_counts.items()
            if label.startswith("model:") and label != "model:general"
        ),
        key=lambda kv: (-kv[1], kv[0]),
    )
    distribution = sorted(
        ((label, count) for label, count in label_counts.items() if label not in STATE_LABELS),
        key=lambda kv: (-kv[1], kv[0]),
    )[:MAX_LABELS_IN_DISTRIBUTION]

    prs = artifact.get("prs", []) or []
    merged_prs = sorted(
        (pr for pr in prs if pr.get("state") == "merged"),
        key=lambda pr: -_pr_size(pr)[0],
    )
    open_prs = sorted(
        (pr for pr in prs if pr.get("state") == "open_pr"),
        key=lambda pr: -_pr_size(pr)[0],
    )

    lines: list[str] = []
    lines.append(f"Repository: {artifact.get('source_repo', '')}")
    lines.append(f"Window: {artifact.get('period_start', '')} to {artifact.get('period_end', '')}")
    lines.append(
        f"Activity: {merged} merged, {opened} newly opened, "
        f"{summary.get('total_commits', 0)} commits, {summary.get('total_files', 0)} files touched"
    )
    lines.append("")

    lines.append("Models with most attention (by label frequency, generic excluded):")
    if model_counts:
        lines.extend(f"- {label}: {count}" for label, count in model_counts)
    else:
        lines.append("- none model-specific this window")
    lines.append("")

    lines.append(f"Label distribution (top {MAX_LABELS_IN_DISTRIBUTION}):")
    lines.extend(f"- {label}: {count}" for label, count in distribution)
    lines.append("")

    lines.append(_pr_section("Merged PRs", merged_prs, max_prs))
    lines.append("")
    lines.append(_pr_section("Newly opened PRs", open_prs, max_prs))
    return "\n".join(lines).strip() + "\n"


def _pr_section(heading: str, prs: list[dict[str, Any]], max_prs: int) -> str:
    shown = prs[:max_prs]
    hidden = len(prs) - len(shown)
    body = [f"## {heading} ({len(prs)}; sorted by churn)"]
    body.extend(_pr_line(pr) for pr in shown)
    if hidden > 0:
        body.append(f"- (+{hidden} more not shown)")
    if not shown:
        body.append("- (none)")
    return "\n".join(body)


_MENTION_RE = re.compile(r"(?<![A-Za-z0-9_])@(?=[A-Za-z0-9])")
_PR_REF_RE = re.compile(r"(?<![\w/])#(\d+)\b")


def strip_mentions(text: str) -> str:
    """Remove leading "@" from any @mention so committing never pings a user."""
    return _MENTION_RE.sub("", text)


def _pr_url_map(artifact: dict[str, Any]) -> dict[int, str]:
    mapping: dict[int, str] = {}
    for pr in artifact.get("prs", []) or []:
        number = pr.get("number")
        url = pr.get("url")
        if isinstance(number, int) and url:
            mapping[number] = str(url)
    return mapping


def linkify_pr_refs(text: str, artifact: dict[str, Any]) -> str:
    """Turn bare ``#1234`` into ``[#1234](url)`` using URLs from the JSON.

    Only PR numbers present in the artifact are linked; unknown numbers are left
    as plain text (which does not autolink inside a committed file), guarding
    against fabricated references.
    """
    url_map = _pr_url_map(artifact)

    def _replace(match: re.Match[str]) -> str:
        number = int(match.group(1))
        url = url_map.get(number)
        return f"[#{number}]({url})" if url else match.group(0)

    return _PR_REF_RE.sub(_replace, text)


def _header(artifact: dict[str, Any], display_name: str) -> str:
    summary = artifact.get("summary", {}) or {}
    state_counts = summary.get("state_counts", {}) or {}
    merged = int(state_counts.get("merged", 0) or 0)
    opened = int(state_counts.get("open_pr", 0) or 0)
    return (
        f"# {display_name}: PR digest "
        f"({artifact.get('period_start', '')} to {artifact.get('period_end', '')})\n\n"
        f"_{merged} merged, {opened} newly opened - source {artifact.get('source_repo', '')}, "
        f"generated {artifact.get('generated_at', '')}_\n\n"
    )


def _footer(display_name: str) -> str:
    return (
        "\n\n---\n_Generated by inferadar-summarize from the committed changelog "
        f"JSON ({display_name}.json), the deterministic source of truth. "
        "This file mentions no users and notifies no PRs._\n"
    )


def build_markdown(
    artifact: dict[str, Any],
    *,
    display_name: str | None = None,
    llm: LLMCallable | None = None,
) -> str:
    """Render a complete markdown digest for one changelog artifact."""
    display_name = display_name or str(artifact.get("source_repo", "repo"))
    call = llm or _default_llm
    body = call(SYSTEM_PROMPT, render_input(artifact))
    body = linkify_pr_refs(strip_mentions(body.strip()), artifact)
    return _header(artifact, display_name) + body + _footer(display_name)


def _default_llm(system: str, user: str) -> str:
    return call_llm(system, user)


def _auth_headers(api_key: str) -> dict[str, str]:
    """Build request headers. Defaults to ``Authorization: Bearer <key>``.

    For an endpoint that authenticates with a non-standard header carrying the
    bare key (no ``Bearer`` prefix), override both, e.g.:

        INFERADAR_LLM_AUTH_HEADER=X-Custom-Key
        INFERADAR_LLM_AUTH_PREFIX=        # empty: send the key with no prefix
    """
    header = os.getenv(ENV_AUTH_HEADER, DEFAULT_AUTH_HEADER).strip() or DEFAULT_AUTH_HEADER
    prefix = os.getenv(ENV_AUTH_PREFIX, DEFAULT_AUTH_PREFIX)
    return {header: f"{prefix}{api_key}", "Content-Type": "application/json"}


def call_llm(
    system: str,
    user: str,
    *,
    base_url: str | None = None,
    api_key: str | None = None,
    model: str | None = None,
    timeout: float | None = None,
    max_tokens: int | None = None,
) -> str:
    """Call any OpenAI-compatible chat-completions endpoint. Config via env by default."""
    base_url = (base_url or os.getenv(ENV_BASE_URL, "")).strip().rstrip("/")
    api_key = (api_key or os.getenv(ENV_API_KEY, "")).strip()
    model = (model or os.getenv(ENV_MODEL, "")).strip()
    if not base_url:
        raise RuntimeError(f"{ENV_BASE_URL} is not set")
    if not api_key:
        raise RuntimeError(f"{ENV_API_KEY} is not set")
    if not model:
        raise RuntimeError(f"{ENV_MODEL} is not set")
    if timeout is None:
        timeout = float(os.getenv(ENV_TIMEOUT, str(DEFAULT_TIMEOUT)))
    if max_tokens is None:
        max_tokens = _env_int(ENV_MAX_TOKENS, DEFAULT_MAX_TOKENS)
    cap = max(1, _env_int(ENV_MAX_TOKENS_CAP, DEFAULT_MAX_TOKENS_CAP))
    empty_retries = max(0, _env_int(ENV_EMPTY_RETRIES, DEFAULT_EMPTY_RETRIES))

    # Reasoning models spend part of the output budget on
    # hidden "thinking"; on a tight budget that can leave zero visible text. When
    # that happens, retry with an escalated budget (doubling, capped) instead of
    # dropping the repo. The cap keeps us within the model's max output.
    budget = min(max(max_tokens, 1), cap)
    last_error: Exception | None = None
    attempts_made = 0
    for attempt in range(empty_retries + 1):
        attempts_made = attempt + 1
        try:
            return _chat_once(base_url, api_key, model, system, user, budget, timeout)
        except _EmptyContentError as exc:
            last_error = exc
            # A non-length stop (content filter, safety, etc.) won't be fixed by a
            # bigger budget, so fail fast instead of wasting slow calls.
            if not exc.budget_related:
                break
            if budget >= cap or attempt >= empty_retries:
                break
            budget = min(budget * 2, cap)
    reason = f" (finish_reason={last_error.finish_reason})" if last_error and last_error.finish_reason else ""
    raise RuntimeError(
        f"LLM returned empty content after {attempts_made} attempt(s) "
        f"(budget up to {budget}){reason}; if truncated, raise {ENV_MAX_TOKENS_CAP}"
    ) from last_error


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return int(raw)
    except ValueError as exc:
        raise RuntimeError(f"{name} must be an integer, got {raw!r}") from exc


class _EmptyContentError(RuntimeError):
    """Internal: the model returned a well-formed response with no text content.

    ``budget_related`` is True when the empty response looks like budget
    exhaustion (finish_reason "length", or absent), so the caller knows whether
    escalating the token budget could help.
    """

    def __init__(self, message: str, *, finish_reason: str | None = None) -> None:
        super().__init__(message)
        self.finish_reason = finish_reason
        self.budget_related = finish_reason in (None, "", "length", "max_tokens")


def _chat_once(
    base_url: str,
    api_key: str,
    model: str,
    system: str,
    user: str,
    max_tokens: int,
    timeout: float,
) -> str:
    try:
        import httpx
    except ImportError as exc:  # pragma: no cover - exercised only without the extra
        raise RuntimeError(
            "httpx is required for LLM calls; install with: pip install -e '.[llm]'"
        ) from exc

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "max_tokens": max_tokens,
        "temperature": TEMPERATURE,
    }
    http_timeout = httpx.Timeout(float(timeout), connect=15.0)
    with httpx.Client(timeout=http_timeout) as client:
        response = client.post(
            f"{base_url}/chat/completions",
            headers=_auth_headers(api_key),
            json=payload,
        )
        response.raise_for_status()
        data = response.json()

    try:
        choice = data["choices"][0]
        content = choice["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(f"Unexpected LLM response shape: {str(data)[:300]}") from exc
    if not content or not str(content).strip():
        finish_reason = choice.get("finish_reason") if isinstance(choice, dict) else None
        raise _EmptyContentError("LLM returned empty content", finish_reason=finish_reason)
    return str(content).strip()


def find_window_dirs(changelogs_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in changelogs_dir.iterdir()
        if path.is_dir() and WINDOW_DIR_RE.match(path.name)
    )


def select_window_dirs(
    changelogs_dir: Path,
    window: str,
    start: str | None,
    end: str | None,
) -> list[Path]:
    if start and end:
        target = changelogs_dir / f"{start}_to_{end}"
        return [target] if target.is_dir() else []
    dirs = find_window_dirs(changelogs_dir)
    if window == "all":
        return dirs
    if window == "latest":
        return dirs[-1:]
    target = changelogs_dir / window
    return [target] if target.is_dir() else []


def find_target_jsons(
    changelogs_dir: Path,
    *,
    window: str = "all",
    start: str | None = None,
    end: str | None = None,
    only: str | None = None,
) -> list[Path]:
    targets: list[Path] = []
    for window_dir in select_window_dirs(changelogs_dir, window, start, end):
        for json_path in sorted(window_dir.glob("*.json")):
            if only and json_path.stem != only:
                continue
            targets.append(json_path)
    return targets


def summarize_artifact_file(
    json_path: Path,
    *,
    llm: LLMCallable | None = None,
    force: bool = False,
) -> tuple[Path, str]:
    """Write ``<repo>.md`` beside ``<repo>.json``. Returns (path, "written"|"skipped")."""
    md_path = json_path.with_suffix(".md")
    if not force and md_path.exists() and md_path.stat().st_mtime >= json_path.stat().st_mtime:
        return md_path, "skipped"
    artifact = json.loads(json_path.read_text(encoding="utf-8"))
    markdown = build_markdown(artifact, display_name=json_path.stem, llm=llm)
    md_path.write_text(markdown, encoding="utf-8")
    return md_path, "written"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="inferadar-summarize",
        description=(
            "Generate markdown digests from InfeRadar changelog JSON via an "
            "OpenAI-compatible LLM gateway."
        ),
    )
    parser.add_argument(
        "--changelogs-dir",
        default="changelogs",
        type=Path,
        help="Root dir holding <start>_to_<end>/<repo>.json (default: changelogs)",
    )
    parser.add_argument(
        "--window",
        default="all",
        help="'all' (default), 'latest', or a specific <start>_to_<end> directory name",
    )
    parser.add_argument("--start", help="Window start YYYY-MM-DD (use with --end to target one window)")
    parser.add_argument("--end", help="Window end YYYY-MM-DD (use with --start to target one window)")
    parser.add_argument("--only", help="Only summarize this repo (JSON stem, e.g. AITER)")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate even when the .md is newer than the .json",
    )
    parser.add_argument("--limit", type=int, help="Process at most N JSON files")
    parser.add_argument("--model", help=f"Model name (overrides ${ENV_MODEL})")
    parser.add_argument("--base-url", dest="base_url", help=f"Gateway base URL (overrides ${ENV_BASE_URL})")
    parser.add_argument(
        "--api-key",
        dest="api_key",
        help=f"API key (overrides ${ENV_API_KEY}); prefer the environment variable",
    )
    parser.add_argument("--timeout", type=float, help=f"Read timeout seconds (overrides ${ENV_TIMEOUT})")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)

    if bool(args.start) ^ bool(args.end):
        print("--start and --end must be provided together", file=sys.stderr)
        return 2

    changelogs_dir = Path(args.changelogs_dir)
    if not changelogs_dir.is_dir():
        print(f"changelogs dir not found: {changelogs_dir}", file=sys.stderr)
        return 1

    targets = find_target_jsons(
        changelogs_dir,
        window=args.window,
        start=args.start,
        end=args.end,
        only=args.only,
    )
    if args.limit is not None:
        targets = targets[: args.limit]
    if not targets:
        print("no changelog JSON files matched")
        return 0

    def llm(system: str, user: str) -> str:
        return call_llm(
            system,
            user,
            base_url=args.base_url,
            api_key=args.api_key,
            model=args.model,
            timeout=args.timeout,
        )

    written = skipped = failed = 0
    for json_path in targets:
        try:
            path, status = summarize_artifact_file(json_path, llm=llm, force=args.force)
        except Exception as exc:  # noqa: BLE001 - resilient batch: one failure must not abort the rest
            failed += 1
            print(f"ERROR {json_path}: {type(exc).__name__}: {exc}", file=sys.stderr)
            continue
        if status == "written":
            written += 1
            print(f"wrote {path}")
        else:
            skipped += 1
            print(f"skip {path} (up to date)")

    print(f"summarize: {written} written, {skipped} skipped, {failed} failed")
    return 1 if failed and not written else 0


if __name__ == "__main__":
    raise SystemExit(main())
