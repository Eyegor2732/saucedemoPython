from page_objects.components.header import Header
from page_objects.components.footer import Footer
from page_objects.components.menu import Menu

class BasePage:

  def __init__(self, page):
    self.page = page

    self.header = Header(page)
    self.footer = Footer(page)
    self.menu = Menu(page)

  def navigate(self, url):
    self.page.goto(url)
