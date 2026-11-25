# REQUIREMENTS: Drill 1 - API Pipeline (JSONPlaceholder)

## 1. Numbered Checklist
- [ ] **REQ-1**: Use https://jsonplaceholder.typicode.com.
- [x] **REQ-2**: Fetch all users and their posts and todos.
- [x] **REQ-3**: Produce `output/summary.csv` with columns: `user id`, `name`, `email`, `city`, `number of posts`, `number of completed todos`, `completion rate`.
- [x] **REQ-4**: Timeouts and retries on all calls.
- [x] **REQ-5**: Resumable: re-running does not refetch users already done (state file).
- [x] **REQ-6**: A user whose request fails is logged, recorded in the state as failed, and the run continues.
- [x] **REQ-7**: Final log summary: ok / skipped / failed. Exit code 1 if any failed.
- [x] **REQ-8**: Tests: aggregation logic (completion rate with 0 todos!), state, one HTTP error case.
- [x] **REQ-9 (Stretch)**: Add `--limit N`.
- [x] **REQ-10 (Stretch)**: Use `ThreadPoolExecutor` with 5 workers.

## 2. Assumptions
1. **Completion Rate Calculation**: `completed_todos / total_todos`. If a user has `0` total todos, completion rate is `0.0` (float rounded to 2 decimal places, e.g. `0.75` or `0.00`).
2. **City Extraction**: Extracted from `user["address"]["city"]`.
3. **State File Location & Format**: `output/state.json` storing `{"completed": [user_id, ...], "failed": [user_id, ...]}`.
4. **CSV Header Exact Naming**: `user id,name,email,city,number of posts,number of completed todos,completion rate`.
5. **Retry Policy**: Exponential backoff on status codes 429 and 5xx (500, 502, 503, 504) with an explicit 10s timeout on all requests. Do not retry on 4xx client errors.
6. **Libraries**: `requests`, `pytest`, standard library (`csv`, `json`, `logging`, `pathlib`, `argparse`, `concurrent.futures`, `time`). No external libraries.

## 3. Minimal Execution Plan (Max 8 Steps)
1. [x] **Step 1 (Vertical Slice)**: Create directory structure (`output/`, `src/`). Implement minimal sequential script fetching 1 user, their posts and todos, calculating metrics, and writing 1 row to `output/summary.csv`. Run it and verify.
2. [x] **Step 2 (Resilient HTTP Client)**: Wrap API calls with explicit timeout (10s), retry strategy on 429/5xx with backoff, and logging.
3. [x] **Step 3 (State File & Resumability)**: Implement `output/state.json` management to record completed/failed users and skip completed users on re-runs.
4. [x] **Step 4 (Full Loop & Error Isolation)**: Implement iteration over all users with per-item `try/except`, recording failures in state, logging final summary (`ok/skipped/failed`), and returning exit code 1 if any failed.
5. [x] **Step 5 (Unit & Integration Tests)**: Add `tests/test_pipeline.py` testing aggregation logic (0 todos boundary), state file save/resume, and HTTP error/retry handling with mocks. Run `pytest`.
6. [x] **Step 6 (CLI & Stretch Goals)**: Add `argparse` for `--limit N` and add `ThreadPoolExecutor(max_workers=5)` with thread-safe recording.
7. [x] **Step 7 (Documentation)**: Create/update `README.md` with install, run, test instructions, design decisions, and limitations.
8. [x] **Step 8 (Final Clean Verification)**: Wipe `output/`, execute a full clean run, verify `output/summary.csv` and `output/state.json`, and run `pytest`.

