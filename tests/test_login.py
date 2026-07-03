from pathlib import Path
import json
import time
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

    expect(inventory_page.header.get_page_title()).to_contain_text("Products")

@pytest.mark.no_auth
@pytest.mark.parametrize('negative_login', negative_login_list)
def test_negative_login(login_page, negative_login):
    user_name = negative_login["username"]
    user_password = negative_login["password"]

    login_page.navigate()
    login_page.login(user_name, user_password)

    expect(login_page.error_message_container).to_contain_text(negative_login["message"])
    expect(login_page.login_credentials_container).to_be_visible()

@pytest.mark.no_auth
def test_login_with_performance_glitch_user(login_page, inventory_page):
    user_name = "performance_glitch_user"
    user_password = "secret_sauce"

    startTime = int(time.time())
    login_page.navigate()   
    login_page.login(user_name, user_password)
    expect(inventory_page.header.get_page_title()).to_contain_text("Products")
    endTime = int(time.time())

    assert (endTime - startTime) > 4, "Login took shorter than 4 seconds"
    