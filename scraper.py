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
card_names = soup.find_all('div', class_='cardname')
card_tags = soup.find_all('span', class_='tag-item')
card_descriptions = soup.find_all('div', class_='card-description')

# Iterate through card elements and extract relevant data
for name in card_names:
    card_name = name.text

for tag in card_tags:
    tag_text = tag.text.strip().lower()
    if tag_text != 'none' and tag_text != 'unreleased':
        card_tag = tag.text

for description in card_descriptions:
    card_description = description.text

# Process and store the extracted data as needed
# You can save it to a file, database, or data structure

# Close the HTML session
session.close()
