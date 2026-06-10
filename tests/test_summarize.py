from __future__ import annotations

import json
import os

import pytest

from inferadar import summarize
from inferadar.summarize import (
    build_markdown,
    find_target_jsons,
    linkify_pr_refs,
    render_input,
    strip_mentions,
    summarize_artifact_file,
)


def _artifact() -> dict:
    return {
        "generated_at": "2026-06-08T09:28:52Z",
        "period_start": "2026-06-01",
        "period_end": "2026-06-08",
        "source_repo": "ROCm/AITER",
        "rule_version": 1,
        "summary": {
            "total_prs": 3,
            "total_commits": 10,
            "total_files": 3,
            "state_counts": {"merged": 2, "open_pr": 1},
            "label_counts": {
                "merged": 2,
                "open_pr": 1,
                "component:moe": 2,
                "type:perf": 1,
                "type:tests": 1,
                "model:deepseek": 2,
                "model:general": 1,
            },
            "primary_label_counts": {},
            "auxiliary_label_counts": {},
        },
        "prs": [
            {
                "number": 100,
                "title": "Big MoE perf win",
                "url": "https://github.com/ROCm/aiter/pull/100",
                "author": "alice",
                "state": "merged",
                "changed_files": [{"additions": 500, "deletions": 100}],
                "commit_shas": ["a", "b"],
                "labels": ["merged", "component:moe", "type:perf", "model:deepseek"],
            },
            {
                "number": 101,
                "title": "small test tweak",
                "url": "https://github.com/ROCm/aiter/pull/101",
                "author": "bob",
                "state": "merged",
                "changed_files": [{"additions": 3, "deletions": 1}],
                "commit_shas": ["c"],
                "labels": ["merged", "type:tests"],
            },
            {
                "number": 102,
                "title": "WIP feature",
                "url": "https://github.com/ROCm/aiter/pull/102",
                "author": "carol",
                "state": "open_pr",
                "changed_files": [{"additions": 20, "deletions": 0}],
                "commit_shas": ["d"],
                "labels": ["open_pr", "model:deepseek"],
            },
        ],
        "unclassified": [],
    }


def test_render_input_surfaces_signal() -> None:
    text = render_input(_artifact())
    assert "ROCm/AITER" in text
    assert "2026-06-01 to 2026-06-08" in text
    assert "2 merged, 1 newly opened" in text
    assert "model:deepseek: 2" in text
    assert "## Merged PRs (2" in text
    assert "## Newly opened PRs (1" in text
    # bigger churn sorts first, and state labels are dropped from per-PR labels
    assert text.index("#100") < text.index("#101")
    assert "size:600 (+500/-100)" in text
    assert "component:moe" in text


def test_strip_mentions_removes_pings_but_not_emails() -> None:
    assert strip_mentions("thanks @alice and @bob-1") == "thanks alice and bob-1"
    assert strip_mentions("email a@b.com stays") == "email a@b.com stays"
    assert strip_mentions("team @org/team") == "team org/team"


def test_linkify_only_known_pr_numbers() -> None:
    out = linkify_pr_refs("see #100 and #999", _artifact())
    assert "[#100](https://github.com/ROCm/aiter/pull/100)" in out
    assert "#999" in out
    assert "[#999]" not in out


def test_build_markdown_header_footer_and_sanitization() -> None:
    def fake_llm(system: str, user: str) -> str:
        assert "ROCm/AITER" in user
        return "## TL;DR\n- @alice landed a MoE perf win #100\n\n## Most important PRs\n- #100 big win"

    md = build_markdown(_artifact(), display_name="AITER", llm=fake_llm)
    assert md.startswith("# AITER: PR digest (2026-06-01 to 2026-06-08)")
    assert "2 merged, 1 newly opened" in md
    assert "@alice" not in md
    assert "alice landed" in md
    assert "[#100](https://github.com/ROCm/aiter/pull/100)" in md
    assert "deterministic source of truth" in md


def test_summarize_artifact_file_idempotent(tmp_path) -> None:
    window = tmp_path / "changelogs" / "2026-06-01_to_2026-06-08"
    window.mkdir(parents=True)
    json_path = window / "AITER.json"
    json_path.write_text(json.dumps(_artifact()), encoding="utf-8")
    md_path = window / "AITER.md"

    calls: list[int] = []

    def fake_llm(system: str, user: str) -> str:
        calls.append(1)
        return "## TL;DR\n- body #100"

    path, status = summarize_artifact_file(json_path, llm=fake_llm)
    assert status == "written"
    assert path == md_path and md_path.exists()
    assert len(calls) == 1

    # md newer than json -> skip
    os.utime(json_path, (1000, 1000))
    os.utime(md_path, (2000, 2000))
    _, status = summarize_artifact_file(json_path, llm=fake_llm)
    assert status == "skipped"
    assert len(calls) == 1

    # json newer than md -> regenerate
    os.utime(json_path, (3000, 3000))
    _, status = summarize_artifact_file(json_path, llm=fake_llm)
    assert status == "written"
    assert len(calls) == 2

    # force regardless of mtimes
    os.utime(json_path, (1000, 1000))
    os.utime(md_path, (9000, 9000))
    _, status = summarize_artifact_file(json_path, llm=fake_llm, force=True)
    assert status == "written"
    assert len(calls) == 3


