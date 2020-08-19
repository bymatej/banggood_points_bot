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
import traceback

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from common.exceptions import ProductAlreadyInWishListException
from intents.navigator import open_cart_page
from intents.navigator import open_wish_list_page
from intents.tasks import TaskData
from intents.utils import close_current_tab
from intents.utils import open_link_in_new_tab
from intents.utils import scroll_to_and_hover_over_element
from intents.utils import wait


def find_task_button_and_click_it(browser: webdriver.WebDriver, task_data: TaskData):
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


def switch_to_newly_opened_tab(browser: webdriver.WebDriver, tasks_tab: webdriver.WebDriver):
    logging.info("Switching to the newly opened tab and confirming it is the right one")
    WebDriverWait(browser, 10).until(ec.new_window_is_opened)
    WebDriverWait(browser, 10).until(ec.number_of_windows_to_be(2))
    all_tabs = browser.window_handles
    new_tab = [tab for tab in all_tabs if tab != tasks_tab][0]
    browser.switch_to.window(new_tab)
    WebDriverWait(browser, 10).until(ec.url_contains("https://www.banggood.com/index.php?com=account&t=vipTaskProduct"))


def get_list_of_products(browser: webdriver.WebDriver):
    logging.info("Getting the ul element holding all li elements that represent the products")
    return browser.find_element_by_xpath("//ul[contains(@class, 'goodlist') and contains(@class, 'cf')]") \
        .find_elements_by_tag_name("li")


def add_product_to_cart(browser: webdriver.WebDriver, li_element, task_data: TaskData):
    product_name = _open_product_details_page_and_get_product_name(browser, li_element)

    logging.info("Finding the add to cart button")
    add_to_cart_button_xpath = "/html/body/div[8]/div/div[2]/form/div[5]/div[1]/a[1]"
    WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.XPATH, add_to_cart_button_xpath)))
    wait()
    logging.info("Clicking the add to cart button")
    browser.find_element_by_xpath(add_to_cart_button_xpath).click()
    wait()

    _continue_shopping(browser, task_data, product_name)


def add_product_to_wish_list(browser: webdriver.WebDriver, li_element, task_data: TaskData):
    product_name = _open_product_details_page_and_get_product_name(browser, li_element)

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
        _continue_shopping(browser, task_data, product_name)
    else:
        logging.info("{} is already added to the wish list".format(product_name))
        logging.warning("Raising an exception. This is OK. By raising the exception this product will be skipped")
        raise ProductAlreadyInWishListException(product_name)


def cleanup_cart(browser: webdriver.WebDriver, task_data: TaskData):
    open_cart_page(browser)

    product_row_xpath = "//div[contains(@class, 'newcart_box')]" \
                        "//div[contains(@class, 'newcart_main')]" \
                        "//ul[contains(@class, 'newcart_list_items')]"
    product_link_xpath = ".//li[contains(@class, 'newcart_product')]//a[contains(@class, 'title')]"

    products_in_cart = list(map(lambda p: p.find_element_by_xpath(product_link_xpath).text,
                                browser.find_elements_by_xpath(product_row_xpath)))

    logging.info("Finding products added from the task in the list of products in cart")
    while task_data.products and set(task_data.products).intersection(products_in_cart):
        logging.info("List of added products and list of products in cart intersect.")
        for product in task_data.products:
            logging.info(f"Working with product {product}.")

            try:
                _remove_one_product_from_cart(browser, task_data, product_row_xpath, product)
                logging.info(f"Done with product {product}. Moving on...")
                break
            except NoSuchElementException:
                logging.error(f"Product {product} was not found in cart and was probably already deleted. Moving on...")
                logging.error(traceback.format_exc())
                task_data.products.remove(product)
                break

        browser.refresh()
        products_in_cart = list(map(lambda p: p.find_element_by_xpath(product_link_xpath).text,
                                    browser.find_elements_by_xpath(product_row_xpath)))


def cleanup_wish_list(browser: webdriver.WebDriver, task_data: TaskData):
    open_wish_list_page(browser)

    for product in task_data.products:
        logging.info(f"Working with product {product}")
        search_input_field_element = _search_for_product_in_wish_list_and_get_input_field_element(browser, product)

        try:
            _remove_one_product_from_wish_list(browser, product)
        except NoSuchElementException:
            logging.error(f"Product {product} not found in wish list. It was probably already deleted. Moving on...")
            logging.error(traceback.format_exc())
        finally:
            task_data.products.remove(product)
            logging.info("Clearing text in input field")
            search_input_field_element.clear()
            wait()


def _open_product_details_page_and_get_product_name(browser: webdriver.WebDriver, li_element):
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


def _continue_shopping(browser: webdriver.WebDriver, task_data: TaskData, product_name: str):
    wait()  # Wait a little longer to ensure the product is added and popup is presented

    logging.info("Clicking on \"Continue Shopping\" button")
    continue_shopping_button_xpath = "//div[contains(@class, 'modal_container')] " \
                                     "//a[(contains(translate(text(), " \
                                     "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), " \
                                     "'continue shopping'))]"
    wait()  # Wait a little longer to ensure the popup is presented
    WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.XPATH, continue_shopping_button_xpath)))
    WebDriverWait(browser, 10).until(ec.element_to_be_clickable((By.XPATH, continue_shopping_button_xpath)))
    browser.find_element_by_xpath(continue_shopping_button_xpath).click()
    wait()

    logging.info("Adding product {} to list and closing the Product Details Page".format(product_name))
    task_data.products.append(product_name)

    if len(task_data.products) >= 3:
        _receive_reward(browser, task_data)

    close_current_tab(browser)


def _receive_reward(browser: webdriver.WebDriver, task_data: TaskData):
    wait()

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


