from time import sleep

from conf.config import get_sleep_time


# Go to banggood login page, wait for 2 seconds to load, confirm that title contains "login"
def open_login_page(browser):
    browser.get("https://www.banggood.com/login.html")
    sleep(get_sleep_time())
    assert "login" in browser.title.lower()


# Go to points page
def open_points_page(browser):
    browser.get("https://www.banggood.com/index.php?com=account&t=vipClub")
    sleep(get_sleep_time())
