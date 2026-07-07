import pytest
import re
from playwright.sync_api import expect

@pytest.mark.usefixtures("setup_checkout_one_test")
def test_empty_checkout_information(negative_checkout_one, checkout_one_page):
    first_name = negative_checkout_one.first_name
    last_name = negative_checkout_one.last_name
    postal_code = negative_checkout_one.postal_code
    error_message = negative_checkout_one.error_message

    checkout_one_page.perform_checkout(first_name, last_name, postal_code)
    expect(checkout_one_page.error_message_container).to_contain_text(error_message)

@pytest.mark.usefixtures("setup_checkout_one_test")
def test_verify_cancel_button_functionality(checkout_one_page, cart_page):
  expect(checkout_one_page.cancel_button).to_be_visible()
  checkout_one_page.navigate_cancel()
  expect(cart_page.page).to_have_url(re.compile(r"/cart\.html$"))
  expect(cart_page.header.get_page_title()).to_contain_text("Your Cart")

@pytest.mark.usefixtures("setup_checkout_one_test")
def test_verify_continue_button_functionality(checkout_one_page, checkout_two_page):
  expect(checkout_one_page.continue_button).to_be_visible()
  checkout_one_page.perform_checkout("John", "Doe", "12345")
  expect(checkout_two_page.page).to_have_url(re.compile(r"/checkout-step-two\.html$"))
  expect(checkout_two_page.header.get_page_title()).to_contain_text("Checkout: Overview")