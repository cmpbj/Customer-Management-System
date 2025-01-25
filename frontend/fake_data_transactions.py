import random
from faker import Faker
import pandas as pd

# Initialize Faker
fake = Faker()

# Number of transactions per customer
TRANSACTIONS_PER_CUSTOMER = 10

# Function to generate fake transactions
def generate_fake_transactions():
    # Prepare transactions
    transactions = []
    for customer_id in range(101):  # Customer IDs from 0 to 100
        for _ in range(TRANSACTIONS_PER_CUSTOMER):
            transaction_date = fake.date_time_between(start_date="-1y", end_date="now")
            amount = round(random.uniform(10.0, 1000.0), 2)
            transactions.append({
                "customer_id": customer_id,
                "transaction_date": transaction_date,
                "amount": amount
            })

    # Create a DataFrame from the transactions
    df = pd.DataFrame(transactions)
    return df
