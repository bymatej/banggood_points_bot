"""
Sub-actions required for all tasks to be completed.
Some sub-actions are subactions for multiple task.

Example:
Task to add 3 products to cart has similar steps as the one where 3 products need to be added to a wish list.
The only difference is where the product is added.
The difference manifests in clicking a different button/link on Product details page.
This means passing a different XPATH for a button/link to be clicked.
The rest is the same.
"""

import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from common.exceptions import ProductAlreadyInWishListException
from intents.utils import close_current_tab
from intents.utils import open_link_in_new_tab
from intents.utils import wait


def find_task_button_and_click_it(browser, task_data):
    logging.info("Finding the div element containing task description and the \"Complete task\" button")
    task_div = browser.find_element_by_xpath(task_data.task_type.value)

    logging.info("Finding the button inside div element")
    task_button = task_div.find_element_by_class_name("item-btn")

    logging.info("Button text is: {}".format(task_button.text))
    if task_button.text.lower() == "received" or task_button.text.lower() == 'claim reward':
        logging.info("Reward already received")
        is_reward_received = True
    else:
        logging.info("Reward not yet received")
        is_reward_received = False

    logging.info("Click the button")
    task_button.click()
    return is_reward_received


def switch_to_newly_opened_tab(browser, tasks_tab):
    logging.info("Switching to the newly opened tab and confirming it is the right one")
    WebDriverWait(browser, 10).until(ec.new_window_is_opened)
    WebDriverWait(browser, 10).until(ec.number_of_windows_to_be(2))
    all_tabs = browser.window_handles
    new_tab = [tab for tab in all_tabs if tab != tasks_tab][0]
    browser.switch_to.window(new_tab)
    WebDriverWait(browser, 10).until(ec.url_contains("https://www.banggood.com/index.php?com=account&t=vipTaskProduct"))


def get_list_of_products(browser):
    logging.info("Getting the ul element holding all li elements that represent the products")
    return browser.find_element_by_xpath("//ul[contains(@class, 'goodlist') and contains(@class, 'cf')]") \
        .find_elements_by_tag_name("li")


def add_product_to_cart(browser, li_element, task_data):
    product_name = __open_product_details_page_and_get_product_name(browser, li_element)

    logging.info("Finding the add to cart button")
    add_to_cart_button_xpath = "/html/body/div[8]/div/div[2]/form/div[5]/div[1]/a[1]"
    WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.XPATH, add_to_cart_button_xpath)))
    wait()
    logging.info("Clicking the add to cart button")
    browser.find_element_by_xpath(add_to_cart_button_xpath).click()
    wait()

    __continue_shopping(browser, task_data, product_name)


def add_product_to_wish_list(browser, li_element, task_data):
    product_name = __open_product_details_page_and_get_product_name(browser, li_element)

    logging.info("Finding the add to wish list button")
    add_to_wish_list_button_xpath = "//span[contains(@class, 'wish_text')]" \
                                    "/ancestor::div[contains(@class, 'addToWish')]"

    WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.XPATH, add_to_wish_list_button_xpath)))
    wait()
    add_to_wish_list_button_element = browser.find_element_by_xpath(add_to_wish_list_button_xpath)
    logging.info("Checking if the product is already in the wish list")
    if "add to wishlist" in add_to_wish_list_button_element.text.lower():
        logging.info("Clicking the add to wish list button")
        add_to_wish_list_button_element.click()
        wait()
        __continue_shopping(browser, task_data, product_name)
    else:
        logging.info("{} is already added to the wish list".format(product_name))
        logging.warning("Raising an exception. This is OK. By raising the exception this product will be skipped")
        raise ProductAlreadyInWishListException(product_name)


def __open_product_details_page_and_get_product_name(browser, li_element):
    logging.info("Finding the link and opening the product details page from the list of products")
    WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.CLASS_NAME, "img")))
    product_main_div_element = li_element.find_element_by_class_name("main")

    product_name = product_main_div_element \
        .find_element_by_class_name("title") \
        .find_element_by_tag_name("a") \
        .text

    logging.info("Opening product details page in new tab")
    open_link_in_new_tab(browser, product_main_div_element
                         .find_element_by_class_name("img")
                         .find_element_by_tag_name("a")
                         .get_attribute("href"))

    return product_name


def __continue_shopping(browser, task_data, product_name):
    wait()  # Wait a little longer to ensure the product is added and popup is presented

    logging.info("Clicking on \"Continue Shopping\" button")
    continue_shopping_button_xpath = "//div[contains(@class, 'modal_container')] " \
                                     "//a[(contains(translate(text(), " \
                                     "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), " \
                                     "'continue shopping'))]"
    WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.XPATH, continue_shopping_button_xpath)))
    browser.find_element_by_xpath(continue_shopping_button_xpath).click()
    wait()

    logging.info("Adding product {} to list and closing the Product Details Page".format(product_name))
    task_data.products.append(product_name)

    if len(task_data.products) >= 3:
        __receive_reward(browser)

    close_current_tab(browser)


def __receive_reward(browser):
    wait()

    logging.info("Clicking on \"Receive it\" button")
    receive_it_button_xpath = "//div[contains(@class, 'modal')] " \
                              "//a[(contains(" \
                              "translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), " \
                              "'receive it'))]"
    WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.XPATH, receive_it_button_xpath)))
    receive_it_button_element = browser.find_element_by_xpath(receive_it_button_xpath)
    if receive_it_button_element.is_displayed():
        receive_it_button_element.click()
        logging.info("Receiving points for completing the task")
    else:
        logging.info("The \"Receive it\" button is not displayed. Not clicking on anything...")
