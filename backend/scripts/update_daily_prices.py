from stealth_selenium import get_daily_prices
import undetected_chromedriver as uc
import psycopg2
from operator import itemgetter
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- PostgreSQL connection ---
conn = psycopg2.connect(
    dbname="stocktracker",
    user="postgres",
    password="your_password",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()


def main():
    driver = uc.Chrome(headless=False, use_subprocess=False)
    data = []

    # Get data from site
    try:
        data = get_daily_prices(driver)
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.quit()
        print("Browser closed")

    # Insert data into db
    try:
        for item in data:
            fund_name, valuation_date, bid_price, offer_price = itemgetter(
                "fund_name", "valuation_date", "bid_price", "offer_price")(item)
            print(f"Inserting {fund_name} ({valuation_date})...")

            # --- Step 1: Get or create fund_id ---
            cursor.execute(
                "SELECT fund_id FROM funds WHERE name = %s", (fund_name,))
            result = cursor.fetchone()

            if result:
                fund_id = result[0]
            else:
                cursor.execute(
                    "INSERT INTO funds (name) VALUES (%s) RETURNING fund_id", (fund_name,)
                )
                fund_id = cursor.fetchone()[0]

            # --- Step 2: Insert price data ---
            cursor.execute("""
                INSERT INTO fund_prices (fund_id, price_date, bid_price, offer_price)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (fund_id, price_date)
                DO UPDATE SET
                    bid_price = EXCLUDED.bid_price,
                    offer_price = EXCLUDED.offer_price,
                    created_at = NOW();
            """, (fund_id, valuation_date, bid_price, offer_price))
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")

    finally:
        cursor.close()
        conn.close()
        print("Browser closed")


if __name__ == "__main__":
    main()
