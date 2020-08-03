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

from intents.task import TaskType


class TaskData:

    def __init__(self, task_type: TaskType, main_css_class: str, identifier_for_logging: str):
        self.task_type = task_type
        self.main_css_class = main_css_class
        self.xpath = f"//li[contains(@class, 'item') and contains(@class, '{main_css_class}')]"
        self.modal_css_class = f"modal-{main_css_class}"
        self.identifier_for_logging = identifier_for_logging
        self.products = []
