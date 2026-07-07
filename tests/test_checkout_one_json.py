from pathlib import Path
import json
import pytest
from playwright.sync_api import expect

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "datasets" / "negative_checkout.json"

with open(DATA_FILE) as f:
  NEGATIVE_CHECKOUT_DATA = json.load(f)
  negative_checkout_list = NEGATIVE_CHECKOUT_DATA['negative_checkout']

@pytest.mark.usefixtures("setup_checkout_one_test")
@pytest.mark.parametrize('negative_checkout', negative_checkout_list)
def test_empty_checkout_information(negative_checkout, checkout_one_page):
  first_name = negative_checkout["first_name"]
  last_name = negative_checkout["last_name"]
  postal_code = negative_checkout["postal_code"]
  error_message = negative_checkout["error_message"]

  checkout_one_page.perform_checkout(first_name, last_name, postal_code)
  expect(checkout_one_page.error_message_container).to_contain_text(error_message)
