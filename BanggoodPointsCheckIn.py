import logging

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from intents.actions import log_in
from intents.actions import log_out
from intents.actions import perform_browse_and_add_to_cart
from intents.actions import perform_browse_and_add_to_wish_list
from intents.actions import perform_check_in
from intents.actions import perform_search_and_add_to_cart
from intents.navigator import open_login_page
from intents.navigator import open_points_page
from intents.navigator import open_tasks_page
from intents.navigator import prepare_tasks_page_for_next_task

logging.info("\n\nThe Bot has started\n\n")

# Open Firefox browser
options = Options()
options.headless = False  # todo: change to True when everything is finished
browser = webdriver.Firefox(options=options)
browser.implicitly_wait(10)  # wait 10 seconds for all DOM elements
# Open log-in page
open_login_page(browser)
# Log in
log_in(browser)

from intents.subactions import cleanup_cart
from intents.task.task_type import browse_add_3_products_to_cart
td = browse_add_3_products_to_cart()
td.products.append("Xiaomi FIMI X8 SE 2020 8KM FPV With 3-axis Gimbal 4K Camera HDR Video GPS 35mins Flight Time RC Quadcopter RTF One Battery Version")
td.products.append("LANGFEITE L8S 2019 Version 20.8Ah 48.1V 800W*2 Dual Motor Folding Electric Scooter Color Display DC Brushless Motor 45km/h Top Speed 55km Range EU Plug")
td.products.append("Xiaomi Redmi Note 8 Pro Global Version 6.53 inch 64MP Quad Rear Camera 6GB 64GB NFC 4500mAh Helio G90T Octa Core 4G Smartphone")
cleanup_cart(browser, td)
print("x")

# # Open points page
# open_points_page(browser)
# # Perform check-in
# perform_check_in(browser)
#
# # Open tasks page
# open_tasks_page(browser)
# # Perform tasks
# perform_browse_and_add_to_cart(browser)
# prepare_tasks_page_for_next_task(browser)
# perform_browse_and_add_to_wish_list(browser)
# prepare_tasks_page_for_next_task(browser)
# perform_search_and_add_to_cart(browser)

# # Log out
# log_out(browser)
# # Close browser
# browser.quit()

logging.info("\n\nThe Bot has finished\n\n")
