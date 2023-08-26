-- create schema commerce
CREATE SCHEMA commerce;

-- Use commerce schema
SET search_path TO commerce;

-- create a users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email_address TEXT NOT NULL UNIQUE,
    CONSTRAINT check_email CHECK (email_address ~* '^[A-Za-z0-9]+@[A-Za-z0-9]+.[A-Za-z0-9]+$')
);

CREATE TABLE IF NOT EXISTS products (
   id SERIAL PRIMARY KEY, 
   name VARCHAR(255) NOT NULL,
   description TEXT,
   price NUMERIC(5,2) NOT NULL
);

ALTER TABLE users REPLICA IDENTITY FULL;

ALTER TABLE products REPLICA IDENTITY FULL;

