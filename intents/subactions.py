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
    logging.info("Finding the link and opening the product details page from the list of products")
    WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.CLASS_NAME, "img")))
    product_main_div_element = li_element.find_element_by_class_name("main")
    product_name = product_main_div_element \
        .find_element_by_class_name("title") \
        .find_element_by_tag_name("a") \
        .text
    open_link_in_new_tab(browser, product_main_div_element
                         .find_element_by_class_name("img")
                         .find_element_by_tag_name("a")
                         .get_attribute("href"))

    logging.info("Finding the add to cart button")
    add_to_cart_button_xpath = "/html/body/div[8]/div/div[2]/form/div[5]/div[1]/a[1]"
    WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.XPATH, add_to_cart_button_xpath)))
    wait()
    logging.info("Clicking the add to cart button")
    browser.find_element_by_xpath(add_to_cart_button_xpath).click()
    wait()
    wait()  # Wait a little longer to ensure the product is added to cart

    logging.info("Clicking on \"Continue Shopping\" button")
    continue_shopping_button_xpath = "//a[contains(text(), 'Continue Shopping')]" \
                                     "/ancestor::div[contains(@class, 'modal_container')]"
    WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.XPATH, continue_shopping_button_xpath)))
    browser.find_element_by_xpath(continue_shopping_button_xpath).click()

    logging.info("Adding product {} to list and closing the Product Details Page".format(product_name))
    task_data.products.append(product_name)
    close_current_tab(browser)
