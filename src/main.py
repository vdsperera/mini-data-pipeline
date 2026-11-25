"""CLI entry point.  Usage:
    python -m src.main api      # API pipeline demo (resumable, retries, CSV output)
    python -m src.main web      # Selenium demo (login + screenshot on failure)
"""
import argparse
import csv
import os
import sys
from pathlib import Path

from . import config
from .http_client import ApiClient
from .logger import get_logger
from .state import State

log = get_logger("main")


def run_api() -> int:
    client = ApiClient(config.API_BASE_URL, config.API_TOKEN, config.TIMEOUT)
    state = State(config.STATE_FILE)
    Path(config.OUTPUT_DIR).mkdir(exist_ok=True)
    out = Path(config.OUTPUT_DIR) / "posts.csv"
    new_file = not out.exists()
    ok = failed = skipped = 0
    with open(out, "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["id", "userId", "title"])
        if new_file:
            writer.writeheader()
        for post in client.paginate("posts", limit=20, max_pages=3):
            pid = post.get("id")
            if pid is None:
                log.warning("Skipping malformed record: %r", post)
                failed += 1
                continue
            if state.is_done(pid):
                skipped += 1
                continue
            try:
                writer.writerow({k: post[k] for k in ("id", "userId", "title")})
                state.mark_done(pid)
                ok += 1
            except KeyError as exc:
                state.mark_failed(pid, f"missing field {exc}")
                failed += 1
    log.info("SUMMARY ok=%d skipped=%d failed=%d", ok, skipped, failed)
    return 1 if failed else 0


def run_web() -> int:
    from .pages.base_page import make_driver
    from .pages.login_page import LoginPage

    driver = make_driver(config.HEADLESS)
    page = LoginPage(driver, config.TIMEOUT)
    try:
        msg = page.login("tomsmith", "SuperSecretPassword!")
        assert "You logged into a secure area" in msg, f"Unexpected message: {msg!r}"
        log.info("Login OK")
        return 0
    except Exception:
        log.exception("Web flow failed")
        page.screenshot("login_failure")
        return 1
    finally:
        driver.quit()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("command", choices=["api", "web"])
    args = parser.parse_args(argv)
    return run_api() if args.command == "api" else run_web()


if __name__ == "__main__":
    sys.exit(main())
