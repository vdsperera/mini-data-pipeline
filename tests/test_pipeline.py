from pathlib import Path
from unittest.mock import MagicMock
import pytest
import requests

from src.pipeline import compute_metrics
from src.state import load_state, save_state
from src.http_client import fetch_json

@pytest.fixture
def isolated_env(tmp_path, monkeypatch):
    from src import pipeline
    out_dir = tmp_path / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_file = out_dir / "summary.csv"
    state_file = out_dir / "state.json"

    monkeypatch.setattr(pipeline, "OUTPUT_DIR", out_dir)
    monkeypatch.setattr(pipeline, "CSV_FILE", csv_file)
    monkeypatch.setattr(pipeline, "STATE_FILE", state_file)
    return {"dir": out_dir, "csv": csv_file, "state": state_file}

def test_compute_metrics_regular():
    posts = [{"id": 1}, {"id": 2}]
    todos = [{"completed": True}, {"completed": False}, {"completed": True}, {"completed": False}]
    n_posts, n_completed, rate = compute_metrics(posts, todos)
    assert n_posts == 2
    assert n_completed == 2
    assert rate == 0.5

def test_compute_metrics_zero_todos():
    posts = [{"id": 1}]
    todos = []
    n_posts, n_completed, rate = compute_metrics(posts, todos)
    assert n_posts == 1
    assert n_completed == 0
    assert rate == 0.0

def test_state_save_and_load(tmp_path: Path):
    state_file = tmp_path / "state.json"
    initial = load_state(state_file)
    assert initial == {"completed": [], "failed": []}

    save_state(state_file, {"completed": [1, 2], "failed": [3]})
    loaded = load_state(state_file)
    assert loaded["completed"] == [1, 2]
    assert loaded["failed"] == [3]

def test_fetch_json_http_error():
    mock_session = MagicMock()
    mock_resp = MagicMock()
    mock_resp.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error")
    mock_session.get.return_value = mock_resp

    with pytest.raises(requests.exceptions.HTTPError):
        fetch_json(mock_session, "https://example.com/api/test")

def test_csv_deduplication(isolated_env):
    from src import pipeline
    test_csv = isolated_env["csv"]

    existing_ids = set()
    row = {
        "user id": 1,
        "name": "Test User",
        "email": "test@example.com",
        "city": "Test City",
        "number of posts": 5,
        "number of completed todos": 3,
        "completion rate": "0.60"
    }

    pipeline.append_row(row, existing_ids)
    assert 1 in existing_ids

    # Append again with the same id
    pipeline.append_row(row, existing_ids)

    # File should have exactly 2 lines (1 header + 1 row)
    lines = test_csv.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 2

def test_run_pipeline_initial_fetch_failure(monkeypatch):
    from src import pipeline
    def mock_fetch_fail(*args, **kwargs):
        raise requests.exceptions.ConnectionError("Network down")

    monkeypatch.setattr(pipeline, "fetch_json", mock_fetch_fail)
    exit_code = pipeline.run_pipeline()
    assert exit_code == 1

def test_pipeline_happy_path(isolated_env, monkeypatch):
    from src import pipeline

    def mock_fetch(session, url, timeout=10):
        if url.endswith("/users"):
            return [
                {"id": 1, "name": "User 1", "email": "u1@test.com", "address": {"city": "City 1"}},
                {"id": 2, "name": "User 2", "email": "u2@test.com", "address": {"city": "City 2"}},
            ]
        if "posts?userId=" in url:
            return [{"id": 101}]
        if "todos?userId=" in url:
            return [{"completed": True}]
        raise ValueError(f"Unexpected url: {url}")

    monkeypatch.setattr(pipeline, "fetch_json", mock_fetch)
    exit_code = pipeline.run_pipeline(max_workers=1)
    assert exit_code == 0

    state = load_state(isolated_env["state"])
    assert set(state["completed"]) == {1, 2}
    assert state["failed"] == []

    lines = isolated_env["csv"].read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 3

def test_pipeline_empty_users(isolated_env, monkeypatch):
    from src import pipeline
    monkeypatch.setattr(pipeline, "fetch_json", lambda session, url, timeout=10: [])
    exit_code = pipeline.run_pipeline(max_workers=1)
    assert exit_code == 0
    state = load_state(isolated_env["state"])
    assert state["completed"] == []
    assert state["failed"] == []

def test_pipeline_one_bad_record_in_middle(isolated_env, monkeypatch):
    from src import pipeline

    def mock_fetch(session, url, timeout=10):
        if url.endswith("/users"):
            return [
                {"id": 1, "name": "User 1", "email": "u1@test.com", "address": {"city": "City 1"}},
                {"id": 2, "name": "User 2", "email": "u2@test.com", "address": {"city": "City 2"}},
                {"id": 3, "name": "User 3", "email": "u3@test.com", "address": {"city": "City 3"}},
            ]
        if "userId=2" in url:
            resp = MagicMock()
            resp.status_code = 500
            raise requests.HTTPError("500 Server Error", response=resp)
        if "posts" in url:
            return [{"id": 10}]
        if "todos" in url:
            return [{"completed": True}]
        raise ValueError(f"Unexpected url: {url}")

    monkeypatch.setattr(pipeline, "fetch_json", mock_fetch)
    exit_code = pipeline.run_pipeline(max_workers=1)
    assert exit_code == 1

    state = load_state(isolated_env["state"])
    assert set(state["completed"]) == {1, 3}
    assert state["failed"] == [2]

    lines = isolated_env["csv"].read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 3

def test_pipeline_rerun_after_partial_failure(isolated_env, monkeypatch):
    from src import pipeline

    fail_user_2 = True
    fetch_counts = {1: 0, 2: 0}

    def mock_fetch(session, url, timeout=10):
        nonlocal fail_user_2
        if url.endswith("/users"):
            return [
                {"id": 1, "name": "User 1", "email": "u1@test.com", "address": {"city": "City 1"}},
                {"id": 2, "name": "User 2", "email": "u2@test.com", "address": {"city": "City 2"}},
            ]
        if "userId=1" in url:
            fetch_counts[1] += 1
            return []
        if "userId=2" in url:
            fetch_counts[2] += 1
            if fail_user_2:
                resp = MagicMock()
                resp.status_code = 503
                raise requests.HTTPError("503 Service Unavailable", response=resp)
            return []
        raise ValueError(f"Unexpected url: {url}")

    monkeypatch.setattr(pipeline, "fetch_json", mock_fetch)

    # Run 1: User 1 passes, User 2 fails
    exit_code_1 = pipeline.run_pipeline(max_workers=1)
    assert exit_code_1 == 1
    state_1 = load_state(isolated_env["state"])
    assert state_1["completed"] == [1]
    assert state_1["failed"] == [2]

    # Run 2: User 2 is now healthy
    fail_user_2 = False
    initial_fetch_1 = fetch_counts[1]
    exit_code_2 = pipeline.run_pipeline(max_workers=1)
    assert exit_code_2 == 0

    # User 1 should have been skipped (no new fetches!)
    assert fetch_counts[1] == initial_fetch_1

    state_2 = load_state(isolated_env["state"])
    assert set(state_2["completed"]) == {1, 2}
    assert state_2["failed"] == []

    lines = isolated_env["csv"].read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 3
