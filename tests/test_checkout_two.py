import pytest
import re
from playwright.sync_api import expect
from utils.common_methods import parse_currency_string_to_float

@pytest.mark.usefixtures("setup_inventory_test")
def test_verify_items_in_checkout(inventory_page, checkout_two_page):
  item_count = inventory_page.get_inventory_items.count()
  for index in range(item_count):
    inventory_page.add_item_to_cart_by_index(index)

  checkout_two_page.navigate()
  expect(checkout_two_page.page).to_have_url(re.compile(r"/checkout-step-two\.html$"))
  expect(checkout_two_page.header.get_page_title()).to_contain_text("Checkout: Overview")

  for index in range(checkout_two_page.get_inventory_items.count()):
    checkout_item_name = checkout_two_page.get_inventory_item_name_by_index(index)
    checkout_item_price = checkout_two_page.get_inventory_item_price_by_index(index)
    checkout_item_description = checkout_two_page.get_inventory_item_description_by_index(index)

    inventory_item_name = inventory_page.get_item_name_by_index(index)
    inventory_item_price = inventory_page.get_item_price_by_index(index)
    inventory_item_description = inventory_page.get_item_description_by_index(index)

    assert checkout_item_name == inventory_item_name, f"Item name mismatch at index {index}: expected '{inventory_item_name}', got '{checkout_item_name}'"
    assert parse_currency_string_to_float(checkout_item_price) == parse_currency_string_to_float(inventory_item_price), f"Item price mismatch at index {index}: expected '{inventory_item_price}', got '{checkout_item_price}'"
    assert checkout_item_description == inventory_item_description, f"Item description mismatch at index {index}: expected '{inventory_item_description}', got '{checkout_item_description}'"

@pytest.mark.usefixtures("setup_inventory_test")
def test_verify_tax_and_total_price(inventory_page, checkout_two_page):
    item_count = inventory_page.get_inventory_items.count()
    subtotal_price = 0.0

    for index in range(item_count):
      inventory_page.add_item_to_cart_by_index(index)

    checkout_two_page.navigate()
    expect(checkout_two_page.page).to_have_url(re.compile(r"/checkout-step-two\.html$"))
    expect(checkout_two_page.header.get_page_title()).to_contain_text("Checkout: Overview")

    item_count_checkout = checkout_two_page.get_inventory_items.count()
    assert item_count_checkout == item_count, f"Item count mismatch: expected {item_count}, got {item_count_checkout}"

    for index in range(item_count_checkout):
      checkout_item_price = checkout_two_page.get_inventory_item_price_by_index(index)
      assert parse_currency_string_to_float(checkout_item_price) == parse_currency_string_to_float(inventory_page.get_item_price_by_index(index)), f"Item price mismatch at index {index}: expected '{inventory_page.get_item_price_by_index(index)}', got '{checkout_item_price}'"
      subtotal_price += parse_currency_string_to_float(checkout_item_price)

    tax_amount = parse_currency_string_to_float(checkout_two_page.get_tax_amount())
    subtotal_amount = parse_currency_string_to_float(checkout_two_page.get_subtotal_amount())
    assert subtotal_amount == subtotal_price, f"Subtotal price mismatch: expected '{subtotal_price}', got '{subtotal_amount}'"

    expected_total = subtotal_amount + tax_amount
    actual_total = parse_currency_string_to_float(checkout_two_page.get_total_amount())
    assert actual_total == expected_total, f"Total price mismatch: expected '{expected_total}', got '{actual_total}'"