import time
import logging
import csv
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException, ElementNotInteractableException
import os
import traceback
import re

months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

years = [2023, 2024, 2025]


# ---------- Configuration ----------
USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
              "AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/120.0.0.0 Safari/537.36")

# ---------- Helpers to act "human" ----------
def human_sleep(a=1, b=1.5):
    """Short randomized pause between actions."""
    time.sleep(random.uniform(a, b))

logging.basicConfig(
    filename="log.txt",         # Log file name
    level=logging.INFO,         # Minimum log level to capture
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log message format
    datefmt="%Y-%m-%d %H:%M:%S"  # Timestamp format
)

def open_ge_page(driver):
    print("Opening GE funds page...")
    driver.get("https://www.greateasternlife.com/sg/en/personal-insurance/our-products/wealth-accumulation/great-invest-advantage/greatlink-funds-prices.html")
    time.sleep(10)


def get_daily_prices(driver):
    open_ge_page(driver)
    wait = WebDriverWait(driver, 10)

    while True:
        try:
            # Wait until the div is visible and clickable
            load_more = wait.until(
                EC.element_to_be_clickable((By.ID, "loadmore1"))
            )

            # Check if the element is actually visible (not display:none)
            if load_more.is_displayed():
                print("Clicking 'Load more'...")
                load_more.click()
                time.sleep(1)
            else:
                print("'Load more' hidden (display:none). Stopping.")
                break

            driver.implicitly_wait(3)

        except TimeoutException:
            print("No more 'Load more' button found or not clickable.")
            break
        except ElementClickInterceptedException:
            print("Click intercepted — maybe a popup or overlay. Retrying later.")
            break

    # --- Extract valuation date from header ---
    header_date_element = driver.find_element(By.ID, "headerDate")
    # Example text: "(Valuation Date:10 Oct 2025)"
    match = re.search(r"Valuation Date:(.*)\)", header_date_element.text)
    valuation_date = match.group(1).strip() if match else "Unknown"

    # --- Extract table body ---
    table_body = driver.find_element(By.ID, "targetTableBody1")
    rows = table_body.find_elements(By.TAG_NAME, "tr")

    data = []

    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) >= 3:
            fund_name = cells[0].text.strip()
            bid_price = cells[1].text.strip()
            offer_price = cells[2].text.strip()

            data.append({
                "fund_name": fund_name,
                "valuation_date": valuation_date,
                "bid_price": bid_price,
                "offer_price": offer_price
            })

    return data


def scrap_historical_price_table(driver):
    data = []
    error_elements = driver.find_elements(
        By.CSS_SELECTOR,
        "#targetTableBody3 .regError.marginBottom25"
    )
    if error_elements:
        print("⚠️ Error found:", error_elements[0].text)
        return
    fund_name = driver.find_element(
        By.CSS_SELECTOR, "#targetTableBody2 h3").text.strip()
    while (True):
        # Locate the table body by class name
        table_body = driver.find_element(
            By.CSS_SELECTOR, "#targetTableBody2 tbody.targetTableBody")

        # Get all rows in the table body
        rows = table_body.find_elements(By.TAG_NAME, "tr")

        # Loop through each row
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            valuation = cells[0].text.strip()
            bid_price = cells[1].text.strip()
            offer_price = cells[2].text.strip()

            data.append({
                "Fund Name": fund_name,
                "Valuation": valuation,
                "Bid Price": bid_price,
                "Offer Price": offer_price
            })

        try:
            next_link = driver.find_element(
                By.XPATH, "//a[normalize-space(text())='Next']"
            )
            next_link.click()
            # Allocate time for page to load the data
            time.sleep(10)

        except NoSuchElementException:
            break

    csv_file = "fund_prices.csv"
    file_exists = os.path.isfile(csv_file)

    with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=["Fund Name", "Valuation", "Bid Price", "Offer Price"])
        # Write header only if file is new
        if not file_exists:
            writer.writeheader()
        writer.writerows(data)

    print(f"✅ {len(data)} rows saved saved for {fund_name} → {csv_file}")

# Used to generate a csv file for seed data
def get_all_funds_historical_prices(driver):
    open_ge_page(driver)

    available_funds = driver.find_element(By.ID, "availablefunds")
    select_obj = Select(available_funds)
    all_option_values = [option.get_attribute(
        "value") for option in select_obj.options if option.get_attribute("value") != 'all']
    print(all_option_values)
    add_link = driver.find_element(By.LINK_TEXT, "Add »")
    reset_link = driver.find_element(By.LINK_TEXT, "Reset Selection")
    display_link = driver.find_element(By.LINK_TEXT, "Display Fund Prices")
    mth_div = driver.find_element(By.ID, "selectMth")
    year_input = driver.find_element(By.ID, "selectYr")
    display_price = driver.find_element(
        "xpath", "//input[@value='display-prices-by-month']")
    title_ele = driver.find_element(
        By.XPATH, "//h4[normalize-space(text())='Historical Prices']"
    )

    """
    STEPS
    1. Select option
    2. Click Add button
    3. Click Display prices by month
    4. Select month
    5. Fill in year
    6. Click Display fund prices
    7. Scrape 
    8. Click Next if have, repeat 7
    9. Save data to csv file
    10. Move on to next date
    11. When done with dates, reset selection and move on to next option
    """
    for value in all_option_values:
        element = driver.find_element(
            "xpath", f"//option[@value='{value}']")
        element.click()
        human_sleep()

        add_link.click()
        human_sleep()

        display_price.click()
        human_sleep()

        for year in years:
            try:
                year_input.clear()
                year_input.send_keys(f"{year}")
                human_sleep()
                for i, month in enumerate(months):
                    month_changed = False
                    while not month_changed:
                        try:
                            mth_div.click()
                            time.sleep(3) # Timeout for full element to load and be interactable
                            label_element = driver.find_element(
                                By.XPATH, f"//label[@class='dd-option-text' and normalize-space(text())='{month}']"
                            )
                            label_element.click()
                            human_sleep()
                            month_changed = True
                        except Exception:
                            traceback.print_exc()
                            break
                    human_sleep()
                    display_link.click()

                    # Allocate time for page to load the data
                    time.sleep(10)

                    # Just to reset any click issues
                    title_ele.click()

                    scrap_historical_price_table(driver)
                    time.sleep(60)
            except Exception:
                traceback.print_exc()
        reset_link.click()


def main():
    driver = uc.Chrome(headless=False, use_subprocess=False)
    try:
        get_daily_prices(driver)
        # get_all_funds_historical_prices(driver)

    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.quit()
        print("Browser closed")


if __name__ == "__main__":
    main()
