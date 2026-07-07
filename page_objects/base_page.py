import os

from playwright.sync_api import Page

from page_objects.components.header import Header
from page_objects.components.footer import Footer
from page_objects.components.menu import Menu

class BasePage:

  def __init__(self, page: Page):
    self.page: Page = page
    self.base_url: str = os.environ.get("PYTEST_BASE_URL", "https://www.saucedemo.com/")
    self.header: Header = Header(page)
    self.footer: Footer = Footer(page)
    self.menu: Menu = Menu(page)

  def navigate(self, path: str = "") -> None:
    url: str = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
    self.page.goto(url)
