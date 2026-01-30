import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from pymongo import MongoClient
import joblib
import redis
import json
import pickle
from fastapi import FastAPI, Form
import hashlib
from fastapi.middleware.cors import CORSMiddleware
api=FastAPI(title="Bank fraud detection api")
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all (safe for dev & college project)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("fraud_model.pkl")
encoder = joblib.load("type_encoder.pkl")
mongo_client = MongoClient("mongodb://localhost:27017",
    serverSelectionTimeoutMS=5000
)
db=mongo_client["cscorner"]
collection=db["sample"]
redis_client= redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)
@api.get("/")
def root():
    return{"status":"Backend running successfully"}
@api.post("/predict")
def predict(
    step:int=Form(...),
    type:str=Form(...),
    amount: float=Form(...),
    olbalanceOrg: float=Form(...),
    newbalanceOrg: float=Form(...),
    oldbalanceDest: float=Form(...),
    newbalanceDest: float=Form(...),
):
    encoded_type = int(encoder.transform([type])[0])

    transaction ={
        "step":step,
        "type":encoded_type,
        "amount":amount,
        "oldbalanceOrg":olbalanceOrg,
        "newbalanceOrg":newbalanceOrg,
        "oldbalanceDest":oldbalanceDest,
        "newbalanceDest":newbalanceDest,
    }
    cache_key = "pred:" + hashlib.md5(
        json.dumps(transaction, sort_keys=True).encode()
    ).hexdigest()

    cached = redis_client.get(cache_key)
    if cached:
        return {
            "source": "redis",
            "fraud": int(cached)
        }


    prediction = model.predict([list(transaction.values())])[0]

  
    redis_client.setex(cache_key, 3600, int(prediction))

    return {
        "source": "model",
        "fraud": int(prediction)
    }


@api.get("/stats")
def stats():
    cache_key = "transaction_stats"

    cached = redis_client.get(cache_key)
    if cached:
        return {
            "source": "redis",
            "data": json.loads(cached)
        }

    total = collection.count_documents({})
    fraud = collection.count_documents({"isFraud": 1})

    data = {
        "total_transactions": total,
        "fraud_transactions": fraud,
        "fraud_ratio": round(fraud / total, 6)
    }

    redis_client.setex(cache_key, 600, json.dumps(data))

    return {
        "source": "mongodb",
        "data": data
    }


