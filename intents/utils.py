import logging
from time import sleep

from selenium.webdriver.firefox import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from conf.config import get_sleep_time


def open_link_in_new_tab(browser: webdriver.WebDriver, url: str):
    logging.info("Opening the new tab with the url {}".format(url))
    browser.execute_script("window.open('{}', 'new_window')".format(url))

    logging.info("Waiting for the tab to be opened")
    WebDriverWait(browser, 10).until(ec.new_window_is_opened)

    logging.info("Switching to newly opened tab")
    browser.switch_to_window(browser.window_handles[get_last_opened_tab_id(browser)])
    WebDriverWait(browser, 10).until(ec.url_contains(url))


def close_current_tab(browser: webdriver.WebDriver):
    logging.info("Closing current tab")
    close_current_tab_and_switch_to_window(browser, None)


def close_current_tab_and_switch_to_window(browser: webdriver.WebDriver,
                                           window_to_switch_to: webdriver.WebDriver = None):
    logging.info("Closing current tab")
    wait()
    browser.close()
    logging.info("Switching to previously opened tab")
    if window_to_switch_to is None:
        browser.switch_to.window(browser.window_handles[get_last_opened_tab_id(browser)])
    else:
        browser.switch_to.window(window_to_switch_to)


def get_current_tab(browser: webdriver.WebDriver):
    logging.info("Getting currently opened tab")
    return browser.current_window_handle


def get_last_opened_tab_id(browser: webdriver.WebDriver):
    return len(browser.window_handles) - 1


def wait():
    seconds_to_sleep = get_sleep_time()
    logging.info("Waiting for {} seconds".format(seconds_to_sleep))
    sleep(seconds_to_sleep)
