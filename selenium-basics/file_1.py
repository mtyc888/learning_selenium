"""
SELENIUM CRASH COURSE — Part 1: Setup & Core Patterns
======================================================
Run each section one at a time (comment/uncomment as needed).
Practice site: https://quotes.toscrape.com (built for scraping practice)

INSTALL FIRST:
    pip install selenium webdriver-manager beautifulsoup4

webdriver-manager auto-downloads the correct chromedriver for your Chrome version,
so you never have to manually manage it.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# ============================================================
# 1. LAUNCHING A BROWSER
# ============================================================
# This is your boilerplate — memorize this pattern.

def get_driver(headless=False):
    """Create and return a Chrome WebDriver instance."""
    options = Options()
    if headless:
        options.add_argument("--headless=new")  # No visible browser window
    
    # Common useful options:
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    # options.add_argument("--disable-blink-features=AutomationControlled")  # Helps avoid detection
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver


# ============================================================
# 2. FINDING ELEMENTS — The Most Important Skill
# ============================================================
# You already know CSS selectors — that's 90% of the battle.
# Selenium uses By.CSS_SELECTOR, By.XPATH, By.ID, By.CLASS_NAME, etc.

def finding_elements_demo():
    driver = get_driver()
    driver.get("https://quotes.toscrape.com")
    
    # --- By CSS Selector (YOUR BREAD AND BUTTER — you already know these) ---
    # Single element
    first_quote = driver.find_element(By.CSS_SELECTOR, ".quote .text")
    print(f"First quote: {first_quote.text}")
    
    # Multiple elements
    all_quotes = driver.find_elements(By.CSS_SELECTOR, ".quote .text")
    print(f"Found {len(all_quotes)} quotes on this page")
    
    # --- By ID ---
    # (not many IDs on this site, but the pattern is:)
    # element = driver.find_element(By.ID, "some-id")
    
    # --- By XPath (useful when CSS selectors aren't enough) ---
    # XPath can search by text content — CSS can't do this
    login_link = driver.find_element(By.XPATH, "//a[text()='Login']")
    print(f"Found link: {login_link.text}")
    
    # XPath: find element containing partial text
    # //a[contains(text(), 'Login')]
    
    # XPath: find element by attribute
    # //input[@name='username']
    
    # --- IMPORTANT: find_element vs find_elements ---
    # find_element  → returns ONE element, throws NoSuchElementException if not found
    # find_elements → returns a LIST, returns [] if not found (no exception!)
    
    tags = driver.find_elements(By.CSS_SELECTOR, ".tag-item a")
    print(f"\nTop tags: {[tag.text for tag in tags]}")
    
    driver.quit()


# ============================================================
# 3. INTERACTING WITH ELEMENTS
# ============================================================

def interaction_demo():
    driver = get_driver()
    driver.get("https://quotes.toscrape.com/login")
    
    # --- Typing into inputs ---
    username_field = driver.find_element(By.CSS_SELECTOR, "#username")
    username_field.clear()              # Always clear first
    username_field.send_keys("admin")   # Type text
    
    password_field = driver.find_element(By.CSS_SELECTOR, "#password")
    password_field.clear()
    password_field.send_keys("admin")
    
    # --- Clicking ---
    submit_btn = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
    submit_btn.click()
    
    time.sleep(1)  # Quick pause to see the result
    
    # After login, check if we're on a new page
    print(f"Current URL: {driver.current_url}")
    
    # --- Other useful interactions ---
    # element.send_keys(Keys.ENTER)     # Press Enter
    # element.send_keys(Keys.TAB)       # Press Tab
    # from selenium.webdriver.common.keys import Keys  # Import Keys first
    
    # element.get_attribute("href")     # Get any HTML attribute
    # element.get_attribute("value")    # Get input value
    # element.text                      # Get visible text
    # element.is_displayed()            # Check if visible
    # element.is_enabled()              # Check if clickable
    
    driver.quit()


# ============================================================
# 4. NAVIGATION
# ============================================================

def navigation_demo():
    driver = get_driver()
    
    driver.get("https://quotes.toscrape.com")        # Go to URL
    print(f"Title: {driver.title}")
    print(f"URL: {driver.current_url}")
    
    driver.get("https://quotes.toscrape.com/page/2") # Go to another URL
    driver.back()                                      # Browser back
    time.sleep(5)
    driver.forward()                                   # Browser forward
    time.sleep(5)
    driver.refresh()                                   # Refresh page
    
    time.sleep(5)
    driver.quit()


# ============================================================
# RUN ONE DEMO AT A TIME (uncomment the one you want to try)
# ============================================================

if __name__ == "__main__":
    #finding_elements_demo()
    # interaction_demo()
    navigation_demo()