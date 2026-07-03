from pathlib import Path
import json
import pytest
from playwright.sync_api import expect

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE_POSITIVE = BASE_DIR / "data" / "datasets" / "positive_login.json"
DATA_FILE_NEGATIVE = BASE_DIR / "data" / "datasets" / "negative_login.json"

with open(DATA_FILE_NEGATIVE) as fn:
    test_data = json.load(fn)
    negative_login_list = test_data['negative_login']

with open(DATA_FILE_POSITIVE) as fp:
    test_data = json.load(fp)
    positive_login_list = test_data['positive_login']

@pytest.mark.no_auth
@pytest.mark.parametrize('positive_login', positive_login_list)
def test_login(login_page, inventory_page, positive_login):
    user_name = positive_login["username"]
    user_password = positive_login["password"]

    login_page.navigate()
    login_page.login(user_name, user_password)

    expect(inventory_page.get_page_title()).to_contain_text("Products")
    expect(inventory_page.getproduct_sort_dropdown()).to_be_visible()
    expect(inventory_page.getproduct_sort_dropdown()).to_have_value("az")
    expect(inventory_page.getproduct_sort_dropdown()).to_contain_text("Name (A to Z)")

@pytest.mark.no_auth
@pytest.mark.parametrize('negative_login', negative_login_list)
def test_negative_login(login_page, negative_login):
    user_name = negative_login["username"]
    user_password = negative_login["password"]

    login_page.navigate()
    login_page.login(user_name, user_password)
    login_page.page.wait_for_timeout(2000)

    expect(login_page.get_error_message()).to_contain_text(negative_login["message"])