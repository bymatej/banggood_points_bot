"""
Sub-actions required for all tasks to be completed.
Some sub-actions are shared across multiple task, and some are not, but they are separated from their actions to
reduce code complexity.

Example:
Task to add 3 products to cart has similar steps as the one where 3 products need to be added to a wish list.
The only difference is where the product is added.
The difference manifests in clicking a different button/link on Product details page.
This means passing a different XPATH for a button/link to be clicked.
The rest is the same.
"""

import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from common import ProductAlreadyInWishListException
# from intents import Navigator
# from intents import TaskData
# from intents import Utils
import intents.utils


class Subactions:

    @classmethod
    def find_task_button_and_click_it(cls, browser: webdriver.WebDriver, task_data: TaskData):
        logging.info("Finding the div element containing task description and the \"Complete task\" button")
        task_div = browser.find_element_by_xpath(task_data.xpath)

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

    @classmethod
    def switch_to_newly_opened_tab(cls, browser: webdriver.WebDriver, tasks_tab: webdriver.WebDriver):
        logging.info("Switching to the newly opened tab and confirming it is the right one")
        WebDriverWait(browser, 10).until(ec.new_window_is_opened)
        WebDriverWait(browser, 10).until(ec.number_of_windows_to_be(2))
        all_tabs = browser.window_handles
        new_tab = [tab for tab in all_tabs if tab != tasks_tab][0]
        browser.switch_to.window(new_tab)
        WebDriverWait(browser, 10).until(
            ec.url_contains("https://www.banggood.com/index.php?com=account&t=vipTaskProduct"))

    @classmethod
    def get_list_of_products(cls, browser: webdriver.WebDriver):
        logging.info("Getting the ul element holding all li elements that represent the products")
        return browser.find_element_by_xpath("//ul[contains(@class, 'goodlist') and contains(@class, 'cf')]") \
            .find_elements_by_tag_name("li")

    @classmethod
    def add_product_to_cart(cls, browser: webdriver.WebDriver, li_element, task_data: TaskData):
        product_name = cls._open_product_details_page_and_get_product_name(browser, li_element)

        logging.info("Finding the add to cart button")
        add_to_cart_button_xpath = "/html/body/div[8]/div/div[2]/form/div[5]/div[1]/a[1]"
        WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.XPATH, add_to_cart_button_xpath)))
        Utils.wait()
        logging.info("Clicking the add to cart button")
        browser.find_element_by_xpath(add_to_cart_button_xpath).click()
        Utils.wait()

        cls._continue_shopping(browser, task_data, product_name)

    @classmethod
    def add_product_to_wish_list(cls, browser: webdriver.WebDriver, li_element, task_data: TaskData):
        product_name = cls._open_product_details_page_and_get_product_name(browser, li_element)

        logging.info("Finding the add to wish list button")
        add_to_wish_list_button_xpath = "//span[contains(@class, 'wish_text')]" \
                                        "/ancestor::div[contains(@class, 'addToWish')]"

        WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.XPATH, add_to_wish_list_button_xpath)))
        Utils.wait()
        add_to_wish_list_button_element = browser.find_element_by_xpath(add_to_wish_list_button_xpath)
        logging.info("Checking if the product is already in the wish list")
        if "add to wishlist" in add_to_wish_list_button_element.text.lower():
            logging.info("Clicking the add to wish list button")
            add_to_wish_list_button_element.click()
            Utils.wait()
            cls._continue_shopping(browser, task_data, product_name)
        else:
            logging.info("{} is already added to the wish list".format(product_name))
            logging.warning("Raising an exception. This is OK. By raising the exception this product will be skipped")
            raise ProductAlreadyInWishListException(product_name)

    @classmethod
    def cleanup_cart(cls, browser: webdriver.WebDriver, task_data: TaskData):
        Navigator.open_cart_page(browser)

        product_row_xpath = "//div[contains(@class, 'newcart_main')]//ul[contains(@class, 'newcart_list_items')]"
        product_link_xpath = "//li[contains(@class, 'newcart_product')]//a[contains(@class, 'title')]"
        product_quantity_xpath = "//li[contains(@class, 'newcart_quantity')]//div[contains(@class, 'quantity_item')]"
        product_quantity_minus_xpath = "//a[contains(text(), '-')]"
        product_options_xpath = "//li[contains(@class, 'newcart_options')]"
        product_remove_button_xpath = f"{product_options_xpath}//span[contains(@data-title, 'Remove')]"
        product_remove_modal_xpath = f"{product_options_xpath}//div[contains(@class, 'item_remove_mask')]"
        product_remove_modal_yes_button_xpath = "//a[contains(@class, 'item_mask_yes')]"

        logging.info("Finding products added from the task in the list of products in cart")
        for product_row in browser.find_elements_by_xpath(product_row_xpath):
            product = product_row.find_element_by_xpath(product_link_xpath).text
            if product in task_data.products:
                logging.info(f"Product found! It's {product}")
                qty_element = product_row.find_element_by_xpath(product_quantity_xpath)
                quantity = int(qty_element.find_element_by_tag_name("input").get_attribute("value"))
                if quantity > 1:
                    logging.info(f"Decreasing qty for product {product} from {quantity} to {quantity - 1}")
                    qty_element.find_element_by_xpath(product_quantity_minus_xpath).click()
                    Utils.wait()
                else:
                    logging.info(f"Removing product {product} from cart.")
                    product_row.find_element_by_xpath(product_remove_button_xpath).click()
                    Utils.wait()
                    product_row.find_element_by_xpath(product_remove_modal_xpath) \
                        .find_element_by_xpath(product_remove_modal_yes_button_xpath) \
                        .click()
                    Utils.wait()
            logging.info(f"Done with product {product}. Moving on...")

    @classmethod
    def cleanup_wish_list(cls, browser: webdriver.WebDriver, task_data: TaskData):
        Navigator.open_wish_list_page(browser)

    @classmethod
    def _open_product_details_page_and_get_product_name(cls, browser: webdriver.WebDriver, li_element):
        logging.info("Finding the link and opening the product details page from the list of products")
        WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.CLASS_NAME, "img")))
        product_main_div_element = li_element.find_element_by_class_name("main")

        product_name = product_main_div_element \
            .find_element_by_class_name("title") \
            .find_element_by_tag_name("a") \
            .text

        logging.info("Opening product details page in new tab")
        Utils.open_link_in_new_tab(browser, product_main_div_element
                                   .find_element_by_class_name("img")
                                   .find_element_by_tag_name("a")
                                   .get_attribute("href"))

        return product_name

    @classmethod
    def _continue_shopping(cls, browser: webdriver.WebDriver, task_data: TaskData, product_name: str):
        Utils.wait()  # Wait a little longer to ensure the product is added and popup is presented

        logging.info("Clicking on \"Continue Shopping\" button")
        continue_shopping_button_xpath = "//div[contains(@class, 'modal_container')] " \
                                         "//a[(contains(translate(text(), " \
                                         "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), " \
                                         "'continue shopping'))]"
        WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.XPATH, continue_shopping_button_xpath)))
        browser.find_element_by_xpath(continue_shopping_button_xpath).click()
        Utils.wait()

        logging.info("Adding product {} to list and closing the Product Details Page".format(product_name))
        task_data.products.append(product_name)

        if len(task_data.products) >= 3:
            cls._receive_reward(browser, task_data)

        Utils.close_current_tab(browser)

    @classmethod
    def _receive_reward(cls, browser: webdriver.WebDriver, task_data: TaskData):
        Utils.wait()

        logging.info("Clicking on \"Receive it\" button")
        receive_it_button_xpath = f"//div[contains(@class, '{task_data.modal_css_class}')] " \
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
