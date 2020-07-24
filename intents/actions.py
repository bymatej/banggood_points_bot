import logging
import re
import traceback
from time import sleep

from selenium.common.exceptions import WebDriverException

from conf.config import get_password
from conf.config import get_username
from intents.subactions import add_product_to_cart
from intents.subactions import find_task_button_and_click_it
from intents.subactions import get_list_of_products
from intents.subactions import switch_to_newly_opened_tab
from intents.task_data import TaskData
from intents.task_type import Tasks
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
    # todo: remember the product name and add it to the list so that we can remove it from cart later on
    # also, remember the quantity and if it is greater than 1, then do not remove the product, but subtract qty by 1
    task = TaskData(Tasks.BROWSE_ADD_3_PRODUCTS_TO_CART)
    tasks_tab = get_current_tab(browser)

    is_reward_received = find_task_button_and_click_it(browser, task)
    if is_reward_received:
        return

    switch_to_newly_opened_tab(browser, tasks_tab)
    product_li_elements = get_list_of_products(browser)

    successful_add_to_cart_count = 0
    for li_element in product_li_elements:
        try:
            add_product_to_cart(browser, li_element, task)
            successful_add_to_cart_count += 1
        except WebDriverException:
            logging.error("Unable to add product to cart")  # todo: specify which product
            logging.error(traceback.format_exc())  # Print stack trace
        finally:
            if successful_add_to_cart_count > 2:
                close_current_tab_and_switch_to_window(browser, tasks_tab)
                logging.info("Products that were added to cart are: {}".format(', '.join(task.products)))
                break
