#!/usr/bin/env python3

from requests_html import HTMLSession
from bs4 import BeautifulSoup

# Create class to store card information


class Card:
    def __init__(self, name, tag, description, cost, power):
        self.name = name
        self.tag = tag
        self.description = description
        self.cost = cost
        self.power = power


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

# List to store card instances
cards = []

# Iterate through card elements and extract relevant data
for i in range(len(card_names)):
    tag_text = card_tags[i].text.strip().lower()
    if tag_text != 'none' and tag_text != 'unreleased':
        card_name = card_names[i].text.strip().lower()
        card_tag = tag_text
        card_description = card_descriptions[i].text.strip().lower()
        response = session.get(url + card_name)
        response.html.render()
        soup = BeautifulSoup(response.html.html, 'html.parser')
        card_cost = soup.find('div', class_='cost')
        card_power = soup.find('div', class_='power')
        cards.append(Card(card_name, card_tag,
                     card_description, card_cost, card_power))

print(cards[0].name)
print(cards[0].tag)
print(cards[0].description)
print(cards[0].cost)
print(cards[0].power)

# Close the HTML session
session.close()
