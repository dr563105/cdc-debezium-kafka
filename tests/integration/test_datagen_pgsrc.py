from user_product_data import *
import pytest
import psycopg2
import os

TEST_POSTGRES_USER = os.getenv("TEST_POSTGRES_USER")
TEST_POSTGRES_PASSWORD = os.getenv("TEST_POSTGRES_PASSWORD")
TEST_POSTGRES_HOSTNAME = os.getenv("TEST_POSTGRES_HOST")
TEST_POSTGRES_DB = os.getenv("TEST_POSTGRES_DB")
SCHEMA = os.getenv("DB_SCHEMA")


@pytest.fixture(scope="module")
def db_connection():
    conn = psycopg2.connect(
        database=TEST_POSTGRES_DB,
        user=TEST_POSTGRES_USER,
        password=TEST_POSTGRES_PASSWORD,
        host=TEST_POSTGRES_HOSTNAME
    )
    yield conn
    conn.close()

@pytest.fixture(scope="module")
def faker_instance():
    # Create a Faker instance with the same seed as in your main script
    Faker.seed(42)
    fake = Faker()
    return fake

def test_insert_user_data(db_connection, faker_instance):
    user_data = generate_user_data(1)
    conn = db_connection
    cur = conn.cursor()
    insert_user_data(conn, cur, user_data)
    cur.execute(f"SELECT * FROM {SCHEMA}.users WHERE id = {user_data['id']}")
    inserted_user_data = cur.fetchone()
    cur.close()
    
    assert inserted_user_data is not None

def test_insert_product_data(db_connection, faker_instance):
    product_data = generate_product_data(1)
    conn = db_connection
    cur = conn.cursor()
    insert_product_data(conn, cur, product_data)
    cur.execute(f"SELECT * FROM {SCHEMA}.products WHERE id = {product_data['id']}")
    inserted_product_data = cur.fetchone()
    cur.close()
    
    assert inserted_product_data is not None

def test_update_records(db_connection, faker_instance):
    user_data = generate_user_data(2)
    product_data = generate_product_data(2)
    conn = db_connection
    cur = conn.cursor()
    insert_user_data(conn, cur, user_data)
    insert_product_data(conn, cur, product_data)
    
    update_records(conn, cur, user_data, product_data)
    
    cur.execute(f"SELECT username FROM {SCHEMA}.users WHERE id = {user_data['id']}")
    updated_username = cur.fetchone()[0]
    cur.execute(f"SELECT name FROM {SCHEMA}.products WHERE id = {product_data['id']}")
    updated_name = cur.fetchone()[0]
    
    assert updated_username != user_data['username']
    assert updated_name != product_data['name']
    
    conn.rollback()  # Rollback the transaction to undo the update
    cur.close()

def get_user_count(cur):
    cur.execute(f"SELECT COUNT(*) FROM {SCHEMA}.users")
    return cur.fetchone()[0]

def get_product_count(cur):
    cur.execute(f"SELECT COUNT(*) FROM {SCHEMA}.products")
    return cur.fetchone()[0]

def test_delete_records(db_connection, faker_instance):
    user_data = generate_user_data(3)
    product_data = generate_product_data(3)
    conn = db_connection
    cur = conn.cursor()
    insert_user_data(conn, cur, user_data)
    insert_product_data(conn, cur, product_data)

    initial_user_count = get_user_count(cur)
    initial_product_count = get_product_count(cur)
    
    delete_records(conn, cur, user_data, product_data)
    
    final_user_count = get_user_count(cur)
    final_product_count = get_product_count(cur)
    
    # Check if either user or product records are deleted
    assert (final_user_count >= initial_user_count) or (final_product_count >= initial_product_count)
    
    conn.rollback()  # Rollback the transaction to undo the deletion
    cur.close()

# def test_gen_user_product_data(db_connection):
#     num_records = 10
#     gen_user_product_data(num_records)
#     conn = db_connection
#     cur = conn.cursor()
    
#     user_count = get_user_count(cur)
#     product_count = get_product_count(cur)
    
#     assert user_count >= num_records
#     assert product_count >= num_records
    
#     conn.rollback()  # Rollback the transaction to undo the insertions
#     cur.close()
