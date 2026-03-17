from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://google.com")

# search for elements in the html
# heres how to find the search element of the google page, click on it and search something.

# we can use the ID, classname, tag name
# we are going to use classname of the search tab
input_element = driver.find_element(By.CLASS_NAME, "gLFyf")
input_element.send_keys("coinmarketcap" + Keys.ENTER)

time.sleep(10)

driver.quit()

