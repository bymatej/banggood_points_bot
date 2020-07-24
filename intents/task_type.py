"""
Types of tasks containing the XPATH for their buttons.
The name of the enum represents the Type, and the value of enum represents the XPATH.

Types:
    - Browse products and add 3 products to cart: BROWSE_ADD_3_PRODUCTS_TO_CART
    - Browse products and add 3 products to wish list: BROWSE_ADD_3_PRODUCTS_TO_WISH_LIST
    - Search products and add x products to cart: SEARCH_ADD_X_PRODUCTS_TO_CART  # todo: find out the value of X
"""

import enum


class Tasks(enum.Enum):
    BROWSE_ADD_3_PRODUCTS_TO_CART = "//li[contains(@class, 'item') and contains(@class, 'browseAddcart')]"
    BROWSE_ADD_3_PRODUCTS_TO_WISH_LIST = ""
    SEARCH_ADD_X_PRODUCTS_TO_CART = ""
