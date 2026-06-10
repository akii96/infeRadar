from __future__ import annotations

import json

import pytest

from inferadar import github_client as gc
from inferadar.github_client import GitHubClient, GitHubClientError


def test_search_merged_prs_follows_pagination() -> None:
    calls: list[str] = []

    def transport(url: str, headers: dict[str, str]) -> tuple[int, dict[str, str], bytes]:
        calls.append(url)
        if "page=2" in url:
            return 200, {}, json.dumps({"items": [{"number": 2, "title": "second"}]}).encode()
        return (
            200,
            {"Link": '<https://api.github.com/search/issues?page=2>; rel="next"'},
            json.dumps({"items": [{"number": 1, "title": "first"}]}).encode(),
        )

    client = GitHubClient(transport=transport)

    items = client.search_merged_prs("2026-05-08", "2026-05-15")

    assert [item["number"] for item in items] == [1, 2]
    assert len(calls) == 2


def test_search_open_prs_uses_created_window() -> None:
    seen_url = ""

    def transport(url: str, headers: dict[str, str]) -> tuple[int, dict[str, str], bytes]:
        nonlocal seen_url
        seen_url = url
        return 200, {}, json.dumps({"items": [{"number": 20, "title": "open"}]}).encode()

    client = GitHubClient(transport=transport)

    items = client.search_open_prs("2026-05-08", "2026-05-15")

    assert items[0]["number"] == 20
    assert "is%3Aopen" in seen_url
    assert "created%3A2026-05-08..2026-05-15" in seen_url


def test_fetch_weekly_records_includes_merged_and_open_prs() -> None:
    def transport(url: str, headers: dict[str, str]) -> tuple[int, dict[str, str], bytes]:
        if "/search/issues" in url and "is%3Amerged" in url:
            payload = {"items": [{"number": 10, "title": "Add Kimi GEMM"}]}
        elif "/search/issues" in url and "is%3Aopen" in url:
            payload = {"items": [{"number": 11, "title": "Add MiniMax cache"}]}
        elif url.endswith("/pulls/10"):
            payload = {
                "number": 10,
                "title": "Add Kimi GEMM",
                "html_url": "https://github.com/ROCm/aiter/pull/10",
                "user": {"login": "author"},
                "body": "new kernel",
                "created_at": "2026-05-13T00:00:00Z",
                "merged_at": "2026-05-14T00:00:00Z",
                "merge_commit_sha": "merge-sha",
            }
        elif url.endswith("/pulls/11"):
            payload = {
                "number": 11,
                "title": "Add MiniMax cache",
                "html_url": "https://github.com/ROCm/aiter/pull/11",
                "user": {"login": "author"},
                "body": "new kernel",
                "created_at": "2026-05-15T00:00:00Z",
                "merged_at": None,
                "merge_commit_sha": "github-test-merge-sha",
            }
        elif url.endswith("/pulls/10/files?per_page=100"):
            payload = [{"filename": "aiter/configs/model_configs/kimik2_bf16_tuned_gemm.csv"}]
        elif url.endswith("/pulls/10/commits?per_page=100"):
            payload = [{"sha": "commit-sha"}]
        elif url.endswith("/pulls/11/files?per_page=100"):
            payload = [{"filename": "csrc/kernels/cache_kernels.cu"}]
        elif url.endswith("/pulls/11/commits?per_page=100"):
            payload = [{"sha": "open-sha"}]
        else:
            raise AssertionError(f"unexpected URL {url}")
        return 200, {}, json.dumps(payload).encode()

    client = GitHubClient(transport=transport)

    records = client.fetch_weekly_records("2026-05-08", "2026-05-15")

    assert len(records) == 2
    assert records[0].number == 10
    assert records[0].state == "merged"
    assert records[0].files[0]["filename"].endswith("kimik2_bf16_tuned_gemm.csv")
    assert records[0].commits[0]["sha"] == "commit-sha"
    assert records[1].number == 11
    assert records[1].state == "open_pr"
    assert records[1].merged_at is None
    assert records[1].merge_commit_sha is None
    assert records[1].commits[0]["sha"] == "open-sha"


def test_retry_after_seconds_reads_headers() -> None:
    assert gc._retry_after_seconds({"Retry-After": "7"}) == 7.0
    assert gc._retry_after_seconds({}) is None
    assert gc._retry_after_seconds(None) is None


def test_is_secondary_rate_limit_detection() -> None:
    assert gc._is_secondary_rate_limit(403, {"Retry-After": "1"}, b"") is True
    assert gc._is_secondary_rate_limit(403, {"X-RateLimit-Remaining": "0"}, b"") is True
    assert gc._is_secondary_rate_limit(403, {}, b"You have exceeded a secondary rate limit") is True
    assert gc._is_secondary_rate_limit(403, {}, b"forbidden") is False
    assert gc._is_secondary_rate_limit(500, {}, b"") is False


def _http_error(code: int) -> gc.HTTPError:
    return gc.HTTPError("https://api.github.com/x", code, "err", {}, None)


def test_default_transport_retries_5xx_then_succeeds(monkeypatch) -> None:
    attempts = {"n": 0}

    class _Resp:
        status = 200
        headers: dict[str, str] = {}

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self):
            return b"{}"

    def fake_urlopen(request, timeout=30):
        attempts["n"] += 1
        if attempts["n"] < 3:
            raise _http_error(500)
        return _Resp()

    monkeypatch.setattr(gc, "urlopen", fake_urlopen)
    slept: list[float] = []
    status, _headers, body = gc._default_transport(
        "https://api.github.com/x", {}, max_retries=5, sleep=slept.append
    )
    assert status == 200 and body == b"{}"
    assert attempts["n"] == 3
    assert len(slept) == 2  # two backoff waits before success


def test_default_transport_no_retry_on_404(monkeypatch) -> None:
    attempts = {"n": 0}

    def fake_urlopen(request, timeout=30):
        attempts["n"] += 1
        raise _http_error(404)

    monkeypatch.setattr(gc, "urlopen", fake_urlopen)
    with pytest.raises(GitHubClientError):
        gc._default_transport("https://api.github.com/x", {}, max_retries=3, sleep=lambda s: None)
    assert attempts["n"] == 1
