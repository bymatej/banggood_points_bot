import logging
import re
import traceback
from time import sleep

from selenium.common.exceptions import WebDriverException

from conf.config import get_password
from conf.config import get_username
from intents.subactions import add_product_to_cart
from intents.subactions import add_product_to_wish_list
from intents.subactions import find_task_button_and_click_it
from intents.subactions import get_list_of_products
from intents.subactions import switch_to_newly_opened_tab
from intents.task.task_type import Tasks
from intents.task.task_type import browse_add_3_products_to_cart
from intents.task.task_type import browse_add_3_products_to_wish_list
from intents.utils import close_current_tab_and_switch_to_window
from intents.utils import get_current_tab
from intents.utils import wait

# todo: replace this with a better way of logging (to file and console) and with log rotation
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)


# Log in
def log_in(browser):
    logging.info("Getting email input field in the login form")
    email_login_input_field = browser.find_element_by_xpath("/html/body/div[1]/div/form[1]/ul/li[1]/label/div/input")

    logging.info("Getting password input field in the login form")
    password_login_input_field = browser.find_element_by_xpath("/html/body/div[1]/div/form[1]/ul/li[2]/label/div/input")

    logging.info("Filling out the login form")
    email_login_input_field.send_keys(get_username())
    password_login_input_field.send_keys(get_password())

    logging.info("Performing login (getting the button and clicking it)")
    browser.find_element_by_xpath("/html/body/div[1]/div/form[1]/ul/li[3]/input").click()

    wait()
    # assert "banggood" in browser.title.lower() # todo: fix


# Log out
def log_out(browser):
    # Sign out
    logging.info("Logging out")
    browser.get("https://www.banggood.com/")
    browser.get("https://www.banggood.com/index.php?com=account&t=logout")
    logging.info("Logout done!")


# Perform daily check-in
def perform_check_in(browser):
    logging.info("Clicking the check-in button (in sidebar)")
    browser.find_element_by_xpath("//*[contains(text(), 'Check-in')]").click()

    logging.info("Getting the button from the popup")
    check_in_button = browser.find_element_by_xpath("/html/body/div[1]/div[9]/div[2]/div/div[2]")
    if check_in_button.text.lower() == "check-in":
        logging.info("Clicking the check-in button")
        check_in_button.click()
        sleep(2)  # The get_sleep_time() method is not used as it always needs ~2 seconds here to view the popup
        # Click on the button on popup to close it
        browser.find_element_by_xpath("//*[contains(text(), 'OK, I know')]").click()
        logging.info("Check-in was successful")
    else:
        # Get time left for the next check-in
        logging.info("Not clicking a button. The text in the button was {}. Moving on".format(check_in_button.text))
        next_check_in = browser.find_element_by_class_name("countdown").text
        logging.info("Next check-in in: {}".format(re.search('(Restart In: )(.*)', next_check_in).group(2)))


# Complete task "Browse and add 3 products to cart" and get reward points
def perform_browse_and_add_to_cart(browser):
    __perform_browse_and_add(browser, browse_add_3_products_to_cart())


# Complete task "Browse and add 3 products to wish list" and get reward points
def perform_browse_and_add_to_wish_list(browser):
    __perform_browse_and_add(browser, browse_add_3_products_to_wish_list())


# Complete task "Search products and add to cart" and get reward points
def perform_search_and_add_to_cart(browser):
    logging.error("This feature is not yet implemented as it does not work properly on the Banggood side.")
    try:
        logging.error("Throwing error on purpose")
        raise NotImplementedError
    except NotImplementedError:
        logging.error("Not handling error on purpose")
        logging.error(traceback.format_exc())  # Print stack trace
        pass


def __perform_browse_and_add(browser, task_data):
    # todo: remember the product name and add it to the list so that we can remove it later on
    tasks_tab = get_current_tab(browser)

    is_reward_received = find_task_button_and_click_it(browser, task_data)
    if is_reward_received:
        return

    switch_to_newly_opened_tab(browser, tasks_tab)
    product_li_elements = get_list_of_products(browser)

    successfully_added_products_count = 0
    for li_element in product_li_elements:
        try:
            if task_data.task_type == Tasks.BROWSE_ADD_3_PRODUCTS_TO_CART:
                add_product_to_cart(browser, li_element, task_data)
            else:
                add_product_to_wish_list(browser, li_element, task_data)

            successfully_added_products_count += 1
        except WebDriverException:
            logging.error("Unable to add product to {}".format(task_data.identifier_for_logging))
            logging.error(traceback.format_exc())  # Print stack trace
            close_current_tab_and_switch_to_window(browser, tasks_tab)
        finally:
            if successfully_added_products_count > 2:
                close_current_tab_and_switch_to_window(browser, tasks_tab)
                logging.info("Products that were added to {} are: {}".format(task_data.identifier_for_logging,
                                                                             ', '.join(task_data.products)))
                break
