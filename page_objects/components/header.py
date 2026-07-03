from playwright.sync_api import Page

class Header:

  def __init__(self, page: Page):
    self.page = page

  @property
  def page_title(self):
    return self.page.locator(".title")
    
  @property
  def shopping_cart(self):
    return self.page.get_by_test_id("shopping-cart-link")
  
  @property
  def shopping_cart_badge(self):
    return self.page.get_by_test_id("shopping-cart-badge")
  
  @property
  def menu_button(self):
    return self.page.get_by_role("button", name="Open Menu")
  
  @property
  def sorting_dropdown(self):
    return self.page.get_by_test_id("product-sort-container")
  
  def open_shopping_cart(self):
    self.shopping_cart.click()

  def open_menu(self):
    self.menu_button.click()
  
  def get_page_title(self):
    return self.page_title

  

