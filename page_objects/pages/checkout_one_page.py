from playwright.sync_api import Locator, Page

from page_objects.base_page import BasePage

class CheckoutOnePage(BasePage):
  def __init__(self, page: Page):
    super().__init__(page)
    self.page: Page = page
  
  def navigate(self) -> None:
    super().navigate("/checkout-step-one.html")

  @property
  def first_name_input(self) -> Locator:
    return self.page.get_by_placeholder("First Name")

  @property
  def last_name_input(self) -> Locator:
    return self.page.get_by_placeholder("Last Name")

  @property
  def postal_code_input(self) -> Locator:
    return self.page.get_by_placeholder("Zip/Postal Code")

  @property
  def continue_button(self) -> Locator:
    return self.page.get_by_role("button", name="Continue")

  @property
  def cancel_button(self) -> Locator:
    return self.page.get_by_role("button", name="Cancel")
  
  @property
  def error_message_container(self) -> Locator:
    return self.page.get_by_test_id("error")

  def perform_checkout(self, first_name: str, last_name: str, postal_code: str) -> None:
    self.first_name_input.fill(first_name)
    self.last_name_input.fill(last_name)
    self.postal_code_input.fill(postal_code)
    self.continue_button.click()

  def navigate_cancel(self) -> None:
    self.cancel_button.click()