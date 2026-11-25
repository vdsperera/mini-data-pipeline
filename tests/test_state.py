from src.state import State


def test_state_persists_and_is_idempotent(tmp_path):
    path = tmp_path / "s.json"
    s = State(str(path))
    assert not s.is_done(1)
    s.mark_done(1)
    assert State(str(path)).is_done(1)  # survives reload


def test_failed_then_done_clears_failure(tmp_path):
    s = State(str(tmp_path / "s.json"))
    s.mark_failed(2, "boom")
    s.mark_done(2)
    assert "2" not in s.data["failed"]
