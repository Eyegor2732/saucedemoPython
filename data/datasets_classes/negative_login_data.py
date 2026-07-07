from dataclasses import dataclass

@dataclass
class NegativeLogin:
  test_case: str
  title: str
  username: str
  password: str
  message: str
  id: str = ""

  def __post_init__(self):
    if not self.id:
      self.id = f"{self.test_case}-{self.title}"

negative_login_cases: tuple[NegativeLogin, ...] = ( 
  NegativeLogin(
    "TC-LOGIN-02", 
    "wrong username, correct password", 
    "invalid_user", 
    "secret_sauce", 
    "Username and password do not match any user in this service"),
  NegativeLogin(
    "TC-LOGIN-03", 
    "correct username, wrong password", 
    "standard_user", 
    "wrong_password", 
    "Username and password do not match any user in this service"),
  NegativeLogin(
    "TC-LOGIN-04", 
    "wrong username, wrong password", 
    "invalid_user", 
    "invalid_password", 
    "Username and password do not match any user in this service"),
  NegativeLogin(
    "TC-LOGIN-05", 
    "correct username with leading spaces, correct password", 
    "   standard_user", 
    "secret_sauce", 
    "Username and password do not match any user in this service"),
  NegativeLogin(
    "TC-LOGIN-06", 
    "correct username with trailing spaces, correct password", 
    "standard_user   ", 
    "secret_sauce", 
    "Username and password do not match any user in this service"),
  NegativeLogin(
    "TC-LOGIN-07", 
    "correct username, correct password with leading spaces", 
    "standard_user", 
    "   secret_sauce", 
    "Username and password do not match any user in this service"),
  NegativeLogin(
    "TC-LOGIN-08", 
    "correct username, correct password with trailing spaces", 
    "standard_user", 
    "secret_sauce   ", 
    "Username and password do not match any user in this service"),
  NegativeLogin(
    "TC-LOGIN-09", 
    "blank username, correct password", 
    "", 
    "secret_sauce", 
    "Username is required"),
  NegativeLogin(
    "TC-LOGIN-10", 
    "correct username, blank password", 
    "standard_user", 
    "", 
    "Password is required"), 
  NegativeLogin(
    "TC-LOGIN-11", 
    "blank username, blank password", 
    "", 
    "", 
    "Username is required"),
  NegativeLogin(
    "TC-LOGIN-12", 
    "locked out user", 
    "locked_out_user", 
    "secret_sauce", 
    "Sorry, this user has been locked out"),
)
