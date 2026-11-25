# Project instructions (any AI coding tool)

This is a timed automation project (about 2 hours, AI allowed). Optimise for: working first, then reliable, then clean. The developer must be able to explain every line afterwards, so keep code simple.

## Workflow
1. Write `REQUIREMENTS.md` first (numbered checklist from the exact task wording + assumptions + plan of max 8 steps). No code before the plan is approved.
2. Build the smallest end-to-end slice first. Run after every step (never more than about 60 lines unrun).
3. Use only requests, selenium, pytest and the standard library unless told otherwise.
4. Keep README.md current: install, run, test, design decisions, assumptions, limitations.

## Reliability defaults
- Network calls: timeout, retry with backoff on 429/5xx, raise_for_status. Do not blindly retry POST.
- Browser: explicit waits only, no time.sleep. Screenshot on failure. Always quit the driver in finally.
- Resumable and idempotent: state file, no duplicate work on re-run.
- One failing item must not stop the run: catch per item, log, record, continue, summarise at the end.
- logging not print. No secrets in code. Non-zero exit code if anything failed.

## Code style
Python 3.10+, type hints, small functions, pathlib, no bare except, no mutable default arguments, argparse CLI.
