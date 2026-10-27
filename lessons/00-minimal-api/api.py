# The smallest useful FastAPI app: three routes, no extras.
#
# Run it:      python api.py
# Try it:      http://127.0.0.1:8000/docs   (FastAPI builds this test page for you)

import json
from datetime import datetime

import uvicorn
from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI()

client = MongoClient("mongodb://localhost:27017")
db = client["classroom"]


# Route 1: read a local file and return it.
# A Python list becomes a JSON array automatically.
@app.get("/api/countries")
def get_countries():
    with open("countries.json") as f:
        return json.load(f)


# Route 2: read documents from MongoDB.
# The projection {"first_name": 1, ...} asks Mongo for only those fields.
@app.get("/api/users")
def get_local_users():
    with open("sample_users.json") as f:
        return json.load(f)


#   {
#     _id: 20,
#     customer_id: 20,
#     card_id: 20,
#     product_id: 379,
#     department: 'Outdoors',
#     amount: Decimal128('19.99'),
#     purchase_date: ISODate('2025-11-19T00:00:00.000Z'),
#     product_name: "Kids' Dinosaur-Themed Lunchbox",
#     state_code: 'CA',
#     card_type: 'switch'
#   }


# Route 2: read documents from MongoDB.
# The projection {"first_name": 1, ...} asks Mongo for only those fields.
@app.get("/api/mongo/purchases")
def get_purchases():
    purchases = []
    for doc in db.purchases.find(
        {}, {"amount": 1, "product_name": 1, "product_id": 1, "_id": 0}
    ).sort("product_id", 1):
        purchases.append(
            doc
        )  # _id is an int in this database, so the doc is already JSON-friendly
    return purchases


@app.get("/api/mongo/users")
def get_users():
    users = []
    for doc in db.customers.find(
        {}, {"first_name": 1, "last_name": 1, "email": 1}
    ).limit(10):
        users.append(
            doc
        )  # _id is an int in this database, so the doc is already JSON-friendly
    return users


# Route 3: add a purchase to MongoDB.
# Annotating the parameter as `dict` tells FastAPI to read it from the JSON request body.
@app.post("/api/purchases")
def add_purchase(purchase: dict):
    # Ask the counters collection for the next purchase id (it adds 1 and hands back the result).
    counter = db.counters.find_one_and_update(
        {"_id": "purchase_id"}, {"$inc": {"seq": 1}}, return_document=True
    )
    purchase["_id"] = counter["seq"]
    purchase["purchase_date"] = datetime.now()

    db.purchases.insert_one(purchase)
    return {"message": "purchase added", "purchase_id": purchase["_id"]}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
