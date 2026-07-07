from dataclasses import dataclass

@dataclass
class NegativeCheckoutOne:
  first_name: str
  last_name: str
  postal_code: str
  error_message: str
  id: str = ""

  def __post_init__(self):
    if not self.id:
      self.id = f"{self.first_name}-{self.last_name}-{self.postal_code}"

negative_checkout_one_cases: tuple[NegativeCheckoutOne, ...] = (
  NegativeCheckoutOne(
    "", 
    "", 
    "", 
    "Error: First Name is required"),
  NegativeCheckoutOne(
    "", 
    "L", 
    "1", 
    "Error: First Name is required"),
  NegativeCheckoutOne(
    "F", 
    "", 
    "1", 
    "Error: Last Name is required"),
  NegativeCheckoutOne(
    "F", 
    "L", 
    "", 
    "Error: Postal Code is required"),
)