from time import sleep

from selenium import webdriver

# Open Firefox browser, go to banggood login page, wait for 2 seconds to load, confirm that title contains "login"
browser = webdriver.Firefox()
browser.get("https://www.banggood.com/login.html")
sleep(2)
assert "Login" in browser.title

# Get email input field in login form
email_login_input_field = browser.find_element_by_xpath("/html/body/div[1]/div/form[1]/ul/li[1]/label/div/input")
# Get password input field in login form
password_login_input_field = browser.find_element_by_xpath("/html/body/div[1]/div/form[1]/ul/li[2]/label/div/input")
# Fill out login details
email_login_input_field.send_keys("detilab611@wonwwf.com")  # todo: Move this to property file
password_login_input_field.send_keys("StrongPass$0")  # todo: move this to property file
# Perform login (get the button and click it)
browser.find_element_by_xpath("/html/body/div[1]/div/form[1]/ul/li[3]/input").click()
sleep(2)
# assert "Banggood" in browser.title #  todo: Fix this
#  - the browser contains the word Banggood in the title, but it is not the first word, so assertion fails

# Go to points page
browser.get("https://www.banggood.com/index.php?com=account&t=vipClub")
sleep(2)
# Perform daily check-in
check_in_button = browser.find_element_by_xpath("/html/body/div[1]/section[2]/div/div[1]/div/div/button")
if check_in_button.text.lower() == "check-in":
    check_in_button.click()
    # Click on X icon on popup to close it
    browser.find_element_by_xpath("/html/body/div[2]/div/div[2]/i").click()
    # Sign out
    browser.get("https://www.banggood.com/")
    browser.get("https://www.banggood.com/index.php?com=account&t=logout")
    print("Check-in was successful")
else:
    # Get time left for the next check-in
    next_check_in = browser.find_element_by_class_name("countdown").text
    print(next_check_in)  # Todo: remove the "RESTART-IN" and seconds using regex
    # Sign out
    browser.get("https://www.banggood.com/")
    browser.get("https://www.banggood.com/index.php?com=account&t=logout")
