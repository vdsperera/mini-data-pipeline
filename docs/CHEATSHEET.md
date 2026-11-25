# Cheat sheet (syntax you don't need to remember)

## requests
```python
import requests
s = requests.Session()
s.headers.update({"Authorization": f"Bearer {token}"})
r = s.get(url, params={"page": 1}, timeout=10)
r.raise_for_status()
data = r.json()
r = s.post(url, json={"a": 1}, timeout=10)        # JSON body
r = s.post(url, data={"a": 1}, timeout=10)        # form body
r = s.post(url, files={"file": open("a.csv", "rb")}, timeout=30)
r.status_code, r.headers["Content-Type"], r.text[:200]
# errors: requests.exceptions.Timeout, ConnectionError, HTTPError, JSONDecodeError
```
Manual retry:
```python
import time
for attempt in range(1, 4):
    try:
        r = s.get(url, timeout=10); r.raise_for_status(); break
    except (requests.Timeout, requests.ConnectionError, requests.HTTPError) as e:
        if attempt == 3: raise
        time.sleep(2 ** attempt)
```

## Selenium 4
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

opts = Options(); opts.add_argument("--headless=new"); opts.add_argument("--window-size=1400,900")
driver = webdriver.Chrome(options=opts)
wait = WebDriverWait(driver, 10)
driver.get(url)
el = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.submit")))
el.click()
inp = wait.until(EC.visibility_of_element_located((By.ID, "q"))); inp.clear(); inp.send_keys("text", Keys.ENTER)
els = driver.find_elements(By.CSS_SELECTOR, ".item")        # list, never raises
el.get_attribute("href"); el.text
Select(driver.find_element(By.ID, "dd")).select_by_visible_text("Option")
driver.execute_script("arguments[0].scrollIntoView(true);", el)
wait.until(EC.staleness_of(old_el))                         # wait for page change
wait.until(EC.url_contains("/dashboard"))
wait.until(EC.text_to_be_present_in_element((By.ID, "flash"), "success"))
driver.switch_to.frame("name_or_element"); driver.switch_to.default_content()
driver.switch_to.window(driver.window_handles[-1])          # new tab
driver.switch_to.alert.accept()
driver.save_screenshot("x.png"); driver.page_source; driver.current_url
driver.quit()
```
CSS: `#id`, `.class`, `tag[attr='v']`, `a[href*='next']`, `ul > li:nth-child(2)`, `[data-test='login']`
XPath: `//button[normalize-space()='Next']`, `//tr[td[text()='ID5']]/td[3]`, `//*[@id='x']//a`

## Scraping with BeautifulSoup (if allowed; pip install beautifulsoup4)
```python
from bs4 import BeautifulSoup
soup = BeautifulSoup(r.text, "html.parser")
for q in soup.select("div.quote"):
    text = q.select_one("span.text").get_text(strip=True)
    nxt = soup.select_one("li.next a")      # None on last page
```

## pytest
```python
def test_x(tmp_path, monkeypatch): ...
@pytest.mark.parametrize("a,b", [(1, 2), (3, 4)])
with pytest.raises(ValueError): ...
from unittest.mock import MagicMock, patch
with patch("src.http_client.requests.Session.request", return_value=fake): ...
```
Run: `pytest -q`, `pytest -k name -x -s`

## Files and data
```python
import csv, json, os, sqlite3
from pathlib import Path
Path("out").mkdir(exist_ok=True)
with open("a.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["id", "name"]); w.writeheader(); w.writerow({...})
rows = list(csv.DictReader(open("a.csv", encoding="utf-8")))
json.dump(data, open("a.json", "w", encoding="utf-8"), indent=2)
tmp.write_text(...); os.replace(tmp, final)                 # atomic write

con = sqlite3.connect("app.db"); cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS t(id INTEGER PRIMARY KEY, name TEXT UNIQUE)")
cur.execute("INSERT OR IGNORE INTO t(id, name) VALUES (?, ?)", (1, "a"))   # dedupe
con.commit(); cur.execute("SELECT * FROM t WHERE id=?", (1,)).fetchall()
```

## CLI, env, logging, time
```python
import argparse, os, logging, sys, time
p = argparse.ArgumentParser(); p.add_argument("--input", required=True); p.add_argument("--limit", type=int, default=10)
args = p.parse_args()
os.getenv("TOKEN", "default")
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
sys.exit(1)     # non-zero on failure
```

## Concurrency (only if asked or clearly needed)
```python
from concurrent.futures import ThreadPoolExecutor, as_completed
with ThreadPoolExecutor(max_workers=5) as ex:
    futures = {ex.submit(fetch, i): i for i in ids}
    for f in as_completed(futures):
        try: f.result()
        except Exception: log.exception("item %s failed", futures[f])
```
Selenium is not thread-safe: one driver per thread.

## Playwright alternative (if Selenium is not mandatory)
```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(headless=True); page = b.new_page()
    page.goto(url); page.fill("#user", "x"); page.click("text=Login")
    page.wait_for_selector(".done"); b.close()
```

## Practice sites
- API: jsonplaceholder.typicode.com, httpbin.org, reqres.in
- Selenium: the-internet.herokuapp.com, saucedemo.com (standard_user / secret_sauce), quotes.toscrape.com, books.toscrape.com
