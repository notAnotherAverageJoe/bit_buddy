
-- Create the database "bitbuddy"
CREATE DATABASE bitbuddy;

-- Connect to the "bitbuddy" database
\c bitbuddy;





-- Create the "User" table
CREATE TABLE "User" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

-- Create the "CryptoCurrency" table if it doesn't already exist
CREATE TABLE IF NOT EXISTS CryptoCurrency (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    descriptions VARCHAR(255) NOT NULL
);

-- Insert data into the "User" table
INSERT INTO "User" (username, email, password_hash) VALUES
('user1', 'user1@example.com', 'password1'),
('user2', 'user2@example.com', 'password2'),
('user3', 'user3@example.com', 'password3');

-- Cryptocurrencies possible deletion
INSERT INTO CryptoCurrency (name, symbol, descriptions) VALUES
('Bitcoin', 'BTC', 'decentralized'),
('Ethereum', 'ETH', 'smart contracts'),
('Litecoin', 'LTC', 'smart contracts'),
('DogeCoin', 'DOGE', 'meme coin');

-- Create the "TransactionHistory" table
CREATE TABLE IF NOT EXISTS TransactionHistory (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "User"(id),
    cryptocurrency_id INTEGER REFERENCES CryptoCurrency(id),
    transaction_type VARCHAR(20) NOT NULL,
    amount DECIMAL(18, 8) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert data into the "TransactionHistory" table
-- Make sure the "user_id" values exist in the "User" table and "cryptocurrency_id" values exist in the "CryptoCurrency" table
INSERT INTO TransactionHistory (user_id, cryptocurrency_id, transaction_type, amount) VALUES
(1, 1, 'buy', 0.5),
(1, 2, 'sell', 1.2),
(2, 1, 'buy', 0.8),
(3, 3, 'sell', 5.0);
