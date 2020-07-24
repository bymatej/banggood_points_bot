"""
Task data containing the following information: 
    - task type: enum that determines the task type and it's XPATH for Banggood tasks page
    - products list: for tasks that add products to cart or wish list - products added will be remembered and removed
                     from cart/wish list after the task completion
"""


class TaskData:

    def __init__(self, task_type, identifier_for_logging):
        self.task_type = task_type
        self.identifier_for_logging = identifier_for_logging
        self.products = []
