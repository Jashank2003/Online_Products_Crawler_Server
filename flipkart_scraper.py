from bs4 import BeautifulSoup
import requests
import json
import sys

# Define the URL of the page you want to scrape
if len(sys.argv) < 2:
    print("Usage: python flipkart_scraper.py <product_name>")
    sys.exit(1)

product_name = sys.argv[1]
print(product_name)
url = f'https://www.flipkart.com/search?q={product_name}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off'
base_path = 'https://www.flipkart.com'

# Send an HTTP request to the URL
response = requests.get(url)
html_text = response.content

# Parse the HTML content
soup = BeautifulSoup(html_text, 'html.parser')
print(response.status_code)

data = {"data": []}  # Initialize data dictionary with 'data' key as a list

containers = soup.find_all('a', '_1fQZEK')
for container in containers:
    item_data = {}

    title_element = container.find('div', '_4rR01T')
    price_element = container.find('div', '_30jeq3 _1_WHN1')
    image_element = container.find('img', '_396cs4')
    link_element = container.get('href')

    item_data['title'] = title_element.get_text() if title_element else "Title not found"
    
    # Extract price text and remove the rupee symbol
    price_text = price_element.get_text() if price_element else "Price not found"
    item_data['price'] = price_text.replace('₹', '').replace(',', '')  # Remove the rupee symbol and commas
    
    item_data['image_link'] = image_element['src'] if image_element else "Image not found"
    item_data['link_to_product'] =link_element if link_element else "Link not found"

    data["data"].append(item_data)  # Append the item_data to the 'data' list in the data dictionary

# Write the data to output.json
with open('output2.json', 'w') as f:
    json.dump(data, f, indent=4)

print("Data written to output2.json")
