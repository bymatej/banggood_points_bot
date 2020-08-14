"""
Navigator represents the intents to navigate to a certain URL.
As if the human user would copy/paste the URL into the address bar, the bot does the similar thing.
In most cases, the bot calls the browser.get(url) from the _perform_navigation function.
"""

import logging

from selenium.webdriver.firefox import webdriver

from conf.config import get_desired_country
from conf.config import get_desired_currency
from intents.utils import wait


# Go to banggood login page, wait for 2 seconds to load, confirm that title contains "login"
def open_login_page(browser: webdriver.WebDriver):
    logging.info("Opening login page")
    _perform_navigation(browser, "https://www.banggood.com/login.html")
    assert "login" in browser.title.lower()


# Go to points page
def open_points_page(browser: webdriver.WebDriver):
    logging.info("Opening my points page")
    _set_shipto_info(browser)
    _perform_navigation(browser, "https://www.banggood.com/index.php?com=account&t=vipClub")


# Go to tasks page
def open_tasks_page(browser: webdriver.WebDriver):
    logging.info("Opening tasks page")
    _perform_navigation(browser, "https://www.banggood.com/index.php?bid=28839&com=account&t=vipTaskList#points")


def prepare_tasks_page_for_next_task(browser: webdriver.WebDriver):
    logging.info("Opening tasks page if it is not already open")
    tasks_page_url = "https://www.banggood.com/index.php?bid=28839&com=account&t=vipTaskList#points"
    # Check if you are still on tasks page, and if not - reopen the tasks page
    if tasks_page_url not in browser.current_url:
        logging.info("Task page was not opened")
        open_tasks_page(browser)


# Opens cart page
def open_cart_page(browser: webdriver.WebDriver):
    logging.info("Opening cart page")
    _perform_navigation(browser, "https://www.banggood.com/shopping_cart.html")


# Opens wish list page
def open_wish_list_page(browser: webdriver.WebDriver):
    logging.info("Opening wish list page")
    _perform_navigation(browser, "https://www.banggood.com/index.php?com=account&t=wishlist")


def _set_shipto_info(browser: webdriver.WebDriver):
    # Explicitly switch to desired country and currency
    url_with_shipto_info = "https://www.banggood.com/index.php?com=account&DCC={}&currency={}" \
        .format(get_desired_country(), get_desired_currency())

    logging.info("\n"
                 "\tSetting country: {} \n"
                 "\tSetting currency: {} \n "
                 "\tWill navigate to URL: {}\n"
                 .format(get_desired_country(), get_desired_currency(), url_with_shipto_info))

    _perform_navigation(browser, url_with_shipto_info)
    wait()


def _perform_navigation(browser: webdriver.WebDriver, url: str):
    browser.get(url)
    wait()
