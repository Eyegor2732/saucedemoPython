import pytest
import re
from playwright.sync_api import expect

@pytest.mark.usefixtures("setup_cart_test")
def test_TC_CART_06_verify_continue_shopping_button_functionality(cart_page, inventory_page):
    expect(cart_page.continue_shopping_button).to_be_visible()
    cart_page.navigate_continue_shopping()
    expect(inventory_page.header.get_page_title()).to_contain_text("Products")

@pytest.mark.usefixtures("setup_cart_test")
def test_verify_checkout_button_functionality(cart_page):
    expect(cart_page.checkout_button).to_be_visible()
    cart_page.navigate_checkout()
    expect(cart_page.page).to_have_url(re.compile(r"/checkout-step-one\.html$"))

@pytest.mark.usefixtures("setup_inventory_test")
def test_TC_CART_01_should_add_items_to_cart_and_verify_count(inventory_page, cart_page):
    item_count = inventory_page.get_inventory_items.count()
    for i in range(item_count):
        inventory_page.add_item_to_cart_by_index(i)
    expect(inventory_page.header.shopping_cart_badge).to_have_text(str(item_count))
    inventory_page.header.open_shopping_cart()
    expect(cart_page.page).to_have_url(re.compile(r"/cart\.html$"))
    expect(cart_page.cart_items).to_have_count(item_count)
    expect(cart_page.header.shopping_cart_badge).to_have_text(str(item_count))

@pytest.mark.usefixtures("setup_inventory_test")
def test_should_remove_items_from_cart_and_verify_count(inventory_page, cart_page):
    item_count = inventory_page.get_inventory_items.count()
    for i in range(item_count):
        inventory_page.add_item_to_cart_by_index(i)
    expect(inventory_page.header.shopping_cart_badge).to_have_text(str(item_count))
    inventory_page.header.open_shopping_cart()
    expect(cart_page.page).to_have_url(re.compile(r"/cart\.html$"))
    expect(cart_page.cart_items).to_have_count(item_count)
    expect(cart_page.header.shopping_cart_badge).to_have_text(str(item_count))
    cart_page.remove_all_items_from_cart()
    expect(cart_page.cart_items).to_have_count(0)  
    expect(cart_page.header.shopping_cart_badge).not_to_be_visible()

@pytest.mark.usefixtures("setup_inventory_test")
def test_TC_CART_05_verify_cart_item_information(inventory_page, cart_page):
    item_count = inventory_page.get_inventory_items.count()
    for index in range(item_count):
        inventory_page.add_item_to_cart_by_index(index)
    inventory_page.header.open_shopping_cart()
    expect(cart_page.page).to_have_url(re.compile(r"/cart\.html$"))

    expect(cart_page.cart_items).to_have_count(item_count)
    for index in range(cart_page.get_cart_items_count()):
        item_name = cart_page.get_cart_item_name_by_index(index)
        item_price = cart_page.get_cart_item_price_by_index(index)
        item_description = cart_page.get_cart_item_description_by_index(index)
        assert item_name, f"Item name is missing for cart item at index {index}"
        assert item_price, f"Item price is missing for cart item at index {index}"
        assert item_description, f"Item description is missing for cart item at index {index}"  