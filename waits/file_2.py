"""
SELENIUM CRASH COURSE — Part 2: WAITS (The #1 Interview Topic)
===============================================================
This is the most important file in this tutorial.

WHY WAITS MATTER:
Modern websites load content dynamically (AJAX, JS rendering).
If you try to find an element before it exists, your script crashes.
Waits solve this. Interviewers WILL test if you know this.

THE GOLDEN RULE: Never use time.sleep() for waiting in production code.
Use explicit waits instead. (time.sleep is fine for quick debugging only)
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
)
from webdriver_manager.chrome import ChromeDriverManager


def get_driver(headless=False):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver


# ============================================================
# 1. EXPLICIT WAITS (WebDriverWait) — What You Must Know
# ============================================================
# Pattern: WebDriverWait(driver, timeout).until(condition)
# This polls the DOM every 0.5s until the condition is met or timeout.

def explicit_wait_demo():
    driver = get_driver()
    driver.get("https://quotes.toscrape.com/js/")  # JS-rendered version of the site!
    
    # BAD — This might fail because content loads via JavaScript:
    # quotes = driver.find_elements(By.CSS_SELECTOR, ".quote")
    
    # GOOD — Wait up to 10 seconds for quotes to appear:
    wait = WebDriverWait(driver, 10)
    
    # Wait for element to be PRESENT in DOM
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".quote")))
    
    # Now safe to grab them
    quotes = driver.find_elements(By.CSS_SELECTOR, ".quote .text")
    print(f"Found {len(quotes)} quotes (JS-rendered page)")
    for q in quotes[:3]:
        print(f"  → {q.text[:60]}...")
    
    # ---------------------------------------------------------
    # THE KEY EXPECTED CONDITIONS — Memorize these 5:
    # ---------------------------------------------------------
    
    # 1. presence_of_element_located — Element exists in DOM (may not be visible)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".quote")))
    
    # 2. visibility_of_element_located — Element is visible on page
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".quote")))
    
    # 3. element_to_be_clickable — Element is visible AND enabled (use before .click())
    next_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.next a")))
    
    # 4. invisibility_of_element_located — Wait for loading spinner to disappear
    # wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".loading-spinner")))
    
    # 5. text_to_be_present_in_element — Wait for specific text to appear
    # wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".status"), "Complete"))
    
    driver.quit()


# ============================================================
# 2. HANDLING TIMEOUTS GRACEFULLY
# ============================================================

def timeout_handling_demo():
    driver = get_driver()
    driver.get("https://quotes.toscrape.com")
    
    wait = WebDriverWait(driver, 5)  # 5 second timeout
    
    # Use try/except for elements that might not exist
    try:
        # This element doesn't exist — will timeout after 5 seconds
        popup = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".cookie-popup"))
        )
        popup.find_element(By.CSS_SELECTOR, ".dismiss").click()
        print("Dismissed popup")
    except TimeoutException:
        print("No popup found — continuing normally")
    
    # Continue with the rest of your script...
    quotes = driver.find_elements(By.CSS_SELECTOR, ".quote .text")
    print(f"Proceeding with {len(quotes)} quotes")
    
    driver.quit()


# ============================================================
# 3. CUSTOM WAIT CONDITIONS
# ============================================================
# Sometimes the built-in conditions aren't enough.

def custom_wait_demo():
    driver = get_driver()
    driver.get("https://quotes.toscrape.com/js/")
    
    wait = WebDriverWait(driver, 10)
    
    # Custom condition: wait until at least 5 quotes are loaded
    def at_least_n_elements(css_selector, n):
        """Returns a callable that WebDriverWait can use."""
        def check(driver):
            elements = driver.find_elements(By.CSS_SELECTOR, css_selector)
            if len(elements) >= n:
                return elements  # Truthy = condition met, returns the elements
            return False         # Falsy = keep waiting
        return check
    
    quotes = wait.until(at_least_n_elements(".quote", 5))
    print(f"At least 5 quotes loaded: got {len(quotes)}")
    
    driver.quit()


# ============================================================
# 4. STALE ELEMENT REFERENCE — Common Gotcha
# ============================================================
# A "stale" element is one that was found but the DOM has since changed
# (e.g., page navigated, AJAX refreshed the section).
# Solution: re-find the element after any page change.

def stale_element_demo():
    driver = get_driver()
    driver.get("https://quotes.toscrape.com")
    
    wait = WebDriverWait(driver, 10)
    
    # Find the "Next" button
    next_btn = driver.find_element(By.CSS_SELECTOR, "li.next a")
    next_btn.click()
    
    # After clicking, the old page is gone. If you try to use
    # elements from the previous page, you get StaleElementReferenceException.
    
    # SOLUTION: Wait for new page to load, then re-find elements
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".quote")))
    
    # Now find elements fresh on the new page
    quotes = driver.find_elements(By.CSS_SELECTOR, ".quote .text")
    print(f"Page 2 has {len(quotes)} quotes")
    print(f"First quote on page 2: {quotes[0].text[:60]}...")
    
    driver.quit()


# ============================================================
# 5. IMPLICIT WAITS (Know This, But Prefer Explicit)
# ============================================================
# An implicit wait tells the driver to poll for a set time
# when finding ANY element. It's global and less precise.

def implicit_wait_demo():
    driver = get_driver()
    driver.implicitly_wait(10)  # Wait up to 10s for any find_element call
    
    driver.get("https://quotes.toscrape.com/js/")
    
    # This will automatically wait up to 10s for the element
    quotes = driver.find_elements(By.CSS_SELECTOR, ".quote .text")
    print(f"Found {len(quotes)} quotes using implicit wait")
    
    # IMPORTANT: Don't mix implicit and explicit waits! Pick one approach.
    # Explicit waits are preferred because they're more precise.
    
    driver.quit()


# ============================================================
# RUN ONE DEMO AT A TIME
# ============================================================

if __name__ == "__main__":
    explicit_wait_demo()
    # timeout_handling_demo()
    # custom_wait_demo()
    # stale_element_demo()
    # implicit_wait_demo()