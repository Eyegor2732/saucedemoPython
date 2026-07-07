from pathlib import Path
import sys
from playwright.sync_api import Browser, Page, expect, Playwright, BrowserContext
import pytest
from pytest import FixtureRequest

from page_objects.pages.login_page import LoginPage
from page_objects.pages.inventory_page import InventoryPage
from page_objects.pages.cart_page import CartPage
from page_objects.pages.checkout_one_page import CheckoutOnePage
from page_objects.pages.checkout_two_page import CheckoutTwoPage
from utils.common_methods import create_saucedemo_session_cookie
from data.datasets_classes.negative_checkout_one_data import negative_checkout_one_cases
from data.datasets_classes.inventory_sorting_data import inventory_sorting_cases, inventory_sorting_dict_cases
from data.datasets_classes.negative_login_data import negative_login_cases
from data.datasets_classes.positive_login_data import positive_login_cases

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

SESSION_COOKIE_PATH = "playwright/.auth/session-cookie.json"

@pytest.fixture(scope="session", autouse=True)
def setup_auth(request: FixtureRequest, playwright: Playwright):
    # skip setup if running only no-auth tests
    markexpr = request.config.getoption("markexpr") or ""
    if "no_auth" in markexpr and "not no_auth" not in markexpr:
        return
    browser: Browser = playwright.chromium.launch()
    context: BrowserContext = browser.new_context()

    create_saucedemo_session_cookie(context)

    auth_state_path = Path(SESSION_COOKIE_PATH)
    auth_state_path.parent.mkdir(parents=True, exist_ok=True)
    context.storage_state(path=str(auth_state_path))

    context.close()
    browser.close()

@pytest.fixture(scope="session", autouse=True)
def set_custom_test_id(playwright: Playwright):
    # Change 'data-testid' to 'data-test' for test id selectors
    playwright.selectors.set_test_id_attribute("data-test")

@pytest.fixture(scope="class")
def browser_instance(playwright: Playwright, request: FixtureRequest):
    browser_name: str = request.config.getoption("browser_name")

    if browser_name == "chrome":
        browser: Browser = playwright.chromium.launch(headless=False)
    if browser_name == "chrome_headless":
        browser: Browser = playwright.chromium.launch(headless=True)
    elif browser_name == "firefox":
        browser: Browser = playwright.firefox.launch(headless=False)
    elif browser_name == "firefox_headless":
        browser: Browser = playwright.firefox.launch(headless=True)
    elif browser_name == "safari":
        browser: Browser = playwright.webkit.launch(headless=False)
    elif browser_name == "safari_headless":
        browser: Browser = playwright.webkit.launch(headless=True)
    elif browser_name == "edge":
        browser: Browser = playwright.chromium.launch(channel="msedge", headless=False)
    elif browser_name == "edge_headless":
        browser: Browser = playwright.chromium.launch(channel="msedge", headless=True)

    auth_state_path: Path = Path(SESSION_COOKIE_PATH)
    if auth_state_path.exists():
        context: BrowserContext = browser.new_context(storage_state=str(auth_state_path))
    else:
        context: BrowserContext = browser.new_context()

    page: Page = context.new_page()

    yield page
    context.close()
    browser.close()

@pytest.fixture()
def login_page(browser_instance: Page):
    page: LoginPage = LoginPage(browser_instance)
    return page  

@pytest.fixture()
def inventory_page(browser_instance: Page):
    page: InventoryPage = InventoryPage(browser_instance)
    return page

@pytest.fixture()
def cart_page(browser_instance: Page):
    page: CartPage = CartPage(browser_instance)
    return page

@pytest.fixture()
def checkout_one_page(browser_instance: Page):
    page: CheckoutOnePage = CheckoutOnePage(browser_instance)
    return page

@pytest.fixture()
def checkout_two_page(browser_instance: Page):
    page: CheckoutTwoPage = CheckoutTwoPage(browser_instance)
    return page

@pytest.fixture()
def setup_inventory_test(inventory_page: InventoryPage):
    inventory_page.navigate()
    expect(inventory_page.header.get_page_title()).to_contain_text("Products")

@pytest.fixture()
def setup_checkout_one_test(checkout_one_page: CheckoutOnePage):
    checkout_one_page.navigate()
    expect(checkout_one_page.header.get_page_title()).to_contain_text("Checkout: Your Information")

@pytest.fixture()
def setup_checkout_two_test(checkout_two_page: CheckoutTwoPage):
    checkout_two_page.navigate()
    expect(checkout_two_page.header.get_page_title()).to_contain_text("Checkout: Overview")

@pytest.fixture()
def setup_cart_test(cart_page: CartPage):
    cart_page.navigate()
    expect(cart_page.header.get_page_title()).to_contain_text("Your Cart")

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item):
    """Expose setup/call/teardown reports on the test item for fixtures."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

@pytest.fixture(autouse=True)
def browser_screenshot(request: FixtureRequest, browser_instance: Page):
    """Take a screenshot when setup, call, or teardown fails."""
    yield

    rep_setup = getattr(request.node, "rep_setup", None)
    rep_call = getattr(request.node, "rep_call", None)
    rep_teardown = getattr(request.node, "rep_teardown", None)

    phase_reports = [
        ("setup", rep_setup),
        ("call", rep_call),
        ("teardown", rep_teardown),
    ]
    failed_phases = [
        phase
        for phase, rep in phase_reports
        if rep and rep.failed and not hasattr(rep, "wasxfail")
    ]
    if not failed_phases:
        return

    # Create screenshots folder and unique screenshot png file name.
    raw_name: str = request.node.nodeid
    safe_name: str = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in raw_name)
    phase_suffix: str = "__".join(failed_phases)
    screenshots_dir: Path = PROJECT_ROOT / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    # Do not fail teardown if screenshot capture is not possible.
    try:
        if not browser_instance.is_closed():
            browser_instance.screenshot(
                path=str(screenshots_dir / f"{safe_name}__{phase_suffix}.png"),
                full_page=True,
            )
    except Exception:
        pass

@pytest.fixture(params=negative_checkout_one_cases, ids=lambda c: c.id)
def negative_checkout_one(request):
    return request.param

@pytest.fixture(params=inventory_sorting_cases, ids=lambda c: c.id)
def inventory_sorting(request):
    return request.param

@pytest.fixture(params=inventory_sorting_dict_cases, ids=lambda c: c.id)
def inventory_sorting_dict(request):
    return request.param

@pytest.fixture(params=negative_login_cases, ids=lambda c: c.id)
def negative_login(request):
    return request.param

@pytest.fixture(params=positive_login_cases, ids=lambda c: c.id)
def positive_login(request):
    return request.param