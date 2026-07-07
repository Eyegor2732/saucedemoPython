from playwright.sync_api import Locator, Page

from page_objects.base_page import BasePage

class CheckoutTwoPage(BasePage):
  def __init__(self, page: Page):
    super().__init__(page)
    self.page: Page = page
  
  def navigate(self) -> None:
    super().navigate("/checkout-step-two.html")

  @property
  def finish_button(self) -> Locator:
    return self.page.get_by_role("button", name="Finish")

  @property
  def cancel_button(self) -> Locator:
    return self.page.get_by_role("button", name="Cancel")
  
  @property
  def get_inventory_items(self) -> Locator:
    return self.page.get_by_test_id("inventory-item")
  
  @property
  def get_inventory_item_name(self) -> Locator:
    return self.page.get_by_test_id("inventory-item-name")
  
  @property
  def get_inventory_item_price(self) -> Locator:
    return self.page.get_by_test_id("inventory-item-price")
  
  @property
  def get_inventory_item_description(self) -> Locator:
    return self.page.get_by_test_id("inventory-item-desc")
  
  def get_tax_amount(self) -> str:
    _, _, after = self.page.get_by_test_id("tax-label").inner_text().partition("$")
    return after if after != "" else "0.00"
  
  def get_subtotal_amount(self) -> str:
    return self.page.get_by_test_id("subtotal-label").inner_text().split("$")[1]
  
  def get_total_amount(self) -> str:
    return self.page.get_by_test_id("total-label").inner_text().split("$")[1]

  def perform_finish(self) -> None:
    self.finish_button.click()

  def navigate_cancel(self) -> None:
    self.cancel_button.click()

  def get_inventory_item_name_by_index(self, index: int) -> str:
    return self.get_inventory_items.nth(index).get_by_test_id("inventory-item-name").inner_text()
  
  def get_inventory_item_price_by_index(self, index: int) -> str:
    return self.get_inventory_items.nth(index).get_by_test_id("inventory-item-price").inner_text()
  
  def get_inventory_item_description_by_index(self, index: int) -> str:
    return self.get_inventory_items.nth(index).get_by_test_id("inventory-item-desc").inner_text()
  