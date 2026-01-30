from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
db = client['cscorner']
collection = db['sample']

docs = []
for i in range(51, 71):
    doc = {
        'step': i,
        'type': 'TRANSFER',
        'amount': 15000.0,
        'oldbalanceOrg': 20000.0,
        'newbalanceOrig': 5000.0,
        'oldbalanceDest': 1000.0,
        'newbalanceDest': 16000.0,
        'isFraud': 1
    }
    docs.append(doc)

collection.insert_many(docs)
print(f'Inserted {len(docs)} fraud documents')
