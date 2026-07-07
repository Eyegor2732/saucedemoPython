from playwright.sync_api import Locator, Page

from page_objects.base_page import BasePage

class CartPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page: Page = page

    def navigate(self) -> None:
        super().navigate("/cart.html")

    @property
    def cart_items(self) -> Locator:
        return self.page.get_by_test_id("inventory-item")
    
    @property
    def cart_item_names(self) -> Locator:
        return self.page.get_by_test_id("inventory-item-name")
    
    @property
    def cart_item_prices(self) -> Locator:
        return self.page.get_by_test_id("inventory-item-price")
    
    @property
    def cart_item_descriptions(self) -> Locator:
        return self.page.get_by_test_id("inventory-item-desc")

    @property
    def checkout_button(self) -> Locator:
        return self.page.get_by_role("button", name="Checkout")
    
    @property
    def continue_shopping_button(self) -> Locator:
        return self.page.get_by_role("button", name="Continue Shopping")
    
    @property
    def remove_buttons(self) -> Locator:
        return self.page.get_by_role("button", name="Remove")
    
    def get_cart_items_count(self) -> int:
        return self.cart_items.count()
    
    def navigate_continue_shopping(self) -> None:
        self.continue_shopping_button.click()

    def navigate_checkout(self) -> None:
        self.checkout_button.click()

    def remove_all_items_from_cart(self) -> None:
        count = self.remove_buttons.count()
        for _ in range(count):
            self.remove_buttons.first.click()

    def get_cart_item_name_by_index(self, index: int) -> str:
        return self.cart_item_names.nth(index).inner_text()

    def get_cart_item_price_by_index(self, index: int) -> str:
        return self.cart_item_prices.nth(index).inner_text()
    
    def get_cart_item_description_by_index(self, index: int) -> str:
        return self.cart_item_descriptions.nth(index).inner_text()

    def is_cart_empty(self) -> bool:
        return self.get_cart_items_count() == 0