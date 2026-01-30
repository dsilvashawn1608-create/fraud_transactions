from pymongo import MongoClient
import random

client = MongoClient('mongodb://localhost:27017')
db = client['cscorner']
collection = db['sample']

# Remove existing docs to keep this deterministic for testing
collection.delete_many({})

types = ['CASH_IN', 'CASH_OUT', 'DEBIT', 'PAYMENT', 'TRANSFER']

docs = []
random.seed(42)
for i in range(1, 51):
    t = random.choice(types)
    amount = round(random.uniform(1, 10000), 2)
    old_org = round(random.uniform(0, 20000), 2)
    new_org = max(0.0, old_org - amount if random.random() < 0.7 else old_org)
    old_dest = round(random.uniform(0, 20000), 2)
    new_dest = max(0.0, old_dest + amount if random.random() < 0.7 else old_dest)
    # Make some frauds: large amounts with TRANSFER or CASH_OUT
    is_fraud = 1 if (amount > 9000 and t in ('TRANSFER', 'CASH_OUT')) else 0

    doc = {
        'step': i,
        'type': t,
        'amount': amount,
        'oldbalanceOrg': old_org,
        'newbalanceOrig': new_org,
        'oldbalanceDest': old_dest,
        'newbalanceDest': new_dest,
        'isFraud': is_fraud
    }
    docs.append(doc)

collection.insert_many(docs)
print(f'Inserted {len(docs)} sample documents into cscorner.sample')
