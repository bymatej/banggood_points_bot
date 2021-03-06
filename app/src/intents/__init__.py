from intents.actions import get_current_amount_of_points
from intents.actions import log_in
from intents.actions import log_out
from intents.actions import perform_browse_and_add_to_cart
from intents.actions import perform_browse_and_add_to_wish_list
from intents.actions import perform_check_in
from intents.actions import perform_search_and_add_to_cart
from intents.navigator import open_cart_page
from intents.navigator import open_login_page
from intents.navigator import open_my_account_page
from intents.navigator import open_points_page
from intents.navigator import open_tasks_page
from intents.navigator import open_wish_list_page
from intents.subactions import add_product_to_cart
from intents.subactions import add_product_to_wish_list
from intents.subactions import cleanup_cart
from intents.subactions import cleanup_wish_list
from intents.subactions import find_task_button_and_click_it
from intents.subactions import get_list_of_products
from intents.subactions import switch_to_newly_opened_tab
from intents.tasks import TaskData
from intents.tasks import TaskType
from intents.tasks import browse_add_3_products_to_cart
from intents.tasks import browse_add_3_products_to_wish_list
from intents.tasks import search_add_products_to_wish_list
from intents.utils import close_current_tab
from intents.utils import close_current_tab_and_switch_to_window
from intents.utils import get_current_tab
from intents.utils import get_last_opened_tab_id
from intents.utils import open_link_in_new_tab
from intents.utils import scroll_to_and_hover_over_element
from intents.utils import wait
