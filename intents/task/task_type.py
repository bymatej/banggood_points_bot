"""
Types of tasks on Banggood.
The name of the enum represents the Type, and the value of the enum is just an integer with no particular use.

Types:
    - Browse products and add 3 products to cart: BROWSE_ADD_3_PRODUCTS_TO_CART
    - Browse products and add 3 products to wish list: BROWSE_ADD_3_PRODUCTS_TO_WISH_LIST
    - Search products and add x products to cart: SEARCH_ADD_PRODUCTS_TO_CART
"""

import enum

from intents.task.task_data import TaskData


class Tasks(enum.Enum):
    BROWSE_ADD_3_PRODUCTS_TO_CART = 1
    BROWSE_ADD_3_PRODUCTS_TO_WISH_LIST = 2
    SEARCH_ADD_PRODUCTS_TO_CART = 3


def browse_add_3_products_to_cart():
    return TaskData(task_type=Tasks.BROWSE_ADD_3_PRODUCTS_TO_CART, main_css_class="browseAddcart",
                    identifier_for_logging="cart")


def browse_add_3_products_to_wish_list():
    return TaskData(task_type=Tasks.BROWSE_ADD_3_PRODUCTS_TO_WISH_LIST, main_css_class="wishlist",
                    identifier_for_logging="wish list")


def search_add_products_to_wish_list():
    return TaskData(task_type=Tasks.SEARCH_ADD_PRODUCTS_TO_CART, main_css_class="searchAddcart",
                    identifier_for_logging="cart")
