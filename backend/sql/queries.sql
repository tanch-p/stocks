-- queries.sql: Example queries for testing

-- List all users
SELECT * FROM users;

-- List all stocks
SELECT * FROM stocks;

-- Which stocks does Alice track?
SELECT s.symbol, s.name
FROM stocks s
JOIN user_stocks us ON s.id = us.stock_id
JOIN users u ON u.id = us.user_id
WHERE u.email = 'alice@example.com';

-- Which users are tracking AAPL?
SELECT u.email
FROM users u
JOIN user_stocks us ON u.id = us.user_id
JOIN stocks s ON s.id = us.stock_id
WHERE s.symbol = 'AAPL';

-- Query latest price for each fund:
SELECT f.name, p.price_date, p.bid_price, p.offer_price
FROM funds f
JOIN fund_prices p ON f.fund_id = p.fund_id
WHERE p.price_date = (
    SELECT MAX(price_date) 
    FROM fund_prices 
    WHERE fund_id = f.fund_id
);
