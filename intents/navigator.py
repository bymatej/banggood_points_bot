from time import sleep

from conf.config import get_sleep_time


def __perform_navigation(browser, url):
    browser.get(url)
    sleep(get_sleep_time())


# Go to banggood login page, wait for 2 seconds to load, confirm that title contains "login"
def open_login_page(browser):
    __perform_navigation(browser, "https://www.banggood.com/login.html")
    assert "login" in browser.title.lower()


# Go to points page
def open_points_page(browser):
    __perform_navigation(browser, "https://www.banggood.com/index.php?com=account&t=vipClub")


# Go to tasks page
def open_tasks_page(browser):
    __perform_navigation(browser, "https://www.banggood.com/index.php?bid=28839&com=account&t=vipTaskList#points")
