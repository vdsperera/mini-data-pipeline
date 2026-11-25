---
name: automation-exam
description: Use when building a timed automation project (API automation with requests, Selenium browser automation, scraping, data pipelines) and the user needs a fast, reliable, explainable result.
---

# Automation exam skill

## When to use
- The user is given a timed project involving APIs, Selenium, scraping, CSV/JSON/SQLite output.
- The user says "exam", "timed", "2 hours", "automation task".

## Approach
1. Requirements checklist first (`REQUIREMENTS.md`), with assumptions.
2. One-item vertical slice, run it, then widen to all items.
3. Add reliability: timeouts, retries with backoff, explicit waits, per-item try/except, state file for resume, logging, failure screenshots.
4. Tests with mocks, README, clean-state run.

## Reuse
If `src/http_client.py`, `src/state.py`, `src/pages/base_page.py` exist, reuse them instead of rewriting.

## Keep it explainable
Prefer simple functions over clever abstractions. The user must be able to explain every line out loud.
