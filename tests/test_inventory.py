from pathlib import Path
import json
import time
import pytest
import re
from playwright.sync_api import expect

pytestmark = pytest.mark.usefixtures("setup_inventory_test")

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "datasets" / "inventory_sorting.json"
SESSION_COOKIE_FILE = BASE_DIR / "playwright" / ".auth" / "session-cookie.json"

with open(DATA_FILE) as f:
    test_data = json.load(f)
    inventory_sorting_list = test_data['inventory_sorting']

def test_inventory_page_basic(inventory_page):
    expect(inventory_page.header.sorting_dropdown).to_be_visible()
    expect(inventory_page.header.sorting_dropdown).to_have_value("az")
    expect(inventory_page.header.sorting_dropdown).to_contain_text("Name (A to Z)")
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
    
def test_TC_PRODUCT_11_expired_cookies_should_not_allow_access_to_another_page(inventory_page, login_page):
    cookies = inventory_page.page.context.cookies()
    assert cookies, "No cookies found in session-cookie.json"
    now_seconds = int(time.time())
    expired_cookies = [{**cookie, "expires": now_seconds} for cookie in cookies]
    inventory_page.page.context.add_cookies(expired_cookies)
    inventory_page.header.open_shopping_cart()
    expect(inventory_page.page).to_have_url("https://www.saucedemo.com/")
    expect(login_page.error_message_container).to_be_visible()
    expect(login_page.error_message_container).to_contain_text(re.compile(r"You can only access '.*?' when you are logged in"))

def test_logout_should_clean_cookies(inventory_page, login_page):
    cookies_before = inventory_page.page.context.cookies()
    assert cookies_before, "No cookies found before logout"
    inventory_page.header.open_menu()
    inventory_page.menu.logout_button.click()
    expect(inventory_page.page).to_have_url("https://www.saucedemo.com/")
    expect(login_page.login_credentials_container).to_be_visible()
    cookies_after = inventory_page.page.context.cookies()
    assert not cookies_after, "Cookies should be cleared after logout"

def test_about_should_open_saucelabs_website(inventory_page):
    inventory_page.header.open_menu()
    inventory_page.menu.about_button.click()
    expect(inventory_page.page).to_have_url(re.compile(r"saucelabs\.com"))