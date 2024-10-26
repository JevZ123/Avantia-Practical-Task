from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# TODO: add proper configuration
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
DATABASE_NAME = os.getenv("DATABASE_NAME", "default")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "laureates")
mongo_client = MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}/")
db = mongo_client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

@app.route('/search', methods=['GET'])
def query_laureates():

    print(request)

    # separate queries, but can be combined in the future if needed
    year = request.args.get('year')
    description = request.args.get('description')
    category = request.args.get('category')
    name = request.args.get('name')

    query = {}

    if year:
        query["year"] = year
    if description:
        query["description"] = {"$regex": description, "$options": "i"}
    if description:
        query["category"] = {"$regex": category, "$options": "i"}
    if description:
        query["name"] = {"$regex": name, "$options": "i"}

    results = list(collection.find(query))

    return jsonify(results)

if __name__ == '__main__':
    app.run()
