import os
import requests
import openai
import streamlit as st
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

def get_news_articles():
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'country': 'us',
        'apiKey': os.getenv('NEWS_API_KEY'),
        'pageSize':5,
    }
    response = requests.get(url, params=params)
    articles = response.json()['articles']
    return articles

def generate_summary(text):
    openai.api_key =  os.getenv('CHATGPT_API_KEY')
    response = openai.Completion.create(
        engine ='text-davinci-003',
        prompt =f"Summarize this text:{text}",
        max_tokens = 100,
        n = 1,
        stop = None,
        temperature = 1,
    )
    summary = response.choices[0].text.strip()
    #summary = "MOCK: Uncomment this line if you want to test this out without hitting GPT API."
    return summary

def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    
    # polarity_scores returns a sentiment dictionary.
    # It contains pos, neg, neu, and compound scores
    sentiment_dict = sia.polarity_scores(text)        
    print("The news was rated as ", sentiment_dict['neg'] * 100, "% Negative")
    print("The news was rated as ", sentiment_dict['neu'] * 100, "% Neutral")
    print("The news was rated as ", sentiment_dict['pos'] * 100, "% Positive")
 
    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05:
        sentiment_scores = "Positive"
    elif sentiment_dict['compound'] <= -0.05:
        sentiment_scores = "Negative"
    else:
        sentiment_scores = "Neutral"
    
    print("Overall, the news was rated as ", sentiment_scores)
    return sentiment_scores


def classify_article(text):
    categories = []

    # Define keywords for each category   
    categories = {
        'Business': ['business', 'economy', 'finance', 'stock', 'share', 'cost', 'loan', 'inflation', 'credit', 'bank'],
        'Technology': ['technology', 'internet', 'software', 'hardware', 'crypto', 'cloud', 'artificial'],
        'Sports': ['sport', 'football', 'basketball', 'soccer', 'game', 'golf', 'cricket', 'baseball', 'NBA'],
        'Entertainment': ['entertainment', 'celebrity', 'movie', 'music', 'television', 'film', 'netflix'],
        'Politics': ['summit', 'election', 'politic', 'vote', 'ukraine', 'conflict', 'government'],
        'Society': ['pollution', 'hospital', 'weather', 'judge', 'social', 'shop', 'school', 'children', 'family']
    }
    
    text = text.lower()
    
    # Check if any category keywords are present in the text
    for category, keywords in categories.items():
        if any(keyword in text for keyword in keywords):
            return category
    
    return 'Other'
