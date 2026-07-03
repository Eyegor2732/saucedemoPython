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