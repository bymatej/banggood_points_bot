from selenium import webdriver

from intents.actions import log_in
from intents.actions import log_out
from intents.actions import perform_check_in
from intents.actions import perform_products_search_and_add_to_cart
from intents.navigator import open_login_page
from intents.navigator import open_points_page
from intents.navigator import open_tasks_page

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

# Open tasks page
open_tasks_page(browser)
# Perform tasks
perform_products_search_and_add_to_cart(browser)

# Log out
log_out(browser)
# Close browser
browser.close()
