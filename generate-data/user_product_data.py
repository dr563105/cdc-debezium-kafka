import psycopg2
import argparse
from time import sleep
import random
from faker import Faker
import os

Faker.seed(42)
fake = Faker()

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "cdc-demo-db")
POSTGRES_HOSTNAME = os.getenv("POSTGRES_HOST", "postgres")


def gen_user_product_data(num_records: int) -> None:
    # connection = (f"dbname={POSTGRES_DB} user={POSTGRES_USER} password={POSTGRES_PASSWORD} host={POSTGRES_HOSTNAME}")
    for id in range(num_records):
        id +=1
        sleep(0.5)
        conn = psycopg2.connect(database=f'{POSTGRES_DB}',
                                user=f'{POSTGRES_USER}',
                                password=f'{POSTGRES_PASSWORD}',
                                host=f'{POSTGRES_HOSTNAME}')
        curr = conn.cursor()
        curr.execute(
            f"INSERT INTO \
                commerce.users (id, username, email_address) \
                VALUES (%s, %s, %s)", (id, fake.user_name(), fake.email())
        )
        curr.execute(
            f"INSERT INTO \
                commerce.products (id, name, description, price) \
                VALUES (%s, %s, %s, %s)", (id, fake.name(), fake.text(), (fake.random_int(min=1, max=999))/100)
        )
        conn.commit()

        sleep(0.5)
        # update 10 % of the time
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

        sleep(0.5)
        # delete 5 % of the time
        if random.randint(1, 100) >= 95:
            curr.execute("DELETE FROM commerce.users WHERE id = %s",(id,))
            curr.execute("DELETE FROM commerce.products WHERE id = %s", (id,))

        conn.commit()
        curr.close()

    return


if __name__ == "__main__":
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

