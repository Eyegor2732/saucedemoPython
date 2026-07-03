from pathlib import Path
import json
import time
import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.usefixtures("setup_inventory_test")

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "datasets" / "inventory_sorting.json"
SESSION_COOKIE_FILE = BASE_DIR / "playwright" / ".auth" / "session-cookie.json"

with open(DATA_FILE) as f:
    test_data = json.load(f)
    inventory_sorting_list = test_data['inventory_sorting']

def test_inventory_page_basic(inventory_page):
    expect(inventory_page.get_page_title()).to_contain_text("Products")
    expect(inventory_page.getproduct_sort_dropdown()).to_be_visible()
    expect(inventory_page.getproduct_sort_dropdown()).to_have_value("az")
    expect(inventory_page.getproduct_sort_dropdown()).to_contain_text("Name (A to Z)")
    expect(inventory_page.get_inventory_items()).to_have_count(6)

@pytest.mark.parametrize('inventory_sorting', inventory_sorting_list)
def test_inventory_sorting(inventory_page, inventory_sorting):
    sort_option = inventory_sorting['select']
    by_name = inventory_sorting['isNameSort']
    is_ascending = inventory_sorting['isAscending']

    inventory_page.sort_and_verify_inventory(sort_option, by_name, is_ascending)

@pytest.mark.parametrize('inventory_sorting', inventory_sorting_list)
def test_product_information_remains_consistent_after_sorting(inventory_page, inventory_sorting):
    sort_option = inventory_sorting['select']
    by_name = inventory_sorting['isNameSort']
    is_ascending = inventory_sorting['isAscending']

    name_description_dict_before_sorting = inventory_page.get_dict_name_description()
    name_price_dict_before_sorting = inventory_page.get_dict_name_price()
    inventory_page.sort_and_verify_inventory(sort_option, by_name, is_ascending)
    name_description_dict_after_sorting = inventory_page.get_dict_name_description()
    name_price_dict_after_sorting = inventory_page.get_dict_name_price()

    assert name_description_dict_before_sorting == name_description_dict_after_sorting, \
        "Product information mismatch after sorting"
    
    assert name_price_dict_before_sorting == name_price_dict_after_sorting, \
        "Product price information mismatch after sorting"
    
def test_expired_cookies_should_not_allow_access_to_another_page(inventory_page):
    expect(inventory_page.get_page_title()).to_contain_text("Products")

    with open(SESSION_COOKIE_FILE) as f:
        auth_state = json.load(f)

    cookies = auth_state.get("cookies", [])
    assert cookies, "No cookies found in session-cookie.json"

    now_seconds = int(time.time())
    expired_cookies = [{**cookie, "expires": now_seconds} for cookie in cookies]

    inventory_page.page.context.add_cookies(expired_cookies)

    inventory_page.navigate_to_shopping_cart()
    expect(inventory_page.page).to_have_url("https://www.saucedemo.com/")