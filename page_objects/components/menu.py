from playwright.sync_api import Page

class Menu:

  def __init__(self, page: Page):
    self.page = page

  @property
  def logout_button(self):
    return self.page.get_by_role("link", name="Logout")
  
  @property
  def all_items_button(self):
    return self.page.get_by_role("link", name="All Items")
  
  @property
  def reset_app_state_button(self):
    return self.page.get_by_role("link", name="Reset App State")
  
  @property
  def about_button(self):
    return self.page.get_by_role("link", name="About")
  
  @property
  def close_menu_button(self):
    return self.page.get_by_role("button", name="Close Menu")