import requests
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_date_ranges(start_date, end_date, interval_months=6):
    """Generate date ranges with the specified interval in months."""
    current_start_date = start_date
    date_ranges = []
    
    while current_start_date < end_date:
        current_end_date = min(current_start_date + timedelta(days=interval_months*30), end_date)
        date_ranges.append((current_start_date, current_end_date))
        current_start_date = current_end_date + timedelta(days=1)
    
    return date_ranges

# Define the date ranges for the intervals
start_date = datetime(2014, 1, 1)
end_date = datetime(2024, 8, 3)
date_ranges = generate_date_ranges(start_date, end_date)

# Define the API endpoint and parameters
url = 'https://www.contractsfinder.service.gov.uk/api/rest/2/search_notices/json'
headers = {'Content-Type': 'application/json'}

# Initialize an empty DataFrame to collect all results
all_data = pd.DataFrame()

for start, end in date_ranges:
    logger.info(f"Fetching data from {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}")
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
            "valueTo": 600000000000.0,
            "publishedFrom": start.strftime('%Y-%m-%d'),
            "publishedTo": end.strftime('%Y-%m-%d'),
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
        "size": 1000
    }

    try:
        # Fetch data from the API with a timeout
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()  # Ensure we notice bad responses
        data = response.json()
        
        if 'noticeList' not in data or not data['noticeList']:
            logger.info(f"No data found for range {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}")
            continue

        # Convert the JSON data to a DataFrame
        df = pd.json_normalize(data['noticeList'], sep='_')

        # Append the data to the all_data DataFrame
        all_data = pd.concat([all_data, df], ignore_index=True)
        logger.info(f"Data fetched for range {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed for range {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}: {e}")
    except ValueError as e:
        logger.error(f"Error processing data for range {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}: {e}")

# Connect to the MariaDB database using SQLAlchemy
db_url = 'mysql+pymysql://root:admin@localhost:3306/mydb'
engine = create_engine(db_url)

# Load data into the database
try:
    all_data.to_sql('notices', engine, if_exists='replace', index=False)
    logger.info("Data successfully loaded into the database.")
except Exception as e:
    logger.error(f"Failed to load data into the database: {e}")
