from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import json
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
        service = Service(executable_path='../chromedriver.exe'),
        options=options
    )
    return driver

def demo_1_interation():
    """
        To interact with specific elements in a page, we use selectors.

        Summary Table:

        ID => By.ID, "user-id"
        Name => By.NAME, "email"
        ClassName => By.CLASS_NAME, "wp-block-paragraph"
        CSS => By.CSS_SELECTOR, "div.btn"
        XPath => By.XPATH, "//div/input"
        TagName => By.TAG_NAME, "a"
        LinkText => By.LINK_TEXT, "Log In"
        PartialLink => By.PARTIAL_LINK_TEXT, "Log"
    """
    # inserting into search box
    driver = get_driver(headless=False)
    driver.get("https://seths.blog/")
    wait = WebDriverWait(driver,5)
    search_field = driver.find_element(By.ID, "s")
    search_field.clear()
    search_field.send_keys("Ai chatbots")

    # clicking the search button
    submit_btn = driver.find_element(By.ID, "searchsubmit")
    submit_btn.click()

    #time.sleep(3)
    # wait for search results to appear
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".search-results mark")))

    search_results = driver.find_element(By.CLASS_NAME, "search-results")
    spans = search_results.find_elements(By.TAG_NAME, 'span')

    for span in spans:
        if "AI" in span.text:
            print(f"term AI found: {span.text[:30]}...")
            """
                More on XPATH:
                "." tells the program to start from this specific <span>
                "preceding-sibling" looks at elements that are on the same level (siblings) but appear above the current element
                "following-sibling" look at elements on the same level that appear below the current element
                "h2" this tell XPath what kind of sibling you are looking for, in this case we only care about siblings that are <h2> tags
                "[1]" this tells XPath to look backwards with preceding-siblings, [1] refers to the closest siblings moving upwards
                "/a" this tells XPath to look inside the <h2> tag and find the <a> tag
            """
            link = span.find_element(By.XPATH, "./preceding-sibling::h2[1]/a")
            link.click()
            break
    else:
        print("ERROR: No span matched 'AI'")
        print(f"Spans found: {[s.text[:40] for s in spans]}")
        driver.quit()
        return None
    wait.until(EC.presence_of_element_located((By.ID, "wrapper")))
    content_wrapper = driver.find_element(By.ID, "wrapper")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".single-post.single-view")))
    content_container = content_wrapper.find_element(By.CSS_SELECTOR, ".single-post.single-view")
    content_div = content_container.find_element(By.CSS_SELECTOR, ".post.single")
    p_elements = content_div.find_elements(By.TAG_NAME, "p")
    content = []
    for p_element in p_elements:
        content.append(p_element.text)

    content_str = ' '.join(content)
    search_data = {
        "url":"https://seths.blog/",
        "content":content_str
    }
    
    
    return search_data


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
    content = demo_1_interation()
    url = content['url']
    content_str = content['content']
    print(f"Found related article from {url}: {content_str}.")

main()