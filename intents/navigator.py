import logging

from conf.config import get_desired_country
from conf.config import get_desired_currency
from intents.utils import wait


def __perform_navigation(browser, url):
    browser.get(url)
    wait()


# Go to banggood login page, wait for 2 seconds to load, confirm that title contains "login"
def open_login_page(browser):
    logging.info("Opening login page")
    __perform_navigation(browser, "https://www.banggood.com/login.html")
    assert "login" in browser.title.lower()


# Go to points page
def open_points_page(browser):
    logging.info("Opening my points page")
    __set_shipto_info(browser)
    __perform_navigation(browser, "https://www.banggood.com/index.php?com=account&t=vipClub")


# Go to tasks page
def open_tasks_page(browser):
    logging.info("Opening tasks page")
    __perform_navigation(browser, "https://www.banggood.com/index.php?bid=28839&com=account&t=vipTaskList#points")


def prepare_tasks_page_for_next_task(browser):
    logging.info("Opening tasks page if it is not already open")
    tasks_page_url = "https://www.banggood.com/index.php?bid=28839&com=account&t=vipTaskList#points"
    # Check if you are still on tasks page, and if not - reopen the tasks page
    if tasks_page_url not in browser.current_url:
        logging.info("Task page was not opened")
        open_tasks_page(browser)


# Opens cart page
def open_cart_page(browser):
    logging.info("Opening cart page")
    __perform_navigation(browser, "https://www.banggood.com/shopping_cart.html")


# Opens wish list page
def open_wish_list_page(browser):
    logging.info("Opening wish list page")
    __perform_navigation(browser, "https://www.banggood.com/index.php?com=account&t=wishlist")


def __set_shipto_info(browser):
    # Explicitly switch to desired country and currency
    url_with_shipto_info = "https://www.banggood.com/index.php?com=account&DCC={}&currency={}" \
        .format(get_desired_country(), get_desired_currency())

    logging.info("\n"
                 "\tSetting country: {} \n"
                 "\tSetting currency: {} \n "
                 "\tWill navigate to URL: {}\n"
                 .format(get_desired_country(), get_desired_currency(), url_with_shipto_info))

    __perform_navigation(browser, url_with_shipto_info)
    wait()
