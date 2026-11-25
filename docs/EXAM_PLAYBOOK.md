# Exam playbook (2-hour automation project)

## Your edge
Graders see many people who can make a script work once. You win by making it **reliable**: timeouts, retries, resumable state, per-item error handling, clear logs, a short honest README. That is also your real experience (semi-attended to unattended bots). Say that in your README and when you present.

## Before you start: ask / check (1 minute)
1. Is AI allowed, and which tools (Cursor, Copilot, ChatGPT)? Is internet allowed (docs, pip)?
2. Which language/libraries are required or forbidden?
3. What is graded: working output, code quality, tests, README, time?
4. Do I need to present or explain afterwards?
If you can't ask, assume: AI allowed, requirements listed in the task are all that matter.

## Timeline (120 min)
| Min | Phase | Output |
|---|---|---|
| 0-10 | Read task twice. Write `REQUIREMENTS.md` (numbered checklist + assumptions). Open the site/API in a browser or curl to see real data. | Checklist |
| 10-20 | Scaffold: venv, install, folder layout, logger, config. Paste starter files if allowed. | Runs "hello" |
| 20-60 | **Vertical slice**: smallest flow that does input -> work -> output for ONE item. Run it. | One item works end to end |
| 60-85 | Widen: all items, pagination/multiple pages, output file, all requirements. | All requirements ticked |
| 85-105 | Reliability: retries, timeouts, per-item try/except, state file, logging, screenshot on failure. | Survives bad data |
| 105-115 | Tests (3-6 focused ones) + README. | `pytest` green |
| 115-120 | Clean-state full run. Fix only typos. Submit. | Done |

Rule: if a requirement is stuck for more than 10 minutes, simplify it, note it under limitations, move on.

## First 10 minutes: prompt to paste into Cursor
```
Read the task below. Do NOT write code yet.
1) Rewrite it as a numbered requirements checklist in REQUIREMENTS.md.
2) List ambiguities and the assumption you propose for each.
3) Propose a plan of max 8 steps, starting with the smallest end-to-end slice.
4) List the libraries you will use (only requests, selenium, pytest, stdlib unless told).
TASK:
<paste task>
```

## Prompts to paste during the build
- Slice: `Implement ONLY step 1 of the plan. Max 60 lines. Tell me the exact command to run it.`
- Explore a site: `Here is the HTML of the page: <paste>. Suggest stable locators (id/data-attr/CSS) for X, Y, Z and explain why each is stable.`
- Debug: `Here is the full traceback and the code: <paste>. Explain the root cause in 2 sentences, then give the minimal fix.`
- Reliability pass: `Review the code for: missing timeouts, missing retries, bare excepts, silent failures, time.sleep, duplicate work on re-run. List issues first, then fix them one at a time.`
- Tests: `Write pytest tests with mocks for: success, empty input, one bad record, 500 then success, re-run after partial failure. No live network.`
- README: `Update README from the real code: install, run, test, design decisions, assumptions, limitations. Be honest, short.`
- Last check: `Run the self-review checklist from the rules file against the repo and report any unchecked item.`

## If AI is restricted or weaker than expected
Use `CHEATSHEET.md`. The skeleton you need is always: `requests.Session` + timeout + `raise_for_status`, or `webdriver.Chrome` + `WebDriverWait`. Write the slice by hand, ugly but working, then improve.

## Selenium quick triage (most common failures)
| Symptom | Fix |
|---|---|
| NoSuchElementException | Wrong locator or not loaded yet: wait for it; check iframe. |
| ElementClickIntercepted | Overlay/cookie banner: wait for it to go, or scroll into view, or JS click as last resort. |
| StaleElementReference | Page re-rendered: re-find the element right before use. |
| Works headed, fails headless | Set window size, wait for visibility, avoid hover-only flows. |
| Timeout | Print `driver.current_url` and take a screenshot, check what is on the page. |

## API quick triage
| Symptom | Fix |
|---|---|
| 401/403 | Token missing/expired, wrong header name. |
| 404 | Path or id wrong; log the full URL. |
| 429 | Back off, respect `Retry-After`. |
| JSONDecodeError | Response isn't JSON (HTML error page?). Log `resp.text[:200]`. |
| Hangs | No timeout set. Always set one. |

## Defending your work (if there is a walkthrough or follow-up)
You used AI, so prove you own the design. Be ready to answer, in plain English:
1. "Walk me through the flow." (input -> fetch -> process -> save -> report)
2. "What happens if the API/page fails halfway?" (retry, per-item catch, state file, resume)
3. "Why this locator / this retry policy / this data structure?"
4. "What would you do with another day?" (async/concurrency, config file, CI, better tests, metrics)
5. "Where did AI help and what did you change?" Honest answer: AI for syntax and boilerplate; you did the decomposition, edge cases and review.
Keep sentences short. Slow down. It is fine to say "I'd check the docs for the exact parameter, but the approach is..."

## Last 15 minutes checklist
- [ ] Fresh venv + `pip install -r requirements.txt` works
- [ ] Full run from clean state (delete state/output) works
- [ ] Re-run does not duplicate
- [ ] `pytest -q` green
- [ ] README: setup, run, test, assumptions, limitations
- [ ] No secrets, no absolute paths, no leftover debug prints
- [ ] `requirements.txt` complete
