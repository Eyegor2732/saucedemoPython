from page_objects.base_page import BasePage

from utils.common_methods import parse_currency_string_to_float
import locale

class InventoryPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    @property
    def get_inventory_items(self):
        return self.page.get_by_test_id("inventory-item")
    
    @property
    def get_remove_buttons(self):
        return(self.page.get_by_role("button", name="Remove"))
    
    @property
    def get_add_to_cart_buttons(self):
        return self.page.get_by_role("button", name="Add to cart")
    
    def navigate(self):
        super().navigate("/inventory.html")
    
    def sort_inventory(self, sort_option):
        self.header.sorting_dropdown.select_option(sort_option)

    def get_item_name_by_index(self, index):
        return self.get_inventory_items.nth(index).get_by_test_id("inventory-item-name").inner_text()
    
    def get_item_price_by_index(self, index):
        return self.get_inventory_items.nth(index).get_by_test_id("inventory-item-price").inner_text()
    
    def get_item_description_by_index(self, index):
        return self.get_inventory_items.nth(index).get_by_test_id("inventory-item-desc").inner_text()

    def sort_and_verify_inventory(self, sort_option, by_name, is_ascending):
        item_count = self.get_inventory_items.count()
        if item_count < 2:
            return

        self.sort_inventory(sort_option)

        for i in range(item_count - 1):
            if by_name:
                current_name = self.get_item_name_by_index(i) or ""
                next_name = self.get_item_name_by_index(i + 1) or ""
                name_comparison = locale.strcoll(current_name, next_name)

                if is_ascending and name_comparison > 0:
                    raise ValueError(
                        f'Name sorting validation failed at index {i}: "{current_name}" should be before "{next_name}".'
                    )

                if not is_ascending and name_comparison < 0:
                    raise ValueError(
                        f'Name sorting validation failed at index {i}: "{current_name}" should be after "{next_name}".'
                    )
            else:
                current_price_text = self.get_item_price_by_index(i) or ""
                next_price_text = self.get_item_price_by_index(i + 1) or ""
                current_price = parse_currency_string_to_float(current_price_text)
                next_price = parse_currency_string_to_float(next_price_text)

                if is_ascending and current_price > next_price:
                    raise ValueError(
                        f"Price sorting validation failed at index {i}: {current_price_text} should be <= {next_price_text}."
                    )

                if not is_ascending and current_price < next_price:
                    raise ValueError(
                        f"Price sorting validation failed at index {i}: {current_price_text} should be >= {next_price_text}."
                    )
                
    def get_dict_name_description(self) -> dict[str, str]:
        name_description_dict: dict[str, str] = {}
        item_count = self.get_inventory_items.count()

        for i in range(item_count):
            name = self.get_item_name_by_index(i)
            description = self.get_item_description_by_index(i)

            if name and description:
                name_description_dict[name] = description

        return name_description_dict
    
    def get_dict_name_price(self) -> dict[str, str]:
        name_price_dict: dict[str, str] = {}
        item_count = self.get_inventory_items.count()

        for i in range(item_count):
            name = self.get_item_name_by_index(i)
            price = self.get_item_price_by_index(i)

            if name and price:
                name_price_dict[name] = price

        return name_price_dict
    
    def remove_all_items_from_cart(self):
        remove_buttons = self.get_remove_buttons
        while remove_buttons.count() > 0:
            remove_buttons.first.click()

    def add_item_to_cart_by_index(self, index):
        items = self.get_inventory_items
        if index < 0 or index >= items.count():
            raise IndexError(f"Index {index} is out of range for inventory items.")
        items.nth(index).get_by_role("button", name="Add to cart").click()  
