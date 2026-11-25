import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import logging
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.http_client import get_session, fetch_json
from src.state import load_state, save_state

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

BASE_URL = "https://jsonplaceholder.typicode.com"
OUTPUT_DIR = Path("output")
CSV_FILE = OUTPUT_DIR / "summary.csv"
STATE_FILE = OUTPUT_DIR / "state.json"
FIELDNAMES = [
    "user id", "name", "email", "city",
    "number of posts", "number of completed todos", "completion rate"
]

def compute_metrics(posts: list, todos: list) -> tuple[int, int, float]:
    total_todos = len(todos)
    completed_todos = sum(1 for t in todos if t.get("completed"))
    rate = round(completed_todos / total_todos, 2) if total_todos > 0 else 0.0
    return len(posts), completed_todos, rate

def process_user(session, user: dict) -> dict:
    user_id = user["id"]
    posts = fetch_json(session, f"{BASE_URL}/posts?userId={user_id}")
    todos = fetch_json(session, f"{BASE_URL}/todos?userId={user_id}")
    n_posts, n_completed, rate = compute_metrics(posts, todos)
    return {
        "user id": user_id,
        "name": user.get("name", ""),
        "email": user.get("email", ""),
        "city": user.get("address", {}).get("city", ""),
        "number of posts": n_posts,
        "number of completed todos": n_completed,
        "completion rate": f"{rate:.2f}",
    }

def append_row(row: dict) -> None:
    write_header = not CSV_FILE.exists()
    with CSV_FILE.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if write_header:
            writer.writeheader()
        writer.writerow(row)

def parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch and aggregate JSONPlaceholder user data.")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of users to process.")
    parser.add_argument("--workers", type=int, default=5, help="Number of concurrent worker threads (default: 5).")
    return parser.parse_args(argv)

def run_pipeline(limit: int | None = None, max_workers: int = 5) -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    state = load_state(STATE_FILE)
    session = get_session()

    users = fetch_json(session, f"{BASE_URL}/users")
    if limit is not None and limit > 0:
        users = users[:limit]

    to_process = []
    skipped_count = 0
    for user in users:
        user_id = user["id"]
        if user_id in state["completed"]:
            skipped_count += 1
            logger.info("User %s already completed, skipping.", user_id)
        else:
            to_process.append(user)

    ok_count = 0
    failed_count = 0

    if to_process:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_user = {
                executor.submit(process_user, session, user): user
                for user in to_process
            }
            for future in as_completed(future_to_user):
                user = future_to_user[future]
                user_id = user["id"]
                try:
                    row = future.result()
                    append_row(row)
                    state["completed"].append(user_id)
                    if user_id in state["failed"]:
                        state["failed"].remove(user_id)
                    save_state(STATE_FILE, state)
                    ok_count += 1
                    logger.info("Successfully processed user %s (%s)", user_id, user.get("name"))
                except Exception as exc:
                    failed_count += 1
                    logger.error("Failed to process user %s: %s", user_id, exc)
                    if user_id not in state["failed"]:
                        state["failed"].append(user_id)
                    save_state(STATE_FILE, state)

    logger.info("Final summary: ok=%d, skipped=%d, failed=%d", ok_count, skipped_count, failed_count)
    return 1 if failed_count > 0 else 0

def main(argv=None) -> int:
    args = parse_args(argv)
    return run_pipeline(limit=args.limit, max_workers=args.workers)

if __name__ == "__main__":
    sys.exit(main())
