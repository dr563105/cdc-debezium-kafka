import psycopg2
from psycopg2.extensions import cursor
import argparse
from time import sleep
import random
from faker import Faker
import os

Faker.seed(42)
fake = Faker()

POSTGRES_USER = os.getenv("POSTGRES_USER") #, "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD") #, "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB") #, "cdc-demo-db")
POSTGRES_HOSTNAME = os.getenv("POSTGRES_HOST") #, "postgres")


def insert_data(conn: str, curr: cursor , id: int) -> None:

    curr.execute(
            f"INSERT INTO \
                commerce.users (id, username, email_address) \
                VALUES (%s, %s, %s)", (id, fake.user_name(), fake.email())
        )
    curr.execute(
            f"INSERT INTO \
                commerce.products (id, name, description, price) \
                VALUES (%s, %s, %s, %s)", (id, fake.name(), fake.text(), (fake.random_int(min=1, max=999_999))/100.0)
        )
    conn.commit()

   
def update_records(conn: str, curr: cursor , id: int) -> None:
    if random.randint(1, 100) >= 90:
        curr.execute(
                "UPDATE commerce.users \
                    SET username = %s\
                    WHERE id = %s",(fake.user_name(), id)
            )
        curr.execute(
                "UPDATE commerce.products \
                    SET name = %s \
                    WHERE id = %s",(fake.user_name(), id)
            )
        conn.commit()

   
def delete_records(conn: str, curr: cursor , id: int) -> None:
    if random.randint(1, 100) >= 95:
        curr.execute("DELETE FROM commerce.users WHERE id = %s",(id,))
        curr.execute("DELETE FROM commerce.products WHERE id = %s", (id,))

        conn.commit()


def gen_user_product_data(num_records: int) -> None:
    # connection = (f"dbname={POSTGRES_DB} user={POSTGRES_USER} password={POSTGRES_PASSWORD} host={POSTGRES_HOSTNAME}")
    with psycopg2.connect(database=f'{POSTGRES_DB}',
                          user=f'{POSTGRES_USER}',
                          password=f'{POSTGRES_PASSWORD}',
                          host=f'{POSTGRES_HOSTNAME}') as conn:
        curr = conn.cursor()
        for id in range(1, num_records + 1):
            insert_data(conn, curr, id)
            sleep(0.3)
            # update 10 % of the time
            update_records(conn, curr, id)
            sleep(0.4)
            # delete 5 % of the time
            delete_records(conn, curr, id)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n",
        "--num_records",
        type=int,
        help="Number of records to generate",
        default=10_000,
    )
    args = parser.parse_args()
    num_records = args.num_records
    gen_user_product_data(num_records)
