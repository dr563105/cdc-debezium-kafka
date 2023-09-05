import random
from faker import Faker
import os
import psycopg2
from psycopg2.extensions import cursor
from typing import Dict, Any

Faker.seed(42)
fake = Faker()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOSTNAME = os.getenv("POSTGRES_HOST")
POSTGRES_DB = os.getenv("POSTGRES_DB")
SCHEMA = os.getenv("DB_SCHEMA")


def generate_user_data(id: int) -> Dict[str, Any]:
    """
    Generate user data.

    Args:
        id (int): The user's ID.

    Returns:
        Dict[str, Any]: A dictionary containing user data.
    """
    return {
        "id": id,
        "username": fake.user_name(),
        "email_address": fake.email(),
    }

def generate_product_data(id: int) -> Dict[str, Any]:
    """
    Generate product data.

    Args:
        id (int): The product's ID.

    Returns:
        Dict[str, Any]: A dictionary containing product data.
    """
    return {
        "id": id,
        "name": fake.name(),
        "description": fake.text(),
        "price": round(fake.random_int(min=1, max=999_999) / 100.0, 2),
    }

def insert_user_data(conn: str, cur: cursor, user_data: Dict[str, Any]) -> None:
    """
    Insert user data into the database.

    Args:
        conn (str): The database connection.
        cur (cursor): The database cursor.
        user_data (Dict[str, Any]): User data to be inserted.

    Returns:
        None
    """
    try:
        cur.execute(
            f"INSERT INTO {SCHEMA}.users (id, username, email_address) VALUES (%s, %s, %s)",
            (user_data['id'], user_data['username'], user_data['email_address'])
        )
    except psycopg2.IntegrityError as e:
        # Handle any database integrity errors (e.g., unique constraint violations) here
        conn.rollback()  # Rollback the transaction to avoid committing the changes
        raise e  # Re-raise the exception for the test to handle
    else:
        conn.commit()  # Commit the transaction if there are no errors

def insert_product_data(conn: str, cur: cursor, product_data: Dict[str, Any]) -> None:
    """
    Insert product data into the database.

    Args:
        conn (str): The database connection.
        cur (cursor): The database cursor.
        product_data (Dict[str, Any]): Product data to be inserted.

    Returns:
        None
    """
    try:
        cur.execute(
            f"INSERT INTO {SCHEMA}.products (id, name, description, price) VALUES (%s, %s, %s, %s)",
            (product_data['id'], product_data['name'], product_data['description'], product_data['price'])
        )
    except psycopg2.IntegrityError as e:
        # Handle any database integrity errors (e.g., unique constraint violations) here
        conn.rollback()  # Rollback the transaction to avoid committing the changes
        raise e  # Re-raise the exception for the test to handle
    else:
        conn.commit()  # Commit the transaction if there are no errors

def update_records(conn: str, cur: cursor, user_data: Dict[str, Any], product_data: Dict[str, Any]) -> None:
    """
    Update user and product records in the database with 10% probability

    Args:
        conn (str): The database connection.
        cur (cursor): The database cursor.
        user_data (Dict[str, Any]): User data to be updated.
        product_data (Dict[str, Any]): Product data to be updated.

    Returns:
        None
    """
    try:
        if random.randint(1, 100) >= 90:
            new_username = fake.user_name()
            new_name = fake.name()

            cur.execute(
                f"UPDATE {SCHEMA}.users SET username = %s WHERE id = %s",
                (new_username, user_data["id"])
            )
            cur.execute(
                f"UPDATE {SCHEMA}.products SET name = %s WHERE id = %s",
                (new_name, product_data["id"])
            )
    except psycopg2.IntegrityError as e:
        # Handle any database integrity errors (e.g., unique constraint violations) here
        conn.rollback()  # Rollback the transaction to avoid committing the changes
        raise e  # Re-raise the exception for the test to handle
    else:
        conn.commit()

def delete_records(conn: str, cur: cursor, user_data: Dict[str, Any], product_data: Dict[str, Any]) -> None:
    """
    Delete user and product records from the database with 5% probability.

    Args:
        conn (str): The database connection.
        cur (cursor): The database cursor.
        user_data (Dict[str, Any]): User data to be deleted.
        product_data (Dict[str, Any]): Product data to be deleted.

    Returns:
        None
    """
    try:
        if random.randint(1, 100) >= 95:
            cur.execute(
                f"DELETE FROM {SCHEMA}.users WHERE id = %s",
                (user_data["id"],)
            )
            cur.execute(
                f"DELETE FROM {SCHEMA}.products WHERE id = %s",
                (product_data["id"],)
            )
    except psycopg2.IntegrityError as e:
        # Handle any database integrity errors (e.g., unique constraint violations) here
        conn.rollback()  # Rollback the transaction to avoid committing the changes
        raise e  # Re-raise the exception for the test to handle 
    else:
        conn.commit()

def gen_user_product_data(num_records: int) -> None: 
    """
    Generate user and product data, and interact with the database.

    Args:
        num_records (int): Number of records to generate.

    Returns:
        Dict[int, Dict[str, Any]]: A dictionary containing generated user and product data.
    """
    # user_product_data = {}
    with psycopg2.connect(
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOSTNAME
    ) as conn:
        cur = conn.cursor()

        for id in range(1, num_records + 1):
            user_data = generate_user_data(id)
            product_data = generate_product_data(id)
            # user_product_data[id] = {"user": user_data, "product": product_data}
            
            # Insert user and product data into the database
            insert_user_data(conn, cur, user_data)
            insert_product_data(conn, cur, product_data)

            # Update and delete records
            update_records(conn, cur, user_data, product_data)
            delete_records(conn, cur, user_data, product_data)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n",
        "--num_records",
        type=int,
        help="Number of records to generate",
        default=100_000,
    )
    args = parser.parse_args()
    num_records = args.num_records
    gen_user_product_data(num_records)
