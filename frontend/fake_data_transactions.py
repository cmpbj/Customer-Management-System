import random
from faker import Faker
import pandas as pd


fake = Faker()

TRANSACTIONS_PER_CUSTOMER = 10


def generate_fake_transactions():

    transactions = []
    for customer_id in range(101):
        for _ in range(TRANSACTIONS_PER_CUSTOMER):
            transaction_date = fake.date_time_between(start_date="-1y", end_date="now")
            amount = round(random.uniform(10.0, 1000.0), 2)
            transactions.append({
                "customer_id": customer_id,
                "transaction_date": transaction_date,
                "amount": amount
            })

    df = pd.DataFrame(transactions)
    return df
