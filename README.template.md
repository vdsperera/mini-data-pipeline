# <Project name>

## What it does
One or two sentences.

## Setup
```
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run
```
python -m src.main api
python -m src.main web
```
Config via environment variables: `API_BASE_URL`, `API_TOKEN`, `HEADLESS`, `TIMEOUT`.

## Test
```
pytest -q
```

## Design decisions
- Retries with backoff on 429/5xx; POST not retried (not idempotent).
- State file makes runs resumable and prevents duplicates.
- One failing item does not stop the run; failures are summarised and exit code is non-zero.
- Explicit waits only in Selenium; screenshot saved on failure.

## Assumptions
-

## Known limitations / what I would do next
-
