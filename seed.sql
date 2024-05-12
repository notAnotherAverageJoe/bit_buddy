-- Create the database "bitbuddy"
CREATE DATABASE bitbuddy;

-- Connect to the "bitbuddy" database
\c bitbuddy;

-- Create the "User" table
CREATE TABLE "User" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(30) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);

-- Create the "CryptoCurrency" table if it doesn't already exist
CREATE TABLE IF NOT EXISTS CryptoCurrency (
    id SERIAL PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    symbol VARCHAR(5) NOT NULL,
    descriptions VARCHAR(100) NOT NULL
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

-- Create the trigger function
CREATE OR REPLACE FUNCTION prevent_delete_bitcoin()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if the record being deleted corresponds to Bitcoin (id = 1)
    IF OLD.id = 1 THEN
        RAISE EXCEPTION 'Bitcoin entry cannot be deleted.';
    END IF;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger
CREATE TRIGGER prevent_delete_bitcoin_trigger
BEFORE DELETE ON CryptoCurrency
FOR EACH ROW
EXECUTE FUNCTION prevent_delete_bitcoin();


CREATE OR REPLACE FUNCTION prevent_update_bitcoin()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if the record being updated corresponds to Bitcoin (id = 1)
    IF NEW.id = 1 THEN
        RAISE EXCEPTION 'Bitcoin entry cannot be updated.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

--  Create Trigger for Updates
CREATE TRIGGER prevent_update_bitcoin_trigger
BEFORE UPDATE ON cryptocurrency
FOR EACH ROW
EXECUTE FUNCTION prevent_update_bitcoin();
