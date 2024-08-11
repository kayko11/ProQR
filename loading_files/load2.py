import requests
import pandas as pd
from sqlalchemy import create_engine

# Define the API endpoint and parameters
url = 'https://www.contractsfinder.service.gov.uk/api/rest/2/search_notices/json'
headers = {'Content-Type': 'application/json'}
payload = {
    "searchCriteria": {
        "types": ["Contract"],
        "statuses": ["Awarded"],
        "keyword": None,
        "queryString": None,
        "regions": None,
        "postcode": None,
        "radius": 0.0,
        "valueFrom": 10000000.0,
        "valueTo": 50000000000.0,
        "publishedFrom": "2020-01-01",
        "publishedTo": "2022-08-03",
        "deadlineFrom": None,
        "deadlineTo": None,
        "approachMarketFrom": None,
        "approachMarketTo": None,
        "awardedFrom": None,
        "awardedTo": None,
        "isSubcontract": None,
        "suitableForSme": None,
        "suitableForVco": None,
        "awardedToSme": None,
        "awardedToVcse": None,
        "cpvCodes": None
    },
    "size": 5000
}

# Fetch data from the API
response = requests.post(url, headers=headers, json=payload)
response.raise_for_status()  # Ensure we notice bad responses
data = response.json()

# Check the response structure
print(data)  # Optional: print the structure for verification

# Convert the JSON data to a DataFrame
# 'noticeList' contains the relevant information
df = pd.json_normalize(data['noticeList'], sep='_')

# Connect to the MariaDB database
engine = create_engine('mysql+pymysql://root:admin@localhost:3306/mydb')

# Load data into the database
df.to_sql('notices', engine, if_exists='replace', index=False)

print("Data successfully loaded into the database.")
