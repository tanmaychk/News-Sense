import helper.functions as ns
import streamlit as st
import pandas as pd

def main():
    st.title("News 📰 Sense")
    st.subheader('Making :red[true] :blue[sense] of the News')
    st.text("-" * 90)
    
    sentiment_name = {
        'Neutral': ':neutral_face:',
        'Positive': ':smiley:',
        'Negative': ':disappointed:'
    }
    
    #Fetch the news articles using News API
    articles = ns.get_news_articles()
    
    # Iterate
    for article in articles:
        title = article['title']
        url = article['url']
        content = article['content']

        #Generate Summary
        summary = ns.generate_summary(content)
        #Get Sentiment
        sentiment = ns.analyze_sentiment(content)
        #Categorize
        categories = ns.classify_article(content)        
        
        print(f'\nTitle: {title}')
        print(f'URL: {url}')
        print(f'Summary: {summary}')
        print(f'Sentiment: {sentiment}')
        print(f'Categories: {categories}')
        print('-' * 50)        

        html_str = f'<a href="{url}">{title}</a>&nbsp;{sentiment_name[sentiment]}<br/>'
        st.info(categories[0])
        st.markdown(html_str, unsafe_allow_html=True)
        st.caption(summary) 

if __name__ == '__main__':
    main()