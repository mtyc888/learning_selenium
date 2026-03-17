from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# Options allows us to configure and customize browser behavior before a session starts


"""
    This function initializes a driver instance, add arguments and returns it,
    it takes in a boolean value,
    If True => user wants to create a driver with the GUI
    If False => user wants to create a driver without the GUI
"""
def get_driver(headless=False):
    # we initialize the options to add arguments
    options = Options()
    # headless allows us to run the driver without the GUI chrome browser appearing.
    if headless:
        options.add_argument('--headless=new')
    """
        some useful arguements are:
        --no-sandbox => bypass OS sandbox
        --disable-popup-blocking => Disables pop-up blocking
        --ignore-certificate-errors => Ignore SSL certificate errors
        --start-maximized => Open browser in maximized mode
        --incognito => opens chrome in incognito mode
        --disable-blink-features=AutomationControlled => helps avoid detection
        etc.
    """
    options.add_argument('--no-sandbox')
    options.add_argument('--incognito')

    # after we set out arguements, we create the driver instance and set the options into the driver.
    driver = webdriver.Chrome(
        # service is used to manage the starting and stopping of local browser driver processes
        service = Service(executable_path='chromedriver.exe'),
        options=options
    )
    return driver

def demo_1_navigation():
    try:
        # call the get_driver function to create a driver instance
        # we don't want the GUI so we give True
        driver = get_driver(headless=False)

        # now we set the driver to go to a specific website
        driver.get("https://seths.blog/")
        print(driver.current_url)
        text_element = driver.find_element(By.CLASS_NAME, "wp-block-paragraph .p")
        print("Text:",text_element.text)
    except Exception as e:
        print(f"An error occured: {e}")
    finally:
        driver.quit()

def main():
    demo_1_navigation()

main()