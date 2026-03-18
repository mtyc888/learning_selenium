import shutil
import tempfile
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
"""
    Scrape https://medium.com/
"""

def get_driver(headless=False):
    options = Options()
    if headless:
        options.add_argument('--headless=new')
    user_data = r"C:\Users\TN User\AppData\Local\Google\Chrome\User Data\Profile 1"
    temp_dir = tempfile.mkdtemp()
    temp_profile = os.path.join(temp_dir, "Profile 1")
    shutil.copytree(user_data, temp_profile)

    options.add_argument(f'--user-data-dir={temp_dir}')
    options.add_argument(f"--profile-directory=Profile 1")
    options.add_argument('--disable-popup-blocking')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(
        options=options,
        service = Service(executable_path='../chromedriver.exe')
    )

    return driver, temp_dir
def scrape_medium():
    driver, temp_dir = get_driver()
    try:
        driver.get("https://medium.com/@marwolwarl/ixs-the-god-tier-rwa-low-cap-you-joined-crypto-to-find-7dbea9c27cd2")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'p')))
        
        p_tags = driver.find_elements(By.TAG_NAME, "p")
        
        for tag in p_tags:
            print(tag.text)
        time.sleep(20)
    finally:
        driver.quit()
        shutil.rmtree(temp_dir, ignore_errors=True)
scrape_medium()