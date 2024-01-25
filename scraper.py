#!/usr/bin/env python3

from requests_html import HTMLSession
from bs4 import BeautifulSoup
import psycopg2


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
        card_ability_html = card.get('data-ability')
        card_ability_soup = BeautifulSoup(card_ability_html, 'html.parser')
        card_ability = card_ability_soup.get_text()
        cards.append(Card(card_name, card_tag,
                     card_ability, card_cost, card_power))

session.close()

# Add card information to a database
conn = psycopg2.connect("dbname=snapdeck_db user=postgres")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS cards (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    tag VARCHAR(255),
    ability TEXT,
    cost INTEGER,
    power INTEGER
)
""")

for card in cards:
    cur.execute("""
    INSERT INTO cards (name, tag, ability, cost, power)
    VALUES (%s, %s, %s, %s, %s)
    """, (card.name, card.tag, card.ability, card.cost, card.power))

conn.commit()
cur.close()
conn.close()
