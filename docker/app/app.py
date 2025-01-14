from flask import Flask, request, jsonify, Response
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

@app.route('/proxy/<path:subpath>', methods=['GET'])
def proxy(subpath):
    target_url = f"{API_BASE_URL}/{subpath}"
    params = request.args
    
    try:
        resp = requests.get(target_url, params=params, allow_redirects=False)
    except requests.RequestException as e:
        return Response(f"Proxy Error: {e}", status=500)
    
    return Response(resp.content, resp.status_code, resp.headers.items())

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
