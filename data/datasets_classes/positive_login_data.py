from dataclasses import dataclass

@dataclass
class PositiveLogin:
  test_case: str
  title: str
  username: str
  password: str
  id: str = ""

  def __post_init__(self):
    if not self.id:
      self.id = f"{self.test_case}-{self.title}"

positive_login_cases: tuple[PositiveLogin, ...] = (
  PositiveLogin(
    "TC-LOGIN-01", 
    "standard_user with correct password", 
    "standard_user", 
    "secret_sauce"),
  PositiveLogin(
    "TC-LOGIN-13", 
    "problem_user with correct password", 
    "problem_user", 
    "secret_sauce"),
  PositiveLogin(
    "TC-LOGIN-14", 
    "performance_glitch_user with correct password", 
    "performance_glitch_user", 
    "secret_sauce"),
  PositiveLogin(
    "TC-LOGIN-15", 
    "error_user with correct password", 
    "error_user", 
    "secret_sauce"),
  PositiveLogin(
    "TC-LOGIN-16", 
    "visual_user with correct password", 
    "visual_user", 
    "secret_sauce"),
)