import requests

# Function to fetch and parse a page
def fetch_page(page_num):
    url = f"https://www.find-tender.service.gov.uk/Search/Results?page=1"
    response = requests.get(url)
    
    if response.status_code == 200:
        print(f"Fetched page {page_num} successfully.")
        return response.text
    else:
        print(f"Failed to fetch page {page_num} with status code {response.status_code}")
        return None

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
    print(f"Saved {len(all_results)} results to results.csv.")
else:
    print("No data to save.")
