import logging
import traceback
from time import sleep

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from conf.config import get_password
from conf.config import get_username
from intents.utils import close_current_tab
from intents.utils import close_current_tab_and_switch_to_window
from intents.utils import get_current_tab
from intents.utils import open_link_in_new_tab
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
        logging.info(next_check_in)  # Todo: remove the "RESTART-IN" and seconds using regex


# Complete task "Search products and add to cart" and get reward points
def perform_products_search_and_add_to_cart(browser):
    tasks_tab = get_current_tab(browser)
    is_button_clicked = __find_task_button_and_click_it(browser)
    if not is_button_clicked:
        return

    __switch_to_newly_opened_tab(browser, tasks_tab)
    product_li_elements = __get_list_of_products(browser)

    successful_add_to_cart_count = 0
    for li_element in product_li_elements:
        try:
            # todo: remember the product name and add it to the list so that we can remove it from cart later on
            # also, remember the quantity and if it is greater than 1, then do not remove the product, but subtract qty by 1
            WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.CLASS_NAME, "img")))
            open_link_in_new_tab(browser, li_element.find_element_by_class_name("main").find_element_by_class_name(
                "img").find_element_by_tag_name("a").get_attribute("href"))
            WebDriverWait(browser, 10).until(
                ec.presence_of_element_located((By.XPATH, "/html/body/div[8]/div/div[2]/form/div[5]/div[1]/a[1]")))
            wait()
            browser.find_element_by_xpath("/html/body/div[8]/div/div[2]/form/div[5]/div[1]/a[1]").click()
            wait()
            wait()
            # Click on "Continue shopping" button
            WebDriverWait(browser, 10).until(
                ec.presence_of_element_located((By.XPATH,
                                                "//a[contains(text(), 'Continue Shopping')]/ancestor::div[contains(@class, 'modal_container')]")))
            browser.find_element_by_xpath(
                "//a[contains(text(), 'Continue Shopping')]/ancestor::div[contains(@class, 'modal_container')]").click()
            successful_add_to_cart_count += 1
            close_current_tab(browser)
        except WebDriverException:
            print("Unable to add product to cart")  # todo: specify which product, and use logging instead of print
            traceback.print_exc()
        finally:
            if successful_add_to_cart_count > 2:
                close_current_tab_and_switch_to_window(browser, tasks_tab)
                break


def __find_task_button_and_click_it(browser):
    is_button_clicked = False

    logging.info("Finding the div element containing task description and the \"Complete task\" button")
    task_div = browser.find_element_by_xpath("//li[contains(@class, 'item') and contains(@class, 'browseAddcart')]")

    logging.info("Finding the button inside div element")
    task_button = task_div.find_element_by_class_name("item-btn")

    logging.info("Button text is: {}".format(task_button.text))
    if task_button.text.lower() != "received":
        logging.info("Click the button")
        task_button.click()
        is_button_clicked = True
    else:
        logging.info("Not clicking a button - reward already received")

    return is_button_clicked


def __switch_to_newly_opened_tab(browser, tasks_tab):
    logging.info("Switching to the newly opened tab and confirming it is the right one")
    WebDriverWait(browser, 10).until(ec.new_window_is_opened)
    WebDriverWait(browser, 10).until(ec.number_of_windows_to_be(2))
    all_tabs = browser.window_handles
    new_tab = [tab for tab in all_tabs if tab != tasks_tab][0]
    browser.switch_to.window(new_tab)
    WebDriverWait(browser, 10).until(ec.url_contains("https://www.banggood.com/index.php?com=account&t=vipTaskProduct"))


def __get_list_of_products(browser):
    logging.info("Getting the ul element holding all li elements that represent the products")
    return browser.find_element_by_xpath("//ul[contains(@class, 'goodlist') and contains(@class, 'cf')]") \
        .find_elements_by_tag_name("li")
