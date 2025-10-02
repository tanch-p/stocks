import requests
import psycopg2
import os
from psycopg2.extras import execute_batch
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("ALPHA_API_KEY")
SYMBOLS = ["AAPL"]    # , "MSFT", "GOOGL"

# Database connection info
DB_CONFIG = {
    "dbname": "stocktracker",
    "user": "postgres",
    "password": "yourpassword",
    "host": "localhost",
    "port": 5432,
}


def fetch_latest_candle(symbol: str):
    """Fetch only the most recent daily candle for a stock."""
    url = (
        f"https://www.alphavantage.co/query"
        f"?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
    )
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json().get("Time Series (Daily)", {})

    if not data:
        return None, None

    # Most recent date (latest trading day)
    latest_date = max(data.keys())
    values = data[latest_date]

    return latest_date, {
        "open": float(values["1. open"]),
        "high": float(values["2. high"]),
        "low": float(values["3. low"]),
        "close": float(values["4. close"]),
        "volume": int(values["5. volume"]),
    }


def fetch_stock_data(symbol: str):
    """Fetch daily stock prices for a symbol from Alpha Vantage."""
    url = (
        f"https://www.alphavantage.co/query"
        f"?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
    )
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    return data.get("Time Series (Daily)", {})


def insert_latest(symbol: str, date: str, candle: dict):
    """Insert the latest OHLCV candle into Postgres."""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO stocktable (symbol, date, open, high, low, close, volume)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (symbol, date) DO UPDATE
        SET open = EXCLUDED.open,
            high = EXCLUDED.high,
            low = EXCLUDED.low,
            close = EXCLUDED.close,
            volume = EXCLUDED.volume;
    """, (
        symbol,
        date,
        candle["open"],
        candle["high"],
        candle["low"],
        candle["close"],
        candle["volume"],
    ))

    conn.commit()
    cur.close()
    conn.close()


def main():
    for symbol in SYMBOLS:
        print(f"Fetching {symbol}...")
        date, candle = fetch_latest_candle(symbol)
        if date and candle:
            insert_latest(symbol, date, candle)
            print(f"Inserted {symbol} for {date}: {candle}")
        else:
            print(f"No data for {symbol} (maybe hit API limit).")


if __name__ == "__main__":
    main()
