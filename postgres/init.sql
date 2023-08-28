-- create schema commerce
CREATE SCHEMA commerce;

-- Use commerce schema
SET search_path TO commerce;

-- create a users table
CREATE TABLE IF NOT EXISTS users (
    id int PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email_address TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
   id int PRIMARY KEY, 
   name VARCHAR(255) NOT NULL,
   description TEXT,
   price REAL NOT NULL
);

ALTER TABLE users REPLICA IDENTITY FULL;

ALTER TABLE products REPLICA IDENTITY FULL;

