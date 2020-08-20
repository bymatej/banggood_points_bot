import logging
import traceback

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options

from intents.actions import get_current_amount_of_points
from intents.actions import log_in
from intents.actions import log_out
from intents.actions import perform_browse_and_add_to_cart
from intents.actions import perform_browse_and_add_to_wish_list
from intents.actions import perform_check_in
from intents.actions import perform_search_and_add_to_cart
from intents.navigator import open_login_page
from intents.navigator import open_my_account_page
from intents.navigator import open_points_page
from intents.navigator import open_tasks_page

logging.info("\n\nThe Bot has started\n\n")

# Open Firefox browser
capabilities = DesiredCapabilities().FIREFOX
capabilities["marionette"] = True
options = Options()
options.headless = False  # todo: change to True when everything is finished
browser = webdriver.Firefox(capabilities=capabilities, options=options)
browser.implicitly_wait(10)  # wait 10 seconds for all DOM elements
# Open log-in page
open_login_page(browser)
# Log in
log_in(browser)


# Open points page and check points
def _get_points(when: bool) -> int:
    try:
        open_points_page(browser)
        return get_current_amount_of_points(browser, when)
    except WebDriverException:
        logging.error(f"Something went wrong while executing the task")
        logging.error(traceback.format_exc())
        return 0


points_before = _get_points(False)

# Open points page and perform check-in, open points page and check points
open_my_account_page(browser)
perform_check_in(browser)
_get_points(False)

# Open tasks page and perform tasks, open points page and check points after each task
open_tasks_page(browser)
perform_browse_and_add_to_cart(browser)
_get_points(False)
open_tasks_page(browser)
perform_browse_and_add_to_wish_list(browser)
_get_points(False)
open_tasks_page(browser)
perform_search_and_add_to_cart(browser)

# Open points page and check points
points_after = _get_points(True)
points_earned = points_after - points_before
logging.info(f"Earned {points_earned} points!")

# Log out
log_out(browser)
# Close browser
browser.quit()

logging.info("\n\nThe Bot has finished\n\n")
