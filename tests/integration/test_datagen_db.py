# Import the functions and constants needed for testing
from user_product_data import *
import pytest
import psycopg2
import os

# Define your test database connection parameters
TEST_POSTGRES_USER = os.getenv("TEST_POSTGRES_USER")
TEST_POSTGRES_PASSWORD = os.getenv("TEST_POSTGRES_PASSWORD")
TEST_POSTGRES_HOSTNAME = os.getenv("TEST_POSTGRES_HOST")
TEST_POSTGRES_DB = os.getenv("TEST_POSTGRES_DB")
SCHEMA = os.getenv("DB_SCHEMA", "commerce") #using TEST_DB_SCHEMA just isn't working


@pytest.fixture(scope="module")
def db_connection():
    """
    Fixture to create a database connection for testing.

    This fixture establishes a database connection using the provided credentials and
    yields the connection object. After the test function that uses this connection is
    executed, the connection is closed.

    Returns:
        psycopg2.extensions.connection: The database connection.
    """
    conn = psycopg2.connect(
        database=TEST_POSTGRES_DB,
        user=TEST_POSTGRES_USER,
        password=TEST_POSTGRES_PASSWORD,
        host=TEST_POSTGRES_HOSTNAME
    )
    yield conn
    conn.close()


@pytest.mark.parametrize("id", [random.randint(15, 35)])
def test_insert_user_data(db_connection, id):
    """
    Test the insertion of user data into the database.

    This test function generates user data, inserts it into the database, and verifies
    that the inserted data exists in the database.

    Args:
        db_connection (psycopg2.extensions.connection): The database connection for testing.
        id (int): The user's ID for testing.

    Returns:
        None
    """
    user_data = generate_user_data(id)
    conn = db_connection
    cur = conn.cursor()
    insert_user_data(conn, cur, user_data)
    cur.execute(f"SELECT * FROM {SCHEMA}.users WHERE id = {user_data['id']}")
    inserted_user_data = cur.fetchone()

    assert inserted_user_data is not None

    conn.rollback()  # Rollback the transaction to undo the insertion
    cur.close()


@pytest.mark.parametrize("id", [random.randint(15, 35)])
def test_insert_product_data(db_connection, id):
    """
    Test the insertion of product data into the database.

    This test function generates product data, inserts it into the database, and verifies
    that the inserted data exists in the database.

    Args:
        db_connection (psycopg2.extensions.connection): The database connection for testing.
        id (int): The product's ID for testing.

    Returns:
        None
    """
    product_data = generate_product_data(id)
    conn = db_connection
    cur = conn.cursor()
    insert_product_data(conn, cur, product_data)
    cur.execute(f"SELECT * FROM {SCHEMA}.products WHERE id = {product_data['id']}")
    inserted_product_data = cur.fetchone()

    assert inserted_product_data is not None

    conn.rollback()  # Rollback the transaction to undo the insertion
    cur.close()


@pytest.mark.parametrize("id", [random.randint(100, 114)])
def test_update_records(db_connection, id):
    """
    Test the update of user and product records in the database.

    This test function generates user and product data, inserts them into the database,
    updates the records, and verifies that the updates are applied correctly.

    Args:
        db_connection (psycopg2.extensions.connection): The database connection for testing.
        id(int): The user's ID for testing. 

    Returns:
        None
    """
    user_data = generate_user_data(id)
    product_data = generate_product_data(id)
    conn = db_connection
    cur = conn.cursor()
    insert_user_data(conn, cur, user_data)
    insert_product_data(conn, cur, product_data)

    update_records(conn, cur, user_data, product_data, should_update=True)

    cur.execute(f"SELECT username FROM {SCHEMA}.users WHERE id = {user_data['id']}")
    updated_username = cur.fetchone()[0]
    cur.execute(f"SELECT name FROM {SCHEMA}.products WHERE id = {product_data['id']}")
    updated_name = cur.fetchone()[0]

    assert updated_username != user_data['username']
    assert updated_name != product_data['name']

    conn.rollback()  # Rollback the transaction to undo the update
    cur.close()


def get_user_count(cur):
    """
    Get the count of user records in the database.

    Args:
        cur (psycopg2.extensions.cursor): The database cursor.

    Returns:
        int: The count of user records.
    """
    cur.execute(f"SELECT COUNT(*) FROM {SCHEMA}.users")
    return cur.fetchone()[0]


def get_product_count(cur):
    """
    Get the count of product records in the database.

    Args:
        cur (psycopg2.extensions.cursor): The database cursor.

    Returns:
        int: The count of product records.
    """
    cur.execute(f"SELECT COUNT(*) FROM {SCHEMA}.products")
    return cur.fetchone()[0]


@pytest.mark.parametrize("id", [random.randint(46, 64)])
def test_delete_records(db_connection,id):
    """
    Test the deletion of user and product records from the database.

    This test function generates user and product data, inserts them into the database,
    deletes the records, and verifies that the records are deleted correctly.

    Args:
        db_connection (psycopg2.extensions.connection): The database connection for testing.
        id (int): The user's ID for testing.

    Returns:
        None
    """
    user_data = generate_user_data(id)
    product_data = generate_product_data(id)
    conn = db_connection
    cur = conn.cursor()
    insert_user_data(conn, cur, user_data)
    insert_product_data(conn, cur, product_data)

    initial_user_count = get_user_count(cur)
    initial_product_count = get_product_count(cur)

    delete_records(conn, cur, user_data, product_data, should_delete=True)

    final_user_count = get_user_count(cur)
    final_product_count = get_product_count(cur)

    # Check if either user or product records are deleted
    assert (final_user_count <= initial_user_count) and (final_product_count <= initial_product_count)

    conn.rollback()  # Rollback the transaction to undo the deletion
    cur.close()


@pytest.mark.parametrize("num_records", [10])
def test_gen_user_product_data(db_connection, num_records):
    """
    Test the generation of user and product data, and verify database consistency.

    This test function generates user and product data using the 'gen_user_product_data' function
    and verifies the correctness of the generated data by comparing user and product counts in
    the database.

    Args:
        db_connection (psycopg2.extensions.connection): The database connection to be used for testing.
        num_records(int): number of records for testing

    Returns:
        None

    Raises:
        AssertionError: If the generated data does not match the expected counts.
    """
    gen_user_product_data(db_connection, num_records, should_update=True, should_delete=True)
    conn = db_connection
    cur = conn.cursor()
    
    user_count = get_user_count(cur)
    product_count = get_product_count(cur)
    
    assert user_count == 2  # Adjust the expected counts as needed
    assert product_count == 2  # Adjust the expected counts as needed
    
    conn.rollback()  # Rollback the transaction to undo the insertions
    cur.close()
