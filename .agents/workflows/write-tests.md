---
description: Write focused pytest tests with mocks (no live network)
---

# Write tests

1. Read the code and pick the logic worth testing (parsing, aggregation, retry decisions, state file, dedupe).
2. Write 3 to 6 pytest tests in `tests/`. Use `tmp_path`, `monkeypatch` or `unittest.mock`. No live network or real browser.
3. Cover: happy path, empty input, one bad record in the middle, a failure then success, and a re-run after partial failure.
4. Run `pytest -q` and show the output. Fix failing tests (or real bugs) before finishing.
