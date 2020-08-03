import logging

from selenium.webdriver.firefox import webdriver

from conf import Config
from intents import Utils


class Navigator:

    # Go to banggood login page, wait for 2 seconds to load, confirm that title contains "login"
    @classmethod
    def open_login_page(cls, browser: webdriver.WebDriver):
        logging.info("Opening login page")
        cls._perform_navigation(browser, "https://www.banggood.com/login.html")
        assert "login" in browser.title.lower()

    # Go to points page
    @classmethod
    def open_points_page(cls, browser: webdriver.WebDriver):
        logging.info("Opening my points page")
        cls._set_shipto_info(browser)
        cls._perform_navigation(browser, "https://www.banggood.com/index.php?com=account&t=vipClub")

    # Go to tasks page
    @classmethod
    def open_tasks_page(cls, browser: webdriver.WebDriver):
        logging.info("Opening tasks page")
        cls._perform_navigation(browser,
                                "https://www.banggood.com/index.php?bid=28839&com=account&t=vipTaskList#points")

    @classmethod
    def prepare_tasks_page_for_next_task(cls, browser: webdriver.WebDriver):
        logging.info("Opening tasks page if it is not already open")
        tasks_page_url = "https://www.banggood.com/index.php?bid=28839&com=account&t=vipTaskList#points"
        # Check if you are still on tasks page, and if not - reopen the tasks page
        if tasks_page_url not in browser.current_url:
            logging.info("Task page was not opened")
            cls.open_tasks_page(browser)

    # Opens cart page
    @classmethod
    def open_cart_page(cls, browser: webdriver.WebDriver):
        logging.info("Opening cart page")
        cls._perform_navigation(browser, "https://www.banggood.com/shopping_cart.html")

    # Opens wish list page
    @classmethod
    def open_wish_list_page(cls, browser: webdriver.WebDriver):
        logging.info("Opening wish list page")
        cls._perform_navigation(browser, "https://www.banggood.com/index.php?com=account&t=wishlist")

    @classmethod
    def _set_shipto_info(cls, browser: webdriver.WebDriver):
        # Explicitly switch to desired country and currency
        url_with_shipto_info = "https://www.banggood.com/index.php?com=account&DCC={}&currency={}" \
            .format(Config.get_desired_country(), Config.get_desired_currency())

        logging.info("\n"
                     "\tSetting country: {} \n"
                     "\tSetting currency: {} \n "
                     "\tWill navigate to URL: {}\n"
                     .format(Config.get_desired_country(), Config.get_desired_currency(), url_with_shipto_info))

        cls._perform_navigation(browser, url_with_shipto_info)
        Utils.wait()

    @classmethod
    def _perform_navigation(cls, browser: webdriver.WebDriver, url: str):
        browser.get(url)
        Utils.wait()
