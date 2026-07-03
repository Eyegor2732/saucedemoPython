from page_objects.base_page import BasePage

class CartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def navigate(self):
        super().navigate("/cart.html")

    @property
    def cart_items(self):
        return self.page.locator(".cart_item")
    
    @property
    def cart_item_names(self):
        return self.page.locator(".inventory_item_name")
    
    @property
    def cart_item_prices(self):
        return self.page.locator(".inventory_item_price")
    
    @property
    def cart_item_descriptions(self):
        return self.page.locator(".inventory_item_desc")

    @property
    def checkout_button(self):
        return self.page.get_by_role("button", name="Checkout")
    
    @property
    def continue_shopping_button(self):
        return self.page.get_by_role("button", name="Continue Shopping")
    
    @property
    def remove_buttons(self):
        return self.page.get_by_role("button", name="Remove")
    
    def get_cart_items_count(self):
        return self.cart_items.count()
    
    def navigate_continue_shopping(self):
        self.continue_shopping_button.click()

    def navigate_checkout(self):
        self.checkout_button.click()

    def remove_all_items_from_cart(self):
        count = self.remove_buttons.count()
        for _ in range(count):
            self.remove_buttons.first.click()
