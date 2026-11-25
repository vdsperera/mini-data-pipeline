import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 10.0

def get_session(retries: int = 3, backoff: float = 0.5) -> requests.Session:
    session = requests.Session()
    strategy = Retry(
        total=retries,
        backoff_factor=backoff,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

def fetch_json(session: requests.Session, url: str, timeout: float = DEFAULT_TIMEOUT):
    logger.info("Requesting %s", url)
    resp = session.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.json()

class ApiClient:
    def __init__(self, base_url: str = "", token: str = "", timeout: float = DEFAULT_TIMEOUT):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = get_session()
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"

    def get_json(self, path_or_url: str) -> dict | list:
        url = path_or_url if path_or_url.startswith("http") else f"{self.base_url}/{path_or_url.lstrip('/')}"
        logger.info("Requesting %s", url)
        resp = self.session.request("GET", url, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def paginate(self, path: str, limit: int = 20, max_pages: int = 10):
        page = 1
        while page <= max_pages:
            items = self.get_json(f"{path}?_page={page}&_limit={limit}")
            if not items:
                break
            for item in items:
                yield item
            page += 1
