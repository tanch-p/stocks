from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import time
import logging

logging.basicConfig(
    filename="log.txt",         # Log file name
    level=logging.INFO,         # Minimum log level to capture
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log message format
    datefmt="%Y-%m-%d %H:%M:%S"  # Timestamp format
)


def setup_firefox_driver():

    # Configure Firefox options
    options = Options()

    # Essential preferences for session persistence
    prefs = {
        "dom.webdriver.enabled": False,
        "useAutomationExtension": False,
        "browser.sessionstore.resume_from_crash": True,
        "dom.storage.enabled": True,
        "browser.cache.disk.enable": True,
        "network.cookie.cookieBehavior": 0,
        "privacy.sanitize.sanitizeOnShutdown": True,
        "privacy.clearOnShutdown.cookies": True,
        "privacy.clearOnShutdown.cache": True,
        "privacy.clearOnShutdown.sessions": True,
        "browser.shell.checkDefaultBrowser": False
    }

    for pref, value in prefs.items():
        options.set_preference(pref, value)
    try:
        service = Service("/usr/local/bin/geckodriver")
        driver = webdriver.Firefox(service=service, options=options)
        return driver
    except Exception as e:
        print(f"Error initializing Firefox driver: {e}")
        print("Make sure geckodriver is installed and in your PATH")
        return None


def open_ge_page(driver):
    print("Opening GE funds page...")
    driver.get("https://www.greateasternlife.com/sg/en/personal-insurance/our-products/wealth-accumulation/great-invest-advantage/greatlink-funds-prices.html")
    time.sleep(10)

def get_fund_price(driver,fund_name):
    wait = WebDriverWait(driver, 10)
    row = None

    while True:
        try:
            # try to find the target row
            row = driver.find_element(
                By.XPATH,
                f'//tr[td[1][normalize-space()="{fund_name}"]]')
            # if found, break the loop
            if row.is_displayed():
                break
        except NoSuchElementException:
            pass

        # try clicking the Load More button if it exists
        try:
            load_more = wait.until(EC.presence_of_element_located((By.ID, "loadmore1")))
            if load_more.is_displayed() and load_more.is_enabled():
                driver.execute_script("arguments[0].click();", load_more)
                # optionally wait a bit for new rows to load
                WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//tr"))
                )
            else:
                break  # no more button
        except TimeoutException:
            break  # no more button
        except ElementClickInterceptedException:
            break  # something blocked clicking

    if row:
        tds = row.find_elements(By.TAG_NAME, "td")
        fund_name = tds[0].text
        bid_price = tds[1].text
        offer_price = tds[2].text

        print(f"Fund: {fund_name}")
        print(f"Bid Price: {bid_price}")
        print(f"Offer Price: {offer_price}")
    else:
        print("Target row not found.")

def main():
    driver = setup_firefox_driver()
    if not driver:
        return

    try:
        open_ge_page(driver)
        fund_name = "GreatLink Global Real Estate Securities Fund"
        get_fund_price(driver,fund_name)

    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()
        print("Browser closed")


if __name__ == "__main__":
    main()
