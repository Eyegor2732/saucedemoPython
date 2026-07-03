from page_objects.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page

    def navigate(self):
        super().navigate("https://www.saucedemo.com/")

    @property
    def login_credentials_container(self):
        return self.page.locator("#login_credentials")
    
    @property
    def login_passwords_container(self):
        return self.page.locator(".login_password")
    
    @property
    def error_message_container(self):
        return self.page.locator(".error-message-container")

    def login(self, username, password):
        self.page.get_by_placeholder("Username").fill(username)
        self.page.get_by_placeholder("Password").fill(password)
        self.page.get_by_role("button", name="Login").click()
