import requests
import time
import csv
from bs4 import BeautifulSoup

# Base URL for fetching pages
base_url = "https://www.find-tender.service.gov.uk/Search/Results?page="

# Function to fetch and parse a page
def fetch_page(page_num):
    url = f"{base_url}{page_num}"
    response = requests.get(url)
    
    if response.status_code == 200:
        print(f"Fetched page {page_num} successfully.")
        return response.text
    else:
        print(f"Failed to fetch page {page_num} with status code {response.status_code}")
        return None

# Function to extract data from the page
def extract_data(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    results = []
    
    # Update the selectors based on the actual structure of the website
    notices = soup.find_all('div', class_='card')  # Adjust class name as needed
    for notice in notices:
        title = notice.find('h2').text.strip() if notice.find('h2') else 'No title'
        description = notice.find('p').text.strip() if notice.find('p') else 'No description'
        published_date = notice.find('time').text.strip() if notice.find('time') else 'No date'
        awarded_value = notice.find('span', class_='value').text.strip() if notice.find('span', class_='value') else 'No value'
        awarded_supplier = notice.find('span', class_='supplier').text.strip() if notice.find('span', class_='supplier') else 'No supplier'
        
        results.append({
            'title': title,
            'description': description,
            'published_date': published_date,
            'awarded_value': awarded_value,
            'awarded_supplier': awarded_supplier
        })
        
    return results

# Function to save results to a CSV file
def save_to_csv(data, filename):
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    print(f"Saved {len(data)} results to {filename}.")

# Main script to iterate through pages and collect data
all_results = []
for page in range(1, 3):  # Example: scrape the first 2 pages for testing
    print(f"Fetching page {page}...")
    page_content = fetch_page(page)
    if page_content:
        print(page_content[:1000])  # Print the first 1000 characters of the page content for inspection
        results = extract_data(page_content)
        all_results.extend(results)
        time.sleep(1)  # Add a delay to be respectful to the server

# Save all results to a CSV file
if all_results:
    save_to_csv(all_results, filename='results.csv')
else:
    print("No data to save.")
