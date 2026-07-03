from playwright.sync_api import Page

class Footer:

  def __init__(self, page: Page):
      self.page = page

  @property
  def twitter(self):
    return self.page.get_by_role("link", name="Twitter")
    
  @property
  def linkedin(self):
    return self.page.get_by_role("link", name="LinkedIn")
    
  @property
  def facebook(self):
    return self.page.get_by_role("link", name="Facebook")
    
  @property
  def copyright(self):
    return self.page.locator(".footer_copy")

  def open_twitter(self):
    self.twitter.click()

  def open_linkedin(self):
    self.linkedin.click()

  def open_facebook(self):
    self.facebook.click()
    