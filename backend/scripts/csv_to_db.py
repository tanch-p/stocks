import csv
import psycopg2
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

conn = psycopg2.connect(
    dbname="stocktracker",
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host="localhost"
)
cur = conn.cursor()

CSV_FILE = "fund_prices.csv"
FUND_NAME = "ABC Growth Fund"   # change this for each fund

# Step 1: Ensure the fund exists
cur.execute("""
    SELECT f.fund_id,
               f.name
        FROM funds f
""")
rows = cur.fetchall()
print(rows)

cur.execute("""
    INSERT INTO funds (name)
    VALUES (%s)
    ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
    RETURNING fund_id;
""", (FUND_NAME,))
fund_id = cur.fetchone()[0]
print(fund_id)

# Step 2: Read CSV and insert rows

with open('test.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    
    for row in csv_reader:
        # Parse values
        price_date = datetime.strptime(row["date"], "%d %b %Y").date()
        bid_price = float(row["bid price"])
        offer_price = float(row["offer price"])

        # Insert or update price record
        cur.execute("""
            INSERT INTO fund_prices (fund_id, price_date, bid_price, offer_price)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (fund_id, price_date)
            DO UPDATE SET bid_price = EXCLUDED.bid_price,
                          offer_price = EXCLUDED.offer_price;
        """, (fund_id, price_date, bid_price, offer_price))

conn.commit()
cur.close()
conn.close()