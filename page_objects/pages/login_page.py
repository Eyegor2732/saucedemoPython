from page_objects.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page

    def navigate(self):
        super().navigate("/")

    @property
    def login_credentials_container(self):
        return self.page.get_by_test_id("login-credentials")
    
    @property
    def login_passwords_container(self):
        return self.page.get_by_test_id("login-password")
    
    @property
    def error_message_container(self):
        return self.page.locator(".error-message-container")
    
    @property
    def username_input(self):
        return self.page.get_by_placeholder("Username")
    
    @property
    def password_input(self):
        return self.page.get_by_placeholder("Password")
    
    @property
    def login_button(self):
        return self.page.get_by_role("button", name="Login")
    
    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
