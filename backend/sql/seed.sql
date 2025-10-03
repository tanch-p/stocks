-- seed.sql: Insert sample data for development

-- Users
INSERT INTO users (email,username, password_hash) VALUES
('alice@example.com', 'alice', 'hash1'),
('bob@example.com','bob', 'hash2');

-- Stocks
INSERT INTO stocks (symbol, name) VALUES
('AAPL', 'Apple Inc.'),
('TSLA', 'Tesla Inc.'),
('GOOG', 'Alphabet Inc.');

-- User-Stock relationships
INSERT INTO user_stocks (user_id, stock_id) VALUES
(1, 1), -- Alice -> AAPL
(1, 2), -- Alice -> TSLA
(2, 1), -- Bob -> AAPL
(2, 3); -- Bob -> GOOG

INSERT INTO funds (name, fund_sg_id) VALUES ('ABC Growth Fund','ABC');
INSERT INTO fund_prices (fund_id, price_date, bid_price, offer_price)
VALUES (1, '2025-09-30', 1.2345, 1.3456);
