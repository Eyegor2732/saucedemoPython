from pathlib import Path
import sys
from playwright.sync_api import expect
import pytest

from page_objects.pages.login_page import LoginPage
from page_objects.pages.inventory_page import InventoryPage
from page_objects.pages.cart_page import CartPage
from utils.common_methods import create_saucedemo_session_cookie

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

SESSION_COOKIE_PATH = "playwright/.auth/session-cookie.json"

@pytest.fixture(scope="session", autouse=True)
def setup_auth(request, playwright):
    # skip setup if running only no-auth tests
    markexpr = request.config.getoption("markexpr") or ""
    if "no_auth" in markexpr and "not no_auth" not in markexpr:
        return
    browser = playwright.chromium.launch()
    context = browser.new_context()

    create_saucedemo_session_cookie(context)

    auth_state_path = Path(SESSION_COOKIE_PATH)
    auth_state_path.parent.mkdir(parents=True, exist_ok=True)
    context.storage_state(path=str(auth_state_path))

    context.close()
    browser.close()

@pytest.fixture(scope="class")
def browser_instance(playwright, request):
    browser_name = request.config.getoption("browser_name")
    # url_name = request.config.getoption("url_name")
    if browser_name == "chrome":
        browser = playwright.chromium.launch(headless=False)
    if browser_name == "chrome_headless":
        browser = playwright.chromium.launch(headless=True)
    elif browser_name == "firefox":
        browser = playwright.firefox.launch(headless=False)
    elif browser_name == "firefox_headless":
        browser = playwright.firefox.launch(headless=True)
    elif browser_name == "safari":
        browser = playwright.webkit.launch(headless=False)
    elif browser_name == "safari_headless":
        browser = playwright.webkit.launch(headless=True)
    elif browser_name == "edge":
        browser = playwright.chromium.launch(channel="msedge", headless=False)
    elif browser_name == "edge_headless":
        browser = playwright.chromium.launch(channel="msedge", headless=True)

    auth_state_path = Path(SESSION_COOKIE_PATH)
    if auth_state_path.exists():
        context = browser.new_context(storage_state=str(auth_state_path))
    else:
        context = browser.new_context()
    page = context.new_page()
    #page.goto(url_name)
    yield page
    context.close()
    browser.close()

@pytest.fixture()
def login_page(browser_instance):
    page = LoginPage(browser_instance)
    return page  

@pytest.fixture()
def inventory_page(browser_instance):
    page = InventoryPage(browser_instance)
    return page

@pytest.fixture()
def cart_page(browser_instance):
    page = CartPage(browser_instance)
    return page

@pytest.fixture()
def setup_inventory_test(inventory_page):
    inventory_page.navigate()
    expect(inventory_page.header.get_page_title()).to_contain_text("Products")
    yield
    inventory_page.remove_all_items_from_cart()

@pytest.fixture()
def setup_cart_test(cart_page):
    cart_page.navigate()
    expect(cart_page.header.get_page_title()).to_contain_text("Your Cart")
    # yield
    # cart_page.remove_all_items_from_cart()