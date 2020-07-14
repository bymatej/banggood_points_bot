import traceback
from time import sleep

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from conf.config import get_password
from conf.config import get_username
from intents.utils import close_current_tab
from intents.utils import open_link_in_new_tab
from intents.utils import wait


def log_in(browser):
    # Get email input field in login form
    email_login_input_field = browser.find_element_by_xpath("/html/body/div[1]/div/form[1]/ul/li[1]/label/div/input")
    # Get password input field in login form
    password_login_input_field = browser.find_element_by_xpath("/html/body/div[1]/div/form[1]/ul/li[2]/label/div/input")
    # Fill out login details
    email_login_input_field.send_keys(get_username())
    password_login_input_field.send_keys(get_password())
    # Perform login (get the button and click it)
    browser.find_element_by_xpath("/html/body/div[1]/div/form[1]/ul/li[3]/input").click()
    wait()
    # assert "banggood" in browser.title.lower() # todo: fix


def log_out(browser):
    # Sign out
    browser.get("https://www.banggood.com/")
    browser.get("https://www.banggood.com/index.php?com=account&t=logout")


# Perform daily check-in
def perform_check_in(browser):
    check_in_button = browser.find_element_by_xpath("/html/body/div[1]/section[2]/div/div[1]/div/div/button")
    if check_in_button.text.lower() == "check-in":
        check_in_button.click()
        sleep(2)  # The get_sleep_time() method is not used as it always needs ~2 seconds here to view the popup
        # Click on the button on popup to close it
        browser.find_element_by_xpath("/html/body/div[2]/div/div[2]/div/div[3]").click()
        print("Check-in was successful")
    else:
        # Get time left for the next check-in
        next_check_in = browser.find_element_by_class_name("countdown").text
        print(next_check_in)  # Todo: remove the "RESTART-IN" and seconds using regex


# Complete task "Search products and add to cart" and get reward points
def perform_products_search_and_add_to_cart(browser):
    # remember current tab
    tasks_tab = browser.current_window_handle

    # div element containing task description and the "Complete task" button
    task_div = browser.find_element_by_xpath("//li[contains(@class, 'item') and contains(@class, 'browseAddcart')]")
    # find button and click it
    task_button = task_div.find_element_by_class_name("item-btn")
    # Check if reward is already received and terminate if it is
    if task_button.text.lower() == "received":
        return
    else:
        task_button.click()

    # Switch to newly opened tab and confirm it is the right one
    WebDriverWait(browser, 10).until(ec.new_window_is_opened)
    WebDriverWait(browser, 10).until(ec.number_of_windows_to_be(2))  # todo: consider moving from sleep() to this wait
    all_tabs = browser.window_handles
    new_tab = [tab for tab in all_tabs if tab != tasks_tab][0]
    browser.switch_to.window(new_tab)
    WebDriverWait(browser, 10).until(ec.url_contains("https://www.banggood.com/index.php?com=account&t=vipTaskProduct"))

    # get ul element holding all products
    product_li_elements = browser \
        .find_element_by_xpath("//ul[contains(@class, 'goodlist') and contains(@class, 'cf')]") \
        .find_elements_by_tag_name("li")
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
            browser.find_element_by_xpath("/html/body/div[8]/div/div[2]/form/div[5]/div[1]/a[1]").click()
            # Click on "Continue shopping" button
            WebDriverWait(browser, 10).until(
                ec.presence_of_element_located((By.XPATH, "/html/body/div[40]/div[2]/div/div/div[1]/div/div/a[1]")))
            browser.find_element_by_xpath("/html/body/div[40]/div[2]/div/div/div[1]/div/div/a[1]").click()
            successful_add_to_cart_count += 1
            close_current_tab(browser)
        except WebDriverException:
            print("Unable to add product to cart")  # todo: specify which product, and use logging instead of print
            traceback.print_exc()
        finally:
            if successful_add_to_cart_count > 2:
                browser.switch_to.window(tasks_tab)
                break
