from selenium import webdriver

from actions.Actions import *
from actions.Navigator import *

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
