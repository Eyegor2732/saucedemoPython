from page_objects.base_page import BasePage

class CheckoutOnePage(BasePage):
  def __init__(self, page):
    super().__init__(page)

  @property
  def first_name_input(self):
    return self.page.get_by_placeholder("First Name")

  @property
  def last_name_input(self):
    return self.page.get_by_placeholder("Last Name")

  @property
  def postal_code_input(self):
    return self.page.get_by_placeholder("Zip/Postal Code")

  @property
  def continue_button(self):
    return self.page.get_by_role("button", name="Continue")

  @property
  def cancel_button(self):
    return self.page.get_by_role("button", name="Cancel")
  
  @property
  def error_message_container(self):
    return self.page.get_by_test_id("error")

  def navigate(self):
    super().navigate("/checkout-step-one.html")

  def perform_checkout(self, first_name, last_name, postal_code):
    self.first_name_input.fill(first_name)
    self.last_name_input.fill(last_name)
    self.postal_code_input.fill(postal_code)
    self.continue_button.click()

  def navigate_cancel(self):
    self.cancel_button.click()