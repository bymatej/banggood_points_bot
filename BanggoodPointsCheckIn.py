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

print("x")
from intents.subactions import cleanup_wish_list
from intents.tasks import browse_add_3_products_to_wish_list
task_data = browse_add_3_products_to_wish_list()
# todo: check why some products cannot be found (1 is fine, 2 is not even in the loop and 3 simply retruns no results in search)
task_data.products.append("Xiaomi Ecosystem WEMAX L1668FCF 4K ALPD Ultra Short Throw Laser Projector 9000 ANSI Lumens 250nit 4000:1 Contrast Ratio Support HDR Voice Control Cinema Theater Projector")
task_data.products.append("Artillery® Genius DIY 3D Printer Kit 220*220*250mm Print Size with Ultra-Quiet Stepper Motor TFT Touch Screen Support Filament Runout Detection&Power Failure Function")
task_data.products.append("OnePlus 8 5G Global Rom 6.55 inch FHD+ 90Hz Fluid Display NFC Android10 4300mAh 48MP Triple Rear Camera 12GB 256GB Snapdragon 865 Smartphone")
cleanup_wish_list(browser, task_data)
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
#
# # Log out
# log_out(browser)
# # Close browser
# browser.quit()

logging.info("\n\nThe Bot has finished\n\n")
