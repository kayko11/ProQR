from flask import Flask, request, Response
from pymongo import MongoClient
import requests
import os

app = Flask(__name__)

# Set the target API endpoint
api_endpoint = 'http://www.contractsfinder.service.gov.uk'

# Connect to the MongoDB database
client = MongoClient("mongodb://0.0.0.0:27017/")
db = client["mydatabase"]
collection = db["mycollection"]

# Basic auth
username = os.environ.get("API_USER")
password = os.environ.get("API_KEY")


@app.route('/', defaults={'path': ''}, methods=['POST', 'GET'])
@app.route('/<path:path>', methods=['POST', 'GET'])
def reroute(path):
    if username and password:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {username}:{password}'
        }
    else:
        headers = {'Content-Type': 'application/json'}

    # Send request to external api
    api_response = requests.request(
        method=request.method,
        url=api_endpoint + '/' + path,headers=headers,
        json=request.json
    )

    try:
        # insert response data into MongoDB
        collection.insert_one(api_response.json())
        print("Data stored successfully")
    except Exception as e:
        print("Error storing data")
        print(e)

    # Return the response
    return Response(
        api_response.text,
        status=api_response.status_code,
        mimetype='application/json'
    )

if __name__ == '__main__':
    app.run()

