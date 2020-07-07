from time import sleep

from conf.config import get_password
from conf.config import get_sleep_time
from conf.config import get_username


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
    sleep(get_sleep_time())
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
        # Click on X icon on popup to close it
        browser.find_element_by_xpath("/html/body/div[2]/div/div[2]/div/div[3]").click()
        print("Check-in was successful")
    else:
        # Get time left for the next check-in
        next_check_in = browser.find_element_by_class_name("countdown").text
        print(next_check_in)  # Todo: remove the "RESTART-IN" and seconds using regex


# Complete task "Search products and add to cart" and get reward points
def perform_products_search_and_add_to_cart(browser):
    # div element containing task description and the "Complete task" button
    task_div = browser.find_element_by_xpath("//li[contains(@class, 'item') and contains(@class, 'browseAddcart')]")
    # find button and click it
    task_div.find_element_by_class_name("item-btn").click()
    # todo: code below produces error - fix it
    # Switch to newly opened tab
    browser.switch_to.window(browser.window_handles[1])
    # get ul element holding all products
    product_list_ul_element = browser.find_element_by_xpath("//ul[contains(@class, 'goodlist') and contains(@class, 'cf')]")
    product_li_elements = product_list_ul_element.find_element("li")
    print(product_li_elements)
