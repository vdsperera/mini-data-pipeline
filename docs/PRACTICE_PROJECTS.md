# Practice drills (timed, use Cursor with the rules)

Rules for every drill: start by writing REQUIREMENTS.md, build a vertical slice first, run constantly, finish with README + tests. Stop at the time limit even if unfinished and note limitations.

## Drill 1: API pipeline (45 min)
Use `https://jsonplaceholder.typicode.com`.
Task: fetch all users and their posts and todos. Produce `output/summary.csv` with columns: user id, name, email, city, number of posts, number of completed todos, completion rate.
Requirements:
1. Timeouts and retries on all calls
2. Resumable: re-running does not refetch users already done (state file)
3. A user whose request fails is logged, recorded in the state as failed, and the run continues
4. Final log summary: ok / skipped / failed. Exit code 1 if any failed
5. Tests: aggregation logic (completion rate with 0 todos!), state, one HTTP error case
Stretch: use `ThreadPoolExecutor` with 5 workers; add `--limit N`.

## Drill 2: Selenium flow (30-40 min)
Use `https://www.saucedemo.com` (standard_user / secret_sauce).
Task: log in, add the 3 cheapest items to the cart, verify the cart count and total, checkout with fake details, assert the confirmation message.
Requirements:
1. Page objects: LoginPage, InventoryPage, CartPage, CheckoutPage
2. Explicit waits only
3. Screenshot + page source saved on any failure
4. Parse prices from text to float and sort them in code
5. Run headless via env var
Stretch: repeat for `locked_out_user` and assert the error message; parametrise users with pytest.

## Drill 3: Scrape + store + post (40 min)
Use `https://quotes.toscrape.com` (or books.toscrape.com).
Task: scrape every page of quotes (text, author, tags) into SQLite with a UNIQUE constraint so reruns do not duplicate, then send a JSON summary (count per author) to `https://httpbin.org/post` and verify the echo.
Requirements: pagination until no "next"; retries on the POST decision explained in README; unit-test the parser with a saved HTML snippet; log counts inserted vs ignored.
Stretch: do it with requests+BeautifulSoup AND Selenium and say when you'd choose each.

## Drill 4: RCM-flavoured claim status checker (45 min, strongest story for your interview)
Mock data: create `claims.csv` with 50 rows (claim_id, patient_ref, payer, amount). Mock API: `https://httpbin.org/status/200,500,404` style endpoint or a tiny local Flask/`http.server` that randomly returns "paid / denied / pending" or a 500.
Task: for each claim, query the status, write `results.csv`, and produce `denied_report.csv`.
Requirements:
1. Semi-attended to unattended thinking: no human watching. Retries, backoff, and a retry-failed-only command (`--retry-failed`)
2. Idempotent: a claim already resolved is never re-queried
3. Status tracking per claim: pending / done / failed with the last error and attempt count
4. End-of-run report: counts per status, list of failures, run duration
5. No PHI in logs (log claim_id only, never patient data). Say why in README
Afterwards, explain it as the story: "what made bots fragile, what I changed, how I measured reliability" (attempt counts, failure rate before/after, runs needing manual intervention).

## After each drill (5 min)
Answer out loud: what was slowest, what did Cursor get wrong, which syntax did I not know? Add it to your own notes.
