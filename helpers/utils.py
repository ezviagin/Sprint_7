from faker import Faker
import random


def generate_order_data(color: list = ''):
    fake = Faker()

    order_body = {
        "name": fake.first_name(),
        "lastName": fake.last_name(),
        "address": fake.address(),
        "metroStation": random.randint(1, 30),
        "phone": fake.phone_number(),
        "rentTime": random.randint(1, 7),  # between 1 and 7 days
        "deliveryDate": fake.date_between(start_date="today", end_date="+2y").strftime('%Y-%m-%d'),
        "comment": fake.sentence()
    }
    if color:
        order_body["color"] = color

    return order_body
