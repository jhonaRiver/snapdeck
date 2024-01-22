#!/usr/bin/env python3

from requests_html import HTMLSession
from bs4 import BeautifulSoup


# Create class to store card information


class Card:
    def __init__(self, name, tag, ability, cost, power):
        self.name = name
        self.tag = tag
        self.ability = ability
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
card_list = soup.find_all('a', class_='simple-card')

# List to store card instances
cards = []

for card in card_list:
    card_tag = card.get('data-source').strip().lower()
    if card_tag != 'none' and card_tag != 'unreleased':
        card_name = card.get('data-name')
        card_cost = card.get('data-cost')
        card_power = card.get('data-power')
        card_ability = card.get('data-ability')
        cards.append(Card(card_name, card_tag,
                     card_ability, card_cost, card_power))

session.close()

# TODO: Add card information to a database
