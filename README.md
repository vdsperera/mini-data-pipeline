# JSONPlaceholder User & Tasks Data Pipeline

## What it does
A resilient, resumable API automation pipeline that fetches users, their posts, and their todos from JSONPlaceholder (`https://jsonplaceholder.typicode.com`), computes user-level task completion metrics, and produces an aggregated CSV report at `output/summary.csv`.

## Setup
```bash
python -m venv .venv
.venv\Scripts\activate   # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

## Run
```bash
# Run full pipeline with default settings (5 workers)
python src/pipeline.py

# Run with a limit on the number of users
python src/pipeline.py --limit 5

# Customize concurrency
python src/pipeline.py --limit 10 --workers 3
```

## Test
```bash
# Run all unit and integration tests
python -m pytest -v
```

## Design decisions
- **Resilient HTTP Client**: Configured with `requests.Session`, `urllib3.util.Retry` with exponential backoff on HTTP 429 and 5xx (500, 502, 503, 504), and an explicit 10-second timeout on every request.
- **Resumable & Idempotent**: Progress is tracked in `output/state.json`. Completed users are automatically skipped on subsequent runs. State files are written atomically via temporary files (`.tmp` renamed via `os.replace`) to prevent corrupted states on sudden crashes.
- **Error Isolation**: Individual user processing failures are caught, logged with details, recorded in `state.json` under `failed`, and do not terminate the entire pipeline run.
- **Exit Codes & Observability**: Logs structured progress with timestamps and prints a final summary (`ok=..., skipped=..., failed=...`). Exits with status code `1` if any user request failed, or `0` on complete success.
- **Thread-safe Concurrency**: Uses `ThreadPoolExecutor` (5 workers by default) for concurrent API fetching. Results are consumed through `as_completed` on the main thread where CSV rows and state updates are recorded sequentially, eliminating race conditions without complex locking.

## Assumptions
- **Completion Rate**: Calculated as `completed_todos / total_todos` rounded to 2 decimal places (e.g. `0.55`). If a user has `0` total todos, completion rate evaluates to `0.0` to safely prevent division by zero.
- **City Extraction**: Extracted from `user["address"]["city"]`.
- **CSV Headers**: Exact required format: `user id,name,email,city,number of posts,number of completed todos,completion rate`.

## Known limitations / what I would do next
- **Streaming & Pagination**: Currently fetches all users upfront; for large-scale datasets, user fetching should be paginated/streamed to keep memory bounded.
- **Adaptive Throttling**: Add dynamic token-bucket rate limiting if upstream APIs enforce strict request-per-second constraints.

