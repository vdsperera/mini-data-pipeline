"""Example page object for https://the-internet.herokuapp.com/login (public practice site)."""
from selenium.webdriver.common.by import By

from .base_page import BasePage


class LoginPage(BasePage):
    URL = "https://the-internet.herokuapp.com/login"
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    SUBMIT = (By.CSS_SELECTOR, "button[type='submit']")
    FLASH = (By.ID, "flash")

    def login(self, user: str, password: str) -> str:
        self.open(self.URL)
        self.type(self.USERNAME, user)
        self.type(self.PASSWORD, password)
        self.click(self.SUBMIT)
        return self.text(self.FLASH)
