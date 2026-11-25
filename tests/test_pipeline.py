from pathlib import Path
from unittest.mock import MagicMock
import pytest
import requests

from src.pipeline import compute_metrics
from src.state import load_state, save_state
from src.http_client import fetch_json

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

