from pathlib import Path
import json
import pytest

pytestmark = pytest.mark.usefixtures("setup_inventory_test")

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "datasets" / "inventory_sorting.json"
SESSION_COOKIE_FILE = BASE_DIR / "playwright" / ".auth" / "session-cookie.json"

with open(DATA_FILE) as f:
    test_data = json.load(f)
    inventory_sorting_list = test_data['inventory_sorting']

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