def test_find_target_jsons_window_selection(tmp_path) -> None:
    root = tmp_path / "changelogs"
    for window in ["2026-06-01_to_2026-06-08", "2026-05-25_to_2026-06-01"]:
        window_dir = root / window
        window_dir.mkdir(parents=True)
        for repo in ["AITER", "vllm"]:
            (window_dir / f"{repo}.json").write_text("{}", encoding="utf-8")
    # noise that must be ignored
    (root / "notawindow").mkdir()
    (root / "legacy.json").write_text("{}", encoding="utf-8")

    assert len(find_target_jsons(root, window="all")) == 4

    latest = find_target_jsons(root, window="latest")
    assert len(latest) == 2
    assert all(p.parent.name == "2026-06-01_to_2026-06-08" for p in latest)

    only = find_target_jsons(root, window="latest", only="AITER")
    assert len(only) == 1 and only[0].stem == "AITER"

    specific = find_target_jsons(root, start="2026-05-25", end="2026-06-01")
    assert len(specific) == 2
    assert all(p.parent.name == "2026-05-25_to_2026-06-01" for p in specific)


def test_main_writes_markdown(monkeypatch, tmp_path) -> None:
    root = tmp_path / "changelogs"
    window_dir = root / "2026-06-01_to_2026-06-08"
    window_dir.mkdir(parents=True)
    (window_dir / "AITER.json").write_text(json.dumps(_artifact()), encoding="utf-8")

    monkeypatch.setattr(summarize, "call_llm", lambda s, u, **k: "## TL;DR\n- body #100")

    assert summarize.main(["--changelogs-dir", str(root)]) == 0
    md = (window_dir / "AITER.md").read_text(encoding="utf-8")
    assert md.startswith("# AITER: PR digest")
    assert "[#100](https://github.com/ROCm/aiter/pull/100)" in md


def test_call_llm_retries_on_empty_then_succeeds(monkeypatch) -> None:
    monkeypatch.setenv("INFERADAR_LLM_BASE_URL", "https://gw/v1")
    monkeypatch.setenv("INFERADAR_LLM_API_KEY", "k")
    monkeypatch.setenv("INFERADAR_LLM_MODEL", "m")
    monkeypatch.setenv("INFERADAR_LLM_MAX_TOKENS", "1000")
    monkeypatch.setenv("INFERADAR_LLM_MAX_TOKENS_CAP", "8000")
    monkeypatch.setenv("INFERADAR_LLM_EMPTY_RETRIES", "3")

    budgets: list[int] = []

    def fake_once(base_url, api_key, model, system, user, max_tokens, timeout):
        budgets.append(max_tokens)
        if max_tokens < 4000:
            raise summarize._EmptyContentError("empty")
        return "ok content"

    monkeypatch.setattr(summarize, "_chat_once", fake_once)
    out = summarize.call_llm("sys", "usr")
    assert out == "ok content"
    # escalates 1000 -> 2000 -> 4000 (doubling, capped at 8000)
    assert budgets == [1000, 2000, 4000]


def test_call_llm_gives_up_after_retries(monkeypatch) -> None:
    monkeypatch.setenv("INFERADAR_LLM_BASE_URL", "https://gw/v1")
    monkeypatch.setenv("INFERADAR_LLM_API_KEY", "k")
    monkeypatch.setenv("INFERADAR_LLM_MODEL", "m")
    monkeypatch.setenv("INFERADAR_LLM_MAX_TOKENS", "1000")
    monkeypatch.setenv("INFERADAR_LLM_MAX_TOKENS_CAP", "4000")
    monkeypatch.setenv("INFERADAR_LLM_EMPTY_RETRIES", "2")

    calls = {"n": 0}

    def always_empty(*a, **k):
        calls["n"] += 1
        raise summarize._EmptyContentError("empty")

    monkeypatch.setattr(summarize, "_chat_once", always_empty)
    with pytest.raises(RuntimeError, match="empty content after"):
        summarize.call_llm("sys", "usr")
    assert calls["n"] == 3  # initial + 2 retries


