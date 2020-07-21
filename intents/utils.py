from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from conf.config import get_sleep_time
from time import sleep


def open_link_in_new_tab(browser, url):
    browser.execute_script("window.open('{}', 'new_window')".format(url))
    WebDriverWait(browser, 10).until(ec.new_window_is_opened)
    browser.switch_to_window(browser.window_handles[get_last_opened_tab_id(browser)])
    WebDriverWait(browser, 10).until(ec.url_contains(url))


def close_current_tab(browser):
    wait()
    browser.close()
    browser.switch_to_window(browser.window_handles[get_last_opened_tab_id(browser)])


def close_current_tab_and_switch_to_window(browser, window_to_switch_to):
    wait()
    browser.close()
    browser.switch_to_window(window_to_switch_to)


def get_last_opened_tab_id(browser):
    return len(browser.window_handles) - 1


def wait():
    sleep(get_sleep_time())
