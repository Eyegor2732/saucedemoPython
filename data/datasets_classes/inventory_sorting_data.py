from dataclasses import dataclass

@dataclass
class InventorySorting:
  test_case: str
  title: str
  select: str
  isNameSort: bool
  isAscending: bool
  id: str = ""

  def __post_init__(self):
    if not self.id:
      self.id = f"{self.test_case}-{self.title}"

inventory_sorting_cases: tuple[InventorySorting, ...] = (
  InventorySorting(
    "TC-PRODUCT-02", 
    "Name (A to Z)", 
    "az", 
    True, 
    True),
  InventorySorting(
    "TC-PRODUCT-03", 
    "Name (Z to A)", 
    "za", 
    True, 
    False),
  InventorySorting(
    "TC-PRODUCT-04", 
    "Price (low to high)", 
    "lohi", 
    False, 
    True),
  InventorySorting(
    "TC-PRODUCT-05", 
    "Price (high to low)", 
    "hilo", 
    False, 
    False),
)

inventory_sorting_dict_cases: tuple[InventorySorting, ...] = (
  InventorySorting(
    "TC-PRODUCT-07", 
    "Name (A to Z)", 
    "az", 
    True, 
    True),
  InventorySorting(
    "TC-PRODUCT-08", 
    "Name (Z to A)", 
    "za", 
    True, 
    False),
  InventorySorting(
    "TC-PRODUCT-09", 
    "Price (low to high)", 
    "lohi", 
    False, 
    True),
  InventorySorting(
    "TC-PRODUCT-10", 
    "Price (high to low)", 
    "hilo", 
    False, 
    False),
)