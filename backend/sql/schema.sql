-- schema.sql: Database structure for stock tracking app

-- Drop tables if they already exist (for dev purposes)
DROP TABLE IF EXISTS user_stocks;
DROP TABLE IF EXISTS stocks;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS funds CASCADE;
DROP TABLE IF EXISTS fund_prices;

-- Users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    phone TEXT UNIQUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE user_passwords (
    user_id INT PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
    password_hash TEXT NOT NULL,
    last_changed TIMESTAMP DEFAULT NOW()
);

CREATE TABLE user_otps (
    otp_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    otp_code TEXT NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    is_used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE user_sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    token TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP NOT NULL
);

-- Stocks table
CREATE TABLE stocks (
    id SERIAL PRIMARY KEY,
    symbol TEXT NOT NULL,
    name TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Junction table: which users track which stocks
CREATE TABLE user_stocks (
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    stock_id INT REFERENCES stocks(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, stock_id)
);

-- Table for fund information
CREATE TABLE funds (
    fund_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    fund_sg_id TEXT NOT NULL UNIQUE
);

-- Table for daily prices
CREATE TABLE fund_prices (
    price_id SERIAL PRIMARY KEY,
    fund_id INT NOT NULL REFERENCES funds(fund_id) ON DELETE CASCADE,
    price_date DATE NOT NULL,
    bid_price NUMERIC(12, 4) NOT NULL,
    offer_price NUMERIC(12, 4) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),

    UNIQUE (fund_id, price_date)  -- prevent duplicate entries for same day
);

-- Index on fund name (quick lookups by name)
CREATE UNIQUE INDEX idx_funds_name ON funds (name);

-- Index on (fund_id, price_date) to speed up queries by fund + date
CREATE INDEX idx_fund_prices_fund_date ON fund_prices (fund_id, price_date);

-- Index on price_date for querying all funds on a specific date
CREATE INDEX idx_fund_prices_date ON fund_prices (price_date DESC);
