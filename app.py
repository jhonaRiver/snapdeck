#!/usr/bin/env python3

from requests_html import HTMLSession
from bs4 import BeautifulSoup
import psycopg2
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')


class Card:
    """Create class to store card information."""

    def __init__(self, name, tag, ability, cost, power, keywords=None):
        self.name = name
        self.tag = tag
        self.ability = ability
        self.cost = cost
        self.power = power
        self.keywords = keywords


def scraper():
    """
    Scrape website for card information.

    Returns:
        list: List of card instances.
    """
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
        if card_tag != 'none' and card_tag != 'unreleased' and card_tag != 'not available':
            card_name = card.get('data-name')
            card_cost = card.get('data-cost')
            card_power = card.get('data-power')
            card_ability_html = card.get('data-ability')
            card_ability_soup = BeautifulSoup(card_ability_html, 'html.parser')
            card_ability = card_ability_soup.get_text()
            cards.append(Card(card_name, card_tag,
                              card_ability, card_cost, card_power))

    session.close()
    return cards


def storage(cards):
    """
    Add card information to a database.

    Args:
        cards (list): List of card instances.
    """
    # Add card information to a database
    conn = psycopg2.connect(database='snapdeck_db', user='jrivera',
                            password='j5h4o6n6y9')
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS cards (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        tag VARCHAR(255),
        ability TEXT,
        cost INTEGER,
        power INTEGER,
        keywords TEXT[]
    )
    ''')

    for card in cards:
        cur.execute('''
        SELECT * FROM cards WHERE name = %s
        ''', (card.name,))
        result = cur.fetchone()

        if result:
            if result[2] != card.tag or result[3] != card.ability or result[4] != card.cost or result[5] != card.power or result[6] != card.keywords:
                cur.execute('''
                UPDATE cards
                SET tag = %s, ability = %s, cost = %s, power = %s, keywords = %s
                WHERE name = %s
                ''', (card.tag, card.ability, card.cost, card.power, card.keywords, card.name))
        else:
            cur.execute('''
            INSERT INTO cards (name, tag, ability, cost, power, keywords)
            VALUES (%s, %s, %s, %s, %s, %s)
            ''', (card.name, card.tag, card.ability, card.cost, card.power, card.keywords))

    conn.commit()
    cur.close()
    conn.close()


def extract_keywords(ability):
    """
    Extract keywords from card abilities using NLP.

    Args:
        ability (str): Card ability
    Returns:
        list: List of keywords
    """
    words = word_tokenize(ability)
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    tagged = pos_tag(words)
    keywords = [word for word, pos in tagged if pos in ('NN', 'VB', 'JJ')]
    return keywords


if __name__ == '__main__':
    cards = scraper()
    for card in cards:
        keywords = extract_keywords(card.ability)
        card.keywords = keywords
    storage(cards)
