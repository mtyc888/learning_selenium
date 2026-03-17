from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

"""
    create a driver to scrap something from https://seths.blog/
"""

def get_driver(headless=False):

    # create option instance
    options = Options()

    if headless:
        options.add_argument('--headless=new')
    
    options.add_argument('--incognito')
    options.add_argument('--no-sandbox')

    # create driver instance
    driver = webdriver.Chrome(
        # get the web driver
        service = Service(executable_path='chromedriver.exe'),
        options=options
    )

    return driver

def scrape():
    # create driver instance
    driver = get_driver(headless=False)

    driver.get('https://seths.blog/')
    post_container = driver.find_element(By.CLASS_NAME, 'post')
    # We were taught to look out for red flags. Little signs that something is wrong, that we should be careful or even turn around.
    text_element = post_container.find_element(By.CSS_SELECTOR, 'p.wp-block-paragraph:nth-of-type(1)')
    print(text_element.text)
    # This should print: Don't let that distract you from being on the lookout for green flags
    text_element = post_container.find_element(By.CSS_SELECTOR, 'p.wp-block-paragraph:nth-of-type(2)')
    print(text_element.text)
    driver.quit()

scrape()