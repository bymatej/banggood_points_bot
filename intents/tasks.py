import enum


class Tasks(enum.Enum):
    BROWSE_ADD_3_PRODUCTS_TO_CART = 1
    BROWSE_ADD_3_PRODUCTS_TO_WISH_LIST = 2
    SEARCH_ADD_PRODUCTS_TO_CART = 3


class TaskData:
    """
    Task data containing the following information:
        - task type: enum that determines the task type on Banggood
        - main css class: css class used for html elements (useful for xpath querying)
        - xpath: xpath for task button on the task page
        - modal_css_class: css class used in modal popups (prefixed with "modal-", useful for xpath querying)
        - identifier for logging: used only in log outputs
        - products list: for tasks that add products to cart or wish list - products added will be remembered and removed
                         from cart/wish list after the task completion
    """

    def __init__(self, task: Tasks, main_css_class: str, identifier_for_logging: str):
        self.task = task
        self.main_css_class = main_css_class
        self.xpath = f"//li[contains(@class, 'item') and contains(@class, '{main_css_class}')]"
        self.modal_css_class = f"modal-{main_css_class}"
        self.identifier_for_logging = identifier_for_logging
        self.products = []


class TaskType:
    """
    Types of tasks on Banggood.
    The name of the enum represents the Type, and the value of the enum is just an integer with no particular use.

    Types:
        - Browse products and add 3 products to cart: BROWSE_ADD_3_PRODUCTS_TO_CART
        - Browse products and add 3 products to wish list: BROWSE_ADD_3_PRODUCTS_TO_WISH_LIST
        - Search products and add x products to cart: SEARCH_ADD_PRODUCTS_TO_CART
    """

    @staticmethod
    def browse_add_3_products_to_cart():
        return TaskData(task=Tasks.BROWSE_ADD_3_PRODUCTS_TO_CART, main_css_class="browseAddcart",
                        identifier_for_logging="cart")

    @staticmethod
    def browse_add_3_products_to_wish_list():
        return TaskData(task=Tasks.BROWSE_ADD_3_PRODUCTS_TO_WISH_LIST, main_css_class="wishlist",
                        identifier_for_logging="wish list")

    @staticmethod
    def search_add_products_to_wish_list():
        return TaskData(task=Tasks.SEARCH_ADD_PRODUCTS_TO_CART, main_css_class="searchAddcart",
                        identifier_for_logging="cart")
