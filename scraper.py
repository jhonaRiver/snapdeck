#!/usr/bin/env python3

from requests_html import HTMLSession
from bs4 import BeautifulSoup

# TODO: Create class to store card information


class Card:
    def __init__(self, name, tag, description):
        self.name = name
        self.tag = tag
        self.description = description


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
card_elements = soup.find_all('div', class_='cards-list')
# card_names = soup.find_all('div', class_='cardname')
# card_tags = soup.find_all('span', class_='tag-item')
# card_descriptions = soup.find_all('div', class_='card-description')

# List to store card instances
cards = []

# Iterate through card elements and extract relevant data
for card in card_elements:
    card_name = card.find('div', class_='cardname')
    card_tag = card.find('span', class_='tag-item').text.strip().lower()
    card_description = card.find(
        'div', class_='card-description').text.strip().lower()
    if card_name and card_tag and card_description:
        name = card_name.text.strip().lower()
        tag = card_tag.text.strip().lower()
        description = card_description.text.strip().lower()
        if tag != 'none' and tag != 'unreleased':
            cards.append(Card(name, tag, description))
# for name in card_names:
#     card_name = name.text

# for tag in card_tags:
#     tag_text = tag.text.strip().lower()
#     if tag_text != 'none' and tag_text != 'unreleased':
#         card_tag = tag.text

# for description in card_descriptions:
#     card_description = description.text

# Close the HTML session
session.close()
