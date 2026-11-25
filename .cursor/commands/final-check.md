# Final check (no new features)

1. Delete `state.json`, `output/`, `artifacts/`, `run.log`. Run the full flow from clean and show the result.
2. Run it a second time and confirm it does not duplicate work.
3. Run `pytest -q`.
4. Confirm `requirements.txt` is complete and README has: install, run, test, design decisions, assumptions, limitations.
5. Check for hard-coded secrets, absolute paths, leftover prints.
6. Go through every item in `REQUIREMENTS.md` and report which are done and which are limitations.
7. Report anything unchecked. Do not add features.
