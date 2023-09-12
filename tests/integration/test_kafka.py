import json
from kafka import KafkaConsumer
import pytest
import psycopg2
import os

# Constants
KAFKA_TOPIC_PRODUCTS = "test_debezium.commerce.products" 
KAFKA_TOPIC_USERS = "test_debezium.commerce.users"
TEST_POSTGRES_USER = os.getenv("TEST_POSTGRES_USER")
TEST_POSTGRES_PASSWORD = os.getenv("TEST_POSTGRES_PASSWORD")
TEST_POSTGRES_HOSTNAME = os.getenv("TEST_POSTGRES_HOST")
TEST_POSTGRES_DB = os.getenv("TEST_POSTGRES_DB")
SCHEMA = os.getenv("DB_SCHEMA", "commerce")


@pytest.fixture(scope="module")
def get_db_connection():
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


@pytest.fixture(scope="module")
def get_consumer_products():
    """
    Fixture to create a Kafka consumer for the products topic.

    This fixture establishes a Kafka consumer for the 'test_debezium.commerce.products'
    topic and yields the consumer object. After the test function that uses this consumer is
    executed, the consumer is closed.

    Returns:
        kafka.KafkaConsumer: The Kafka consumer for products.
    """
    consumer_products = KafkaConsumer(
        KAFKA_TOPIC_PRODUCTS,
        bootstrap_servers=['kafka:9092'],
        auto_offset_reset="earliest",
        consumer_timeout_ms=1000
    )
    yield consumer_products
    consumer_products.close()


@pytest.fixture(scope="module")
def get_consumer_users():
    """
    Fixture to create a Kafka consumer for the users topic.

    This fixture establishes a Kafka consumer for the 'test_debezium.commerce.users'
    topic and yields the consumer object. After the test function that uses this consumer is
    executed, the consumer is closed.

    Returns:
        kafka.KafkaConsumer: The Kafka consumer for users.
    """
    consumer_users = KafkaConsumer(
        KAFKA_TOPIC_USERS,
        bootstrap_servers=['kafka:9092'],
        auto_offset_reset="earliest",
        consumer_timeout_ms=1000
    )
    yield consumer_users
    consumer_users.close()


def test_bootstrap_connection(get_consumer_products, get_consumer_users):
    """
    Test function to check if the Kafka consumers are able to establish a connection.

    Args:
        get_consumer_products (kafka.KafkaConsumer): Kafka consumer for products.
        get_consumer_users (kafka.KafkaConsumer): Kafka consumer for users.
    """
    assert get_consumer_products.bootstrap_connected()
    assert get_consumer_users.bootstrap_connected()


def test_topic_name(get_consumer_products, get_consumer_users):
    """
    Test function to verify if the Kafka consumers have subscribed to the correct topics.

    Args:
        get_consumer_products (kafka.KafkaConsumer): Kafka consumer for products.
        get_consumer_users (kafka.KafkaConsumer): Kafka consumer for users.
    """
    assert get_consumer_products.subscription() == {KAFKA_TOPIC_PRODUCTS}
    assert get_consumer_users.subscription() == {KAFKA_TOPIC_USERS}


def test_total_transactions(get_consumer_users, get_consumer_products):
    """
    Test function to ensure that both consumers receive the expected number of transactions.

    Args:
        get_consumer_users (kafka.KafkaConsumer): Kafka consumer for users.
        get_consumer_products (kafka.KafkaConsumer): Kafka consumer for products.
    """
    lsn_u=[]
    lsn_p=[]
    for msg in get_consumer_users:
        if msg.value:
            json_object = json.loads(msg.value)
            lsn_u.append(json_object['payload']['source']['lsn'])

    for msg in get_consumer_products:
        if msg.value:
            json_object = json.loads(msg.value)
            lsn_p.append(json_object['payload']['source']['lsn'])

    assert len(lsn_u) == 35
    assert len(lsn_p) == 35


def test_username_present(get_db_connection):
    """
    Test function to check if usernames received from Kafka are present in the database.

    Args:
        get_db_connection (psycopg2.extensions.connection): Database connection.
    """
    usernames =[]

    # For some reason KafkaConsumer doesn't work through module function
    consumer_users = KafkaConsumer(
        KAFKA_TOPIC_USERS,
        bootstrap_servers=['kafka:9092'],
        auto_offset_reset="earliest",
        consumer_timeout_ms=1000
    )
    for msg in consumer_users:
        if msg.value:
            json_object = json.loads(msg.value)
            if json_object['payload']['after']:
                usernames.append(json_object['payload']['after']['username'])

    consumer_users.close()
    cur = get_db_connection.cursor()
    cur.execute(f"SELECT username FROM {SCHEMA}.users")
    result = cur.fetchone()[0]

    assert result in usernames
