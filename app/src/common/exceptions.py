"""
Exceptions related to actions with products.
"""

from selenium.common.exceptions import WebDriverException


class ProductAlreadyInWishListException(WebDriverException):
    """
    Exception raised when product is already in the wish list, and should be skipped and the wish list button should
    not be clicked.
    """

    def __init__(self, product_name):
        self.product_name = product_name
        self.message = "Product {} already added to the wish list".format(product_name)
        super().__init__(msg=self.message)
