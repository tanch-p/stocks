import time
import logging
import csv
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


# ---------- Configuration ----------
USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
              "AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/120.0.0.0 Safari/537.36")

# ---------- Helpers to act "human" ----------
def human_sleep(a=0.05, b=0.4):
    """Short randomized pause between actions."""
    time.sleep(random.uniform(a, b))

def human_type(element, text, min_delay=0.03, max_delay=0.18):
    """Type text into an element with randomized per-key delays."""
    for ch in text:
        element.send_keys(ch)
        time.sleep(random.uniform(min_delay, max_delay))

def human_move_and_click(driver, element):
    """Move cursor in small increments then click, via ActionChains."""
    actions = ActionChains(driver)
    # simulate multiple small moves
    steps = random.randint(5, 12)
    for _ in range(steps):
        actions.move_by_offset(random.uniform(-5,5), random.uniform(-5,5))
    actions.move_to_element(element).pause(random.uniform(0.05, 0.3)).click().perform()
    human_sleep(0.1, 0.4)


logging.basicConfig(
    filename="log.txt",         # Log file name
    level=logging.INFO,         # Minimum log level to capture
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log message format
    datefmt="%Y-%m-%d %H:%M:%S"  # Timestamp format
)


def write_to_csv():
    with open('fund_data.csv', 'w', newline='') as file:
        fieldnames = ['Date', 'Bid Price', 'Offer Price']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        # Write data
        writer.writerow(
            {'Date': '2025-09-30', 'Bid Price': 10.25, 'Offer Price': 10.35})
        writer.writerow(
            {'Date': '2025-09-29', 'Bid Price': 10.20, 'Offer Price': 10.30})
        writer.writerow(
            {'Date': '2025-09-28', 'Bid Price': 10.18, 'Offer Price': 10.28})


def add_fund_price(date, bid_price, offer_price):
    with open('fund_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, bid_price, offer_price])

def open_ge_page(driver):
    print("Opening GE funds page...")
    driver.get("https://www.greateasternlife.com/sg/en/personal-insurance/our-products/wealth-accumulation/great-invest-advantage/greatlink-funds-prices.html")
    time.sleep(10)

def get_fund_price(driver, fund_name):
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
            load_more = wait.until(
                EC.presence_of_element_located((By.ID, "loadmore1")))
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


def get_price_history(driver, duration=5):
    # default 5 years
    pass

def scrap_all_funds(driver):
    available_funds = driver.find_element(By.ID, "availablefunds")
    select_obj = Select(available_funds)
    all_options = select_obj.options

    add_link = driver.find_element(By.LINK_TEXT, "Add »")
    reset_link = driver.find_element(By.LINK_TEXT, "Reset Selection")
    display_link = driver.find_element(By.LINK_TEXT, "Display Fund Prices")
    display_price = driver.find_element(
        "xpath", "//input[@value='display-prices-by-month']")
    display_price.click()
    print("click")
    input("")
    for option in all_options:
        option_value = option.get_attribute("value")
        option_text = option.text

        # Skip the 'all' option
        if option_value == "all":
            continue

        print(f"Value: {option_value}, Text: {option_text}")
        option.click()
        time.sleep(0.5)
        add_link.click()


def main():
    driver = uc.Chrome(headless=False,use_subprocess=False)
    try:
        open_ge_page(driver)
        fund_name = "GreatLink Global Real Estate Securities Fund"
        # get_fund_price(driver, fund_name)
        scrap_all_funds(driver)

    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        driver.quit()
        print("Browser closed")


if __name__ == "__main__":
    main()