def _remove_one_product_from_cart(browser: webdriver.WebDriver, task_data: TaskData, product_row_xpath: str,
                                  product: str):
    product_quantity_xpath = ".//li[contains(@class, 'newcart_quantity')]//div[contains(@class, 'quantity_item')]"
    product_quantity_minus_xpath = ".//a[contains(text(), '-')]"
    product_options_xpath = ".//li[contains(@class, 'newcart_options')]"
    product_remove_button_xpath = f"{product_options_xpath}//span[contains(@data-title, 'Remove')]"
    product_remove_modal_xpath = f"{product_options_xpath}//div[contains(@class, 'item_remove_mask')]"
    product_remove_modal_yes_button_xpath = ".//a[contains(@class, 'item_mask_yes')]"
    target_product_link_xpath = f"{product_row_xpath}//li[contains(@class, 'newcart_product')]" \
                                f"//a[contains(@class, 'title') and contains(text(), '{product}')]"
    target_product_link_element = browser.find_element_by_xpath(target_product_link_xpath)
    product_row_ancestor_xpath = ".//ancestor::ul[contains(@class, 'newcart_list_items')]"
    product_row_element = target_product_link_element.find_element_by_xpath(product_row_ancestor_xpath)

    scroll_to_and_hover_over_element(browser, product_row_element)

    if product in task_data.products:
        logging.info(f"Product found! It's {product}")
        qty_element = product_row_element.find_element_by_xpath(product_quantity_xpath)
        quantity = int(qty_element.find_element_by_tag_name("input").get_attribute("value"))
        if quantity > 1:
            logging.info(f"Decreasing qty for product {product} from {quantity} to {quantity - 1}")
            qty_element.find_element_by_xpath(product_quantity_minus_xpath).click()
            wait()
        else:
            logging.info(f"Removing product {product} from cart.")
            WebDriverWait(browser, 10). \
                until(ec.presence_of_element_located((By.XPATH, product_remove_button_xpath)))
            WebDriverWait(browser, 10). \
                until(ec.element_to_be_clickable((By.XPATH, product_remove_button_xpath)))
            product_row_element.find_element_by_xpath(product_remove_button_xpath).click()
            wait()
            product_row_element.find_element_by_xpath(product_remove_modal_xpath) \
                .find_element_by_xpath(product_remove_modal_yes_button_xpath) \
                .click()
            wait()
        task_data.products.remove(product)


def _search_for_product_in_wish_list_and_get_input_field_element(browser: webdriver.WebDriver,
                                                                 product: str) -> WebElement:
    logging.info("Finding the search button and clicking on it.")

    if "+" in product:
        logging.info("Invalid character '+' detected.")
        product = product.split("+")[0]
        logging.warning(f"Using {product} in the search. Potentially the wrong product can be returned...")
        logging.info(f"This hack was necessary as Banggood search on wish lists does not allow '+' character")

    search_component_xpath = "//li[contains(@class, 'wishlist-nav-search')]"
    search_span_xpath = f"{search_component_xpath}//span[contains(@class, 'search-inner')]"
    search_button_xpath = f"{search_span_xpath}" \
                          f"//span[contains(@class, 'icon-search_new') and contains(@class, 'search-btn')]"
    search_input_field_xpath = f"{search_span_xpath}//input[contains(@class, 'search-text')]"

    logging.info("Clicking on a search button to activate the input field")
    WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.XPATH, search_button_xpath)))
    WebDriverWait(browser, 10).until(ec.element_to_be_clickable((By.XPATH, search_button_xpath)))
    search_button_element = browser.find_element_by_xpath(search_button_xpath)
    scroll_to_and_hover_over_element(search_button_element)
    search_button_element.click()

    logging.info("Filling out the input field")
    WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.XPATH, search_input_field_xpath)))
    WebDriverWait(browser, 10).until(ec.element_to_be_clickable((By.XPATH, search_input_field_xpath)))
    search_input_field_element = browser.find_element_by_xpath(search_input_field_xpath)
    search_input_field_element.send_keys(product)

    logging.info("Clicking on a search button again to perform the search")
    browser.find_element_by_xpath(search_button_xpath).click()
    wait()

    return search_input_field_element


def _remove_one_product_from_wish_list(browser: webdriver.WebDriver, product: str):
    delete_core_xpath = "//div[contains(@class, 'wishlist-product')]" \
                        "//div[contains(@class, 'product-cnt')]" \
                        "//ul[contains(@class, 'product-list') and contains(@class, 'cf')]"
    delete_button_xpath = f"{delete_core_xpath}" \
                          f"//span[contains(@class, 'options')]//span[contains(@class, 'options-remove')]//i"
    delete_popup_yes_xpath = f"{delete_core_xpath}" \
                             f"//span[contains(@class, 'remove-pop')]//p[contains(@class, 'p-btn')]" \
                             f"//span[contains(@class, 'p-btn-yes')]"

    product_element = browser.find_element_by_xpath(f"{delete_core_xpath}//li")
    scroll_to_and_hover_over_element(browser, product_element)

    logging.info("Clicking on delete button")
    WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.XPATH, delete_button_xpath)))
    WebDriverWait(browser, 10).until(ec.element_to_be_clickable((By.XPATH, delete_button_xpath)))
    browser.find_element_by_xpath(delete_button_xpath).click()
    wait()

    logging.info("Confirming deletion")
    WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.XPATH, delete_popup_yes_xpath)))
    WebDriverWait(browser, 10).until(ec.element_to_be_clickable((By.XPATH, delete_popup_yes_xpath)))
    browser.find_element_by_xpath(delete_popup_yes_xpath).click()
    wait()

    logging.info(f"Product {product} deleted successfully from the wish list")
