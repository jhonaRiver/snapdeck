#!/usr/bin/env python3

from requests_html import HTMLSession
from bs4 import BeautifulSoup
import psycopg2
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PWD = os.getenv('DB_PWD')

app = Flask(__name__)
CORS(app)

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
conn = psycopg2.connect(database=DB_NAME, user=DB_USER,
                        password=DB_PWD)


class Card:
    """Create class to store card information."""

    def __init__(self, name, tag, ability, cost, power, img, keywords=None):
        self.name = name
        self.tag = tag
        self.ability = ability
        self.cost = cost
        self.power = power
        self.img = img
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
            card_img = card.get('data-src')
            card_ability_html = card.get('data-ability')
            card_ability_soup = BeautifulSoup(card_ability_html, 'html.parser')
            card_ability = card_ability_soup.get_text()
            cards.append(Card(card_name, card_tag,
                              card_ability, card_cost, card_power, card_img))

    session.close()
    return cards


def storage(cards):
    """
    Add card information to a database.

    Args:
        cards (list): List of card instances.
    """
    # Add card information to a database

    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS cards (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        tag VARCHAR(255),
        ability TEXT,
        cost INTEGER,
        power INTEGER,
        img TEXT,
        keywords TEXT[]
    )
    ''')

    for card in cards:
        cur.execute('''
        SELECT * FROM cards WHERE name = %s
        ''', (card.name,))
        result = cur.fetchone()

        if result:
            if result[2] != card.tag or result[3] != card.ability or result[4] != card.cost or result[5] != card.power or result[6] != card.img or result[7] != card.keywords:
                cur.execute('''
                UPDATE cards
                SET tag = %s, ability = %s, cost = %s, power = %s, img = %s, keywords = %s
                WHERE name = %s
                ''', (card.tag, card.ability, card.cost, card.power, card.img, card.keywords, card.name))
        else:
            cur.execute('''
            INSERT INTO cards (name, tag, ability, cost, power, img, keywords)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (card.name, card.tag, card.ability, card.cost, card.power, card.img, card.keywords))

    conn.commit()
    cur.close()


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


def get_card_keywords_and_image(card_name):
    """
    Get keywords for specific card.

    Args:
        card_name (str): name of the card
    Returns:
        list: List of keywords
    """
    cur = conn.cursor()
    cur.execute('''
    SELECT keywords, img FROM cards WHERE name = %s
    ''', (card_name,))
    result = cur.fetchall()
    cur.close()
    if result:
        return result[0]
    else:
        return []


def recommend_cards(card_name, keywords):
    """
    Recommend cards based on keywords.

    Args:
        keywords (list): List of keywords to match
    Returns:
        list: List of recommended card names
    """
    cur = conn.cursor()
    cur.execute('''
    SELECT name, keywords, img FROM cards
    ''')
    results = cur.fetchall()
    cur.close()
    common_keywords_counts = [(name, img, len(set(keywords) & set(
        card_keywords))) for name, card_keywords, img in results if name != card_name]
    recommended_cards = sorted(
        common_keywords_counts, key=lambda x: x[2], reverse=True)[:11]
    return [{'name': name, 'img': img} for name, img, _ in recommended_cards]


@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    card_name = request.args.get('cardName')
    if not card_name:
        return jsonify({'error': 'Missing cardName parameter'}), 400

    card_keywords, card_img = get_card_keywords_and_image(card_name)
    recommended_cards = recommend_cards(card_name, card_keywords)
    recommended_cards.insert(0, {'name': card_name, 'img': card_img})

    return jsonify(recommended_cards)


@app.route('/card', methods=['GET'])
def get_card():
    card_name = request.args.get('cardName')
    if not card_name:
        return jsonify({'error': 'Missing cardName parameter'}), 400

    cur = conn.cursor()
    cur.execute('''
    SELECT * FROM cards WHERE name = %s
    ''', (card_name,))
    result = cur.fetchone()
    cur.close()
    if result:
        return jsonify({'img': result[7], 'ability': result[3].capitalize()})
    else:
        return jsonify({'error': 'Card not found'}), 404


if __name__ == '__main__':
    cards = scraper()
    for card in cards:
        keywords = extract_keywords(card.ability)
        card.keywords = keywords
    storage(cards)
    app.run(host='0.0.0.0', port=5000, debug=True)
    conn.close()


# TODO: See how to get better keywords for the recommendation
