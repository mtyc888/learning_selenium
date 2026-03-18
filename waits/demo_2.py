from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchAttributeException,
    StaleElementReferenceException,
    ElementClickInterceptedException
)

def get_driver(headless=False):
    options = Options()
    if headless:
        options.add_argument('--headless=new')
    options.add_argument('--incognito')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(
        options=options,
        service=Service(executable_path='../chromedriver.exe')
    )
    return driver

"""
    Explicit waits,

    Pattern: WebDriverWait(driver, timeout).until(condition)
    polls the DOM every 0.5 seconds until the condition is met or timeout
"""
def explicit_wait():
    driver = get_driver()
    driver.get("https://quotes.toscrape.com/js/")

    # this will make the driver wait 10 seconds for elements to appear
    wait = WebDriverWait(driver, 10)

    """
        Main 5 Expected Conditions (EC)

        EC.presence_of_element_located() => wait until element exists in DOM
        EC.visibility_of_element_located() => wait until element is visible on page
        EC.element_to_be_clickable() => wait until element is enabled and clickable in the DOM
        EC.invisibility_of_element_located() => wait for an element to disappear (used in waiting for loading spinner to finish loading)
        EC.text_to_be_present_in_element() => wait for specific text to appear
    """

    # wait for element to appear in DOM
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".quote")))

    # when it reaches this, it means that the element has appeared
    quotes = driver.find_elements(By.CSS_SELECTOR, ".quote .text")
    for quote in quotes:
        print(quote.text)

    driver.quit()

"""
    Handling timeouts gracefully
"""
def timeout_handling():
    driver = get_driver()
    driver.get("https://quotes.toscrape.com")

    wait =WebDriverWait(driver, 5)

    try:
        # we purposely use EC to wait for an non-existent element in the DOM
        non_exist_element = wait.until(EC.presence_of_element_located((By.ID, "non-exist")))
        non_exist_element.find_element(By.CSS_SELECTOR, '.non_exist_btn')
        non_exist_element.click()
    except TimeoutException:
        print("Timeout, element does not exist in DOM, moving on...")
    
    quotes = driver.find_elements(By.CSS_SELECTOR, '.quote .text')
    for quote in quotes:
        print(quote.text)
    driver.quit()

timeout_handling()