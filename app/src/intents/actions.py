"""
Actions represent the actions that the bot needs to complete in order to finish the tasks.
Example of those actions are logging in, logging out, finishing the banggood tasks, etc.
"""

import logging
import re
import traceback
from time import sleep

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox import webdriver

from conf.config import get_password
from conf.config import get_username
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
from intents.utils import close_current_tab_and_switch_to_window
from intents.utils import get_current_tab
from intents.utils import wait

# todo: replace this with a better way of logging (to file and console) and with log rotation
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)


# Log in
def log_in(browser: webdriver.WebDriver):
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


# Log out
def log_out(browser: webdriver.WebDriver):
    # Sign out
    logging.info("Logging out")
    browser.get("https://www.banggood.com/")
    browser.get("https://www.banggood.com/index.php?com=account&t=logout")
    logging.info("Logout done!")


# Perform daily check-in
def perform_check_in(browser: webdriver.WebDriver):
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
def perform_browse_and_add_to_cart(browser: webdriver.WebDriver):
    _perform_browse_and_add(browser, browse_add_3_products_to_cart())


# Complete task "Browse and add 3 products to wish list" and get reward points
def perform_browse_and_add_to_wish_list(browser: webdriver.WebDriver):
    _perform_browse_and_add(browser, browse_add_3_products_to_wish_list())


# Complete task "Search products and add to cart" and get reward points
def perform_search_and_add_to_cart(browser: webdriver.WebDriver):
    logging.error("This feature is not yet implemented as it does not work properly on the Banggood side.")
    try:
        logging.error("Throwing error on purpose")
        raise NotImplementedError
    except NotImplementedError:
        logging.error("Not handling error on purpose")
        logging.error(traceback.format_exc())  # Print stack trace
        pass


# Check the amount of points
def get_current_amount_of_points(browser: webdriver.WebDriver, is_before_tasks: bool):
    available_points_div_xpath = "//div[contains(@class, 'myaccount-points-total')]" \
                                 "//ul//li//div[contains(@class, 'number')]"
    points_xpath = f"{available_points_div_xpath}//p[contains(@class, 'num-p')]"
    cash_xpath = f"{available_points_div_xpath}//span[contains(@class, 'cash')]"

    when = "after"
    if is_before_tasks:
        when = "before"

    points = int(browser.find_element_by_xpath(points_xpath).text)
    cash = browser.find_element_by_xpath(cash_xpath).text
    logging.info("\n\n")
    logging.info(f"\n\nPoints {when} check-in and tasks are completed: {points}")
    logging.info(f"Cash {when} check-in and tasks are completed: {cash}\n")

    return points


def _perform_browse_and_add(browser: webdriver.WebDriver, task_data: TaskData):
    # todo:
    # - wrap each task in try/catch and if a task fails don't let the app fail, but just move to the next task
    # - write down (in logger) the amount of points before and after each task (and after all tasks)
    # - fill out __init.py__ file(s)
    # - refactor imports if necessary
    is_reward_received = find_task_button_and_click_it(browser, task_data)
    if is_reward_received:
        return

    tasks_tab = get_current_tab(browser)
    switch_to_newly_opened_tab(browser, tasks_tab)
    product_li_elements = get_list_of_products(browser)

    successfully_added_products_count = 0
    for li_element in product_li_elements:
        try:
            if task_data.task_type == TaskType.BROWSE_ADD_3_PRODUCTS_TO_CART:
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
                logging.info("Products that were added to {} are: {}".format(task_data.identifier_for_logging,
                                                                             ', '.join(task_data.products)))
                _cleanup(browser, task_data)
                close_current_tab_and_switch_to_window(browser, tasks_tab)
                break


# Clean up the products from cart/wish list added from the task
def _cleanup(browser: webdriver.WebDriver, task_data: TaskData):
    if task_data.task_type == TaskType.BROWSE_ADD_3_PRODUCTS_TO_CART:
        logging.info("Cleaning up the products from the cart added from the task")
        cleanup_cart(browser, task_data)
    else:
        logging.info("Cleaning up the products from the wish list added from the task")
        cleanup_wish_list(browser, task_data)
