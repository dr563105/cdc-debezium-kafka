import psycopg2
import argparse
from time import sleep
import random
from faker import Faker

Faker.seed(42)
fake = Faker()

def gen_user_product_data(num_records: int) -> None:
    for id in range(num_records):
        sleep(0.5)
        conn = psycopg2.connect(
            "dbname='postgres' user='postgres' host='postgres' password='postgres'"
        )
        curr = conn.cursor()
        curr.execute(
            f"INSERT INTO \
                commerce.users (id, username, email_address) \
                VALUES ({id}, {fake.user_name()}, {fake.email()})"
        )
        curr.execute(
            f"INSERT INTO \
                commerce.products (id, name, description, price) \
                VALUES ({id}, {fake.name()}, {fake.text()}, {fake.random_int(min=1, max=100)})"
        )
        conn.commit()

        sleep(0.5)
        # update 10 % of the time
        if random.randint(1, 100) >= 90:
            curr.execute(
                f"UPDATE commerce.users \
                    SET username = {fake.user_name()} \
                    WHERE id = {id}"
            )
            curr.execute(
                f"UPDATE commerce.products \
                    SET name = {fake.name()} \
                    WHERE id = {id}"
            )
        conn.commit()

        sleep(0.5)
        # delete 5 % of the time
        if random.randint(1, 100) >= 95:
            curr.execute(f"DELETE FROM commerce.users WHERE id = {id}")
            curr.execute(f"DELETE FROM commerce.products WHERE id = {id}")

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
        default=1000,
    )
    args = parser.parse_args()
    num_records = args.num_records
    gen_user_product_data(num_records)

