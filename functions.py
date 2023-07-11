import os
import requests
import openai
import streamlit as st
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer

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
        
    print("Overall sentiment dictionary is : ", sentiment_dict)
    print("The news was rated as ", sentiment_dict['neg']*100, "% Negative")
    print("The news  was rated as ", sentiment_dict['neu']*100, "% Neutral")
    print("The news  was rated as ", sentiment_dict['pos']*100, "% Positive")
 
    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05 :
        sentiment_scores = "Positive"
    elif sentiment_dict['compound'] <= - 0.05 :
        sentiment_scores = "Negative"
    else :
        sentiment_scores = "Neutral"  
    
    print("The news was overall rated as ", sentiment_scores)
    return sentiment_scores

def classify_article(text):
    categories = []

    # Define keywords for each category
    business_keywords = ['business', 'economy', 'finance', 'stock', 'share', 'cost', 'billion', 'inflation']
    tech_keywords = ['technology', 'internet', 'software', 'hardware','crypto','cloud']
    sports_keywords = ['sport', 'football', 'basketball', 'soccer', 'game']
    entertainment_keywords = ['entertainment', 'celebrity', 'movie', 'music', 'television', 'film', 'netflix']
    politics_keywords = ['united nations', 'election', 'politic', 'vote', 'ukraine', 'conflict', 'government']
    society_keywords = ['disaster', 'hospital', 'weather', 'flood', 'social', 'shop', 'school','children', 'family']

    # Check if any category keywords are present in the text
    for keyword in business_keywords:
        if keyword in text.lower():
            categories.append('Business')
            break

    for keyword in tech_keywords:
        if keyword in text.lower():
            categories.append('Technology')
            break

    for keyword in sports_keywords:
        if keyword in text.lower():
            categories.append('Sports')
            break

    for keyword in entertainment_keywords:
        if keyword in text.lower():
            categories.append('Entertainment')
            break
            
    for keyword in society_keywords:
        if keyword in text.lower():
            categories.append('Society')
            break
            
    for keyword in politics_keywords:
        if keyword in text.lower():
            categories.append('Politics')
            break

    # If no category keywords are present, classify as "Other"
    if not categories:
        categories.append('Other')

    return categories