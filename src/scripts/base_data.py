import datetime
import random

from faker import Faker
import psycopg2
import psycopg2.extras

import uuid
from random import choice

import settings

faker = Faker()
psycopg2.extras.register_uuid()

districts_list = [['d1', 'd2'], ['d2', 'd3'], ['d1', 'd3']]

couriers_dct = {}


def generate_couriers():
    conn = psycopg2.connect(
        f"host={settings.POSTGRES_HOST} port={settings.POSTGRES_PORT} "
        f"dbname={settings.POSTGRES_DB_NAME} user={settings.POSTGRES_USERNAME} password={settings.POSTGRES_PASSWORD}")
    conn.autocommit = True
    cur = conn.cursor()

    for _ in range(3):
        sid = uuid.uuid4()
        districts = choice(districts_list)
        couriers_dct[sid] = districts
        query = (f"INSERT INTO couriers (sid, name, districts) "
                 f"VALUES ('{sid}', '{faker.name()}', ARRAY{districts});")

        cur.execute(query)
    conn.commit()


def generate_orders():
    conn = psycopg2.connect(
        f"host={settings.POSTGRES_HOST} port={settings.POSTGRES_PORT} "
        f"dbname={settings.POSTGRES_DB_NAME} user={settings.POSTGRES_USERNAME} password={settings.POSTGRES_PASSWORD}")
    conn.autocommit = True
    cur = conn.cursor()

    try:
        for courier_sid, districts in couriers_dct.items():
            order_sid = uuid.uuid4()
            cur.execute(
                f"INSERT INTO orders (sid, name, district, status, courier_sid, created_at) "
                f"VALUES ('{order_sid}', '{faker.word()}', '{choice(districts)}', 'in_progress', '{courier_sid}', "
                f"'{datetime.datetime.now() - datetime.timedelta(hours=random.randint(1, 10))}');"
            )

            # add order_sid to courier
            cur.execute(
                f"UPDATE couriers SET order_sid = '{order_sid}' WHERE sid = '{courier_sid}';"
            )

        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")

    conn.commit()


if __name__ == "__main__":
    generate_couriers()
    generate_orders()
