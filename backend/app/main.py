from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import os
import logging
import uvicorn
import psycopg2
import psycopg2.extras
from datetime import date
from routes import auth


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_CONFIG = {
    "dbname": "stocktracker",
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": "localhost"
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


app = FastAPI(
    title="My API",
    description="This is an example API with Swagger docs",
    version="1.0.0",
    docs_url="/swagger",   # change default /docs
    redoc_url="/redoc",    # change default /redoc
    openapi_url="/openapi.json"  # OpenAPI schema endpoint
)

# Middleware
# Allow your frontend origin
origins = [
    "http://localhost:5173",  # your Vite frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # or ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],         # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],         # Authorization, Content-Type, etc.
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/funds", response_model=List[Dict], summary="Get funds with latest price")
def get_funds_with_latest_price():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Query: each fund with its latest price
    cur.execute("""
        SELECT f.fund_id,
               f.name,
               p.price_date,
               p.bid_price,
               p.offer_price
        FROM funds f
        JOIN LATERAL (
            SELECT price_date, bid_price, offer_price
            FROM fund_prices fp
            WHERE fp.fund_id = f.fund_id
            ORDER BY price_date DESC
            LIMIT 1
        ) p ON TRUE
        ORDER BY f.name;
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    # Convert to dict list for FastAPI response
    return [
        {
            "name": row["name"],
            "latest_date": row["price_date"],
            "bid_price": float(row["bid_price"]),
            "offer_price": float(row["offer_price"])
        }
        for row in rows
    ]

@app.get("/funds", response_model=List[Dict], summary="Get summary of all funds with latest price and performance")
def get_funds_summary():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Query: each fund with its latest price
    cur.execute("""
        SELECT f.fund_id,
               f.name,
               p.price_date,
               p.bid_price,
               p.offer_price
        FROM funds f
        JOIN LATERAL (
            SELECT price_date, bid_price, offer_price
            FROM fund_prices fp
            WHERE fp.fund_id = f.fund_id
            ORDER BY price_date DESC
            LIMIT 1
        ) p ON TRUE
        ORDER BY f.name;
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    # Convert to dict list for FastAPI response
    return [
        {
            "name": row["name"],
            "latest_date": row["price_date"],
            "bid_price": float(row["bid_price"]),
            "offer_price": float(row["offer_price"])
        }
        for row in rows
    ]


@app.get("/funds/history")
def get_funds_history(
    fund_ids: str = Query(...,
                          description="Comma-separated fund IDs, e.g. 1,2,3"),
    start_date: date = Query(...),
    end_date: date = Query(...)
):
    # Convert "1,2,3" → [1, 2, 3]
    fund_id_list = [int(x) for x in fund_ids.split(",")]

    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("""
        SELECT f.fund_id, f.name, p.price_date, p.bid_price, p.offer_price
        FROM fund_prices p
        JOIN funds f ON f.fund_id = p.fund_id
        WHERE p.fund_id = ANY(%s)
          AND p.price_date BETWEEN %s AND %s
        ORDER BY f.name, p.price_date;
    """, (fund_id_list, start_date, end_date))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    # Group by fund
    grouped: Dict[int, Dict[str, Any]] = {}
    for row in rows:
        fid = row["fund_id"]
        if fid not in grouped:
            grouped[fid] = {
                "fund_id": fid,
                "name": row["name"],
                "prices": []
            }
        grouped[fid]["prices"].append({
            "date": row["price_date"],
            "bid_price": float(row["bid_price"]),
            "offer_price": float(row["offer_price"])
        })

    return list(grouped.values())


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=9000,
        reload=True,
        log_level="info"
    )
from database import Base, engine
Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Auth API")
app.include_router(auth.router)
