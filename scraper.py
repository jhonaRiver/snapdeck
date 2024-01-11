#!/usr/bin/env python3

from requests_html import HTMLSession
from bs4 import BeautifulSoup

# Create an HTML session
session = HTMLSession()

# Define the URL of the website
url = 'https://marvelsnapzone.com/cards/'

# Send a GET request and render the HTML content
response = session.get(url)
response.html.render()

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(response.html.html, 'html.parser')

# Find the HTML elements that contain card information
card_list = soup.find_all('div', class_='cardname')

# Iterate through card elements and extract relevant data
for card in card_list:
    # Extract card attributes (e.g., name, type, mana cost, etc.)
    card_name = card.text
    print(card_name)
# card_type = card.find('span', class_='card-type').text
# mana_cost = card.find('span', class_='mana-cost').text

# Process and store the extracted data as needed
# You can save it to a file, database, or data structure

# Close the HTML session
session.close()
