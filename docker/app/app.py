from flask import Flask, request, jsonify
import requests
import os
from pymongo import MongoClient

app = Flask(__name__)

# Load environment variables
API_BASE_URL = os.getenv('API_BASE_URL', 'https://api.publicapis.org/entries')
MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_PORT = os.getenv('MONGO_PORT', '27017')
MONGO_USER = os.getenv('MONGO_USER', 'admin')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
DB_NAME = os.getenv('DB_NAME', 'admin')

# Construct MongoDB URI
MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/"

# MongoDB setup
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db['api_logs']
data_collection = db['test_data']

@app.route('/proxy', methods=['GET'])
def proxy():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is required."}), 400

    # Forward request to public API
    response = requests.get(API_BASE_URL, params={'title': query})

    if response.status_code == 200:
        data = response.json()
        # Log query to MongoDB
        collection.insert_one({"query": query, "response": data})
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to fetch data from the API."}), response.status_code

@app.route('/data', methods=['POST'])
def add_data():
    new_data = request.json
    if not new_data:
        return jsonify({"error": "No data provided."}), 400

    result = data_collection.insert_one(new_data)
    return jsonify({"message": "Data added successfully.", "id": str(result.inserted_id)})

@app.route('/data', methods=['GET'])
def get_data():
    data = list(data_collection.find({}, {"_id": 0}))
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
