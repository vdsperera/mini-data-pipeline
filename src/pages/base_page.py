"""Base page object: explicit waits and failure artifacts."""
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..logger import get_logger

log = get_logger(__name__)


def make_driver(headless: bool = True) -> webdriver.Chrome:
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1400,900")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=opts)  # Selenium Manager finds the driver


class BasePage:
    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url: str):
        self.driver.get(url)
        return self

    def visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator):
        self.clickable(locator).click()

    def type(self, locator, text: str):
        el = self.visible(locator)
        el.clear()
        el.send_keys(text)

    def text(self, locator) -> str:
        return self.visible(locator).text

    def screenshot(self, name: str = "failure") -> str:
        Path("artifacts").mkdir(exist_ok=True)
        path = f"artifacts/{name}_{datetime.now():%Y%m%d_%H%M%S}.png"
        self.driver.save_screenshot(path)
        log.error("Screenshot saved: %s (url=%s)", path, self.driver.current_url)
        return path
