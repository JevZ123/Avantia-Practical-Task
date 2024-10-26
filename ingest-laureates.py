from pymongo import MongoClient, ASCENDING
import json
import os

# TODO: reformat into a proper command line util with named arguments
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
DATABASE_NAME = os.getenv("DATABASE_NAME", "default")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "laureates")
FILE_PATH = os.getenv("FILE_PATH", "data.json")

client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

def ingest_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    documents = []
    for prize in data.get("prizes", []):
        year = prize.get("year")
        category = prize.get("category")

        for laureate in prize.get("laureates", []):
            document = {
                "year": year,
                "category": category,
                "firstname": laureate.get("firstname"),
                "lastname": laureate.get("surname"),
                "name" : f"{laureate.get('firstname')} {laureate.get('surname')}",
                "description": laureate.get("motivation"),
            }
            documents.append(document)

    collection.insert_many(documents)


def create_indices():
    collection.create_index([("year", ASCENDING)])
    collection.create_index([("category", ASCENDING)])
    collection.create_index([("name", ASCENDING)])
    collection.create_index([("description", ASCENDING)])

if __name__ == "__main__":
    ingest_data(FILE_PATH)
    create_indices()