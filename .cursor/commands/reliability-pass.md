# Reliability pass

1. Scan the code and LIST issues first (do not fix yet), grouped as:
   - network calls without timeout or retry
   - browser actions without explicit waits, any time.sleep
   - bare except, swallowed errors, silent failures
   - one bad item stopping the whole run
   - re-running duplicates work or output
   - secrets or URLs hard-coded
   - logs that would not explain a failure
2. Ask the user which to fix, or fix them in the order above, one at a time.
3. After each fix, run the code and show the result.
4. Make sure the run ends with a summary (ok / skipped / failed) and a non-zero exit code on failure.
