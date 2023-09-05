import psycopg2
import pytest
import os

# Environment variables for PostgreSQL connection
TEST_POSTGRES_USER = os.getenv("TEST_POSTGRES_USER")
TEST_POSTGRES_PASSWORD = os.getenv("TEST_POSTGRES_PASSWORD")
TEST_POSTGRES_HOSTNAME = os.getenv("TEST_POSTGRES_HOST")
TEST_POSTGRES_DB = os.getenv("TEST_POSTGRES_DB")
SCHEMA = os.getenv("DB_SCHEMA")

# Fixture for creating a database connection
@pytest.fixture(scope="module")
def db_connection():
    """
    Fixture for creating a PostgreSQL database connection.

    Yields:
        psycopg2.extensions.connection: A database connection object.
    """
    conn = psycopg2.connect(
        database=TEST_POSTGRES_DB,
        user=TEST_POSTGRES_USER,
        password=TEST_POSTGRES_PASSWORD,
        host=TEST_POSTGRES_HOSTNAME,
    )
    yield conn
    conn.close()


#Test case to check if db connection is active
def test_db_connection(db_connection):
    """
    Test case to check if the PostgreSQL database connection is active.

    Args:
        db_connection (psycopg2.extensions.connection): The database connection.

    Raises:
        AssertionError: If the connection is not of the expected type or is closed.
    """
    # The db_connection fixture should already be set up and open.
    assert isinstance(db_connection, psycopg2.extensions.connection)
    
    # Optionally, you can also check if the connection is open.
    assert not db_connection.closed

    # Perform any other necessary assertions or tests related to the database connection.
    # For example, you can try executing a simple query here to check if the connection is functional.
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        assert result == (1,)


# Test case to check if all tables in a schema exist
def test_all_tables_exist_in_schema(db_connection):
    """
    Test case to check if all expected tables exist in a PostgreSQL schema.

    Args:
        db_connection (psycopg2.extensions.connection): The database connection.

    Raises:
        AssertionError: If any expected tables are missing in the schema.
    """
    schema_name = SCHEMA

    # Create a cursor
    with db_connection.cursor() as cursor:
        # Execute a query to retrieve a list of all table names in the schema
        cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema_name}'")
        table_names = [row[0] for row in cursor.fetchall()]
        print(table_names)

    # List of expected table names
    expected_table_names = ["products", "users"]

    # Check if all expected tables exist in the schema
    missing_tables = [table_name for table_name in expected_table_names if table_name not in table_names]
    print(missing_tables)
    # Assert that there are no missing tables
    assert not missing_tables, f"Missing tables: {', '.join(missing_tables)}"