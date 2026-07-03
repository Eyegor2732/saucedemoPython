class CartPage:
    def __init__(self, page):
        self.page = page

    def navigate(self):
        self.page.goto("https://www.saucedemo.com/cart.html")
