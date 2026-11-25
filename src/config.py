import os

API_BASE_URL = os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")
API_TOKEN = os.getenv("API_TOKEN")  # optional
HEADLESS = os.getenv("HEADLESS", "1") == "1"
TIMEOUT = int(os.getenv("TIMEOUT", "10"))
STATE_FILE = os.getenv("STATE_FILE", "state.json")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")
