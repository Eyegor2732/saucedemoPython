import os

from page_objects.components.header import Header
from page_objects.components.footer import Footer
from page_objects.components.menu import Menu

class BasePage:

  def __init__(self, page):
    self.page = page
    self.base_url = os.environ.get("PYTEST_BASE_URL", "https://www.saucedemo.com/")
    self.header = Header(page)
    self.footer = Footer(page)
    self.menu = Menu(page)

  def navigate(self, path = ""):
    url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
    self.page.goto(url)
