-- Drop the database if it already exists
DROP DATABASE IF EXISTS bitbuddy;

-- Create the database "bitbuddy"
CREATE DATABASE bitbuddy;



CREATE TABLE User (
    id INTEGER PRIMARY KEY,
    username TEXT,
    email TEXT,
    password_hash TEXT
);

CREATE TABLE Cryptocurrency (
    id INTEGER PRIMARY KEY,
    name TEXT,
    symbol TEXT,
    price NUMERIC,
    purpose TEXT
);

CREATE TABLE TransactionHistory (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES User(id),
    transaction_type TEXT,
    amount NUMERIC,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);




-- Insert data into the User table
INSERT INTO User (id, username, email, password_hash)
VALUES
    (1, 'user1', 'user1@example.com', 'hash1'),
    (2, 'user2', 'user2@example.com', 'hash2'),
    (3, 'user3', 'user3@example.com', 'hash3');

-- Insert data into the Cryptocurrency table
INSERT INTO Cryptocurrency (id, name, symbol, price, purpose)
VALUES
    (1, 'Bitcoin', 'BTC', 50000, 'Digital currency'),
    (2, 'Ethereum', 'ETH', 3000, 'Smart contracts'),
    (3, 'Litecoin', 'LTC', 200, 'Payments');
    (4, 'Thisguyscoin', 'TGC', 2000, 'Payments');


-- Insert data into the TransactionHistory table
INSERT INTO TransactionHistory (id, user_id, transaction_type, amount, timestamp)
VALUES
    (1, 1, 'buy', 0.5, '2024-05-10 10:00:00'),
    (2, 2, 'sell', 1.2, '2024-05-10 11:00:00'),
    (3, 3, 'stake', 10, '2024-05-10 12:00:00');
