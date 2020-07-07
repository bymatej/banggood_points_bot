from selenium import webdriver

from intents.actions import log_in
from intents.actions import log_out
from intents.actions import perform_check_in
from intents.navigator import open_login_page
from intents.navigator import open_points_page

# Open Firefox browser
browser = webdriver.Firefox()
# Open log-in page
open_login_page(browser)
# Log in
log_in(browser)
# Open points page
open_points_page(browser)
# Perform check-in
perform_check_in(browser)
# Log out
log_out(browser)
# Close browser
browser.close()