def _set_llm_env(monkeypatch, **overrides) -> None:
    monkeypatch.setenv("INFERADAR_LLM_BASE_URL", "https://gw/v1")
    monkeypatch.setenv("INFERADAR_LLM_API_KEY", "k")
    monkeypatch.setenv("INFERADAR_LLM_MODEL", "m")
    for key in ("INFERADAR_LLM_MAX_TOKENS", "INFERADAR_LLM_MAX_TOKENS_CAP", "INFERADAR_LLM_EMPTY_RETRIES"):
        monkeypatch.delenv(key, raising=False)
    for key, val in overrides.items():
        monkeypatch.setenv(key, val)


def test_call_llm_single_attempt_when_budget_at_cap(monkeypatch) -> None:
    _set_llm_env(monkeypatch, INFERADAR_LLM_MAX_TOKENS="8000", INFERADAR_LLM_MAX_TOKENS_CAP="4000",
                 INFERADAR_LLM_EMPTY_RETRIES="5")
    budgets: list[int] = []

    def fake_once(b, a, m, s, u, max_tokens, t):
        budgets.append(max_tokens)
        raise summarize._EmptyContentError("empty")

    monkeypatch.setattr(summarize, "_chat_once", fake_once)
    with pytest.raises(RuntimeError, match="after 1 attempt"):
        summarize.call_llm("sys", "usr")
    assert budgets == [4000]  # initial clamped to cap; no escalation past cap


def test_call_llm_zero_retries(monkeypatch) -> None:
    _set_llm_env(monkeypatch, INFERADAR_LLM_MAX_TOKENS="1000", INFERADAR_LLM_MAX_TOKENS_CAP="9000",
                 INFERADAR_LLM_EMPTY_RETRIES="0")
    calls = {"n": 0}

    def fake_once(*a, **k):
        calls["n"] += 1
        raise summarize._EmptyContentError("empty")

    monkeypatch.setattr(summarize, "_chat_once", fake_once)
    with pytest.raises(RuntimeError, match="after 1 attempt"):
        summarize.call_llm("sys", "usr")
    assert calls["n"] == 1


def test_call_llm_fast_fails_on_content_filter(monkeypatch) -> None:
    _set_llm_env(monkeypatch, INFERADAR_LLM_MAX_TOKENS="1000", INFERADAR_LLM_MAX_TOKENS_CAP="9000",
                 INFERADAR_LLM_EMPTY_RETRIES="5")
    calls = {"n": 0}

    def fake_once(*a, **k):
        calls["n"] += 1
        raise summarize._EmptyContentError("empty", finish_reason="content_filter")

    monkeypatch.setattr(summarize, "_chat_once", fake_once)
    with pytest.raises(RuntimeError, match="content_filter"):
        summarize.call_llm("sys", "usr")
    assert calls["n"] == 1  # non-budget reason: no escalation


def test_call_llm_invalid_env_int(monkeypatch) -> None:
    _set_llm_env(monkeypatch, INFERADAR_LLM_MAX_TOKENS_CAP="not-a-number")
    monkeypatch.setattr(summarize, "_chat_once", lambda *a, **k: "x")
    with pytest.raises(RuntimeError, match="must be an integer"):
        summarize.call_llm("sys", "usr")


def test_auth_headers_default_bearer(monkeypatch) -> None:
    monkeypatch.delenv("INFERADAR_LLM_AUTH_HEADER", raising=False)
    monkeypatch.delenv("INFERADAR_LLM_AUTH_PREFIX", raising=False)
    headers = summarize._auth_headers("KEY")
    assert headers["Authorization"] == "Bearer KEY"
    assert headers["Content-Type"] == "application/json"


def test_auth_headers_apim_subscription_key(monkeypatch) -> None:
    monkeypatch.setenv("INFERADAR_LLM_AUTH_HEADER", "Ocp-Apim-Subscription-Key")
    monkeypatch.setenv("INFERADAR_LLM_AUTH_PREFIX", "")
    headers = summarize._auth_headers("KEY")
    assert headers == {"Ocp-Apim-Subscription-Key": "KEY", "Content-Type": "application/json"}
    assert "Authorization" not in headers


def test_main_validates_and_handles_empty(tmp_path) -> None:
    root = tmp_path / "changelogs"
    (root / "2026-06-01_to_2026-06-08").mkdir(parents=True)
    # start without end is an argument error
    assert summarize.main(["--changelogs-dir", str(root), "--start", "2026-06-01"]) == 2
    # valid dir but no JSON files -> nothing to do, success
    empty = tmp_path / "empty"
    empty.mkdir()
    assert summarize.main(["--changelogs-dir", str(empty)]) == 0
