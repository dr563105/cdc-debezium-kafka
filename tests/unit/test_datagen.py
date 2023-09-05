from user_product_data import *
import pytest
import psycopg2
import os

TEST_POSTGRES_USER = os.getenv("TEST_POSTGRES_USER")
TEST_POSTGRES_PASSWORD = os.getenv("TEST_POSTGRES_PASSWORD")
TEST_POSTGRES_HOSTNAME = os.getenv("TEST_POSTGRES_HOST")
TEST_POSTGRES_DB = os.getenv("TEST_POSTGRES_DB")
TEST_SCHEMA = os.getenv("TEST_DB_SCHEMA")


@pytest.fixture(scope="module")
def db_connection():
    conn = psycopg2.connect(
        database=TEST_POSTGRES_DB,
        user=TEST_POSTGRES_USER,
        password=TEST_POSTGRES_PASSWORD,
        host=TEST_POSTGRES_HOSTNAME,
    )
    yield conn
    conn.close()
