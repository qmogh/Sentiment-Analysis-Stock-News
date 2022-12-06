# Import necessary libraries
import requests
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import pandas as pd
import nltk

# Download necessary resources for the nltk library
nltk.download('vader_lexicon')


# Define a function that takes a stock ticker symbol as input and returns a list of news articles
def get_stock_news(ticker):
    articles = []
    # Scrape news articles from finviz using the ticker symbol
    url = 'https://finviz.com/quote.ashx?t={}'.format(ticker)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    # Find the news table on the page
    news_table = soup.find('table', {'class': 'fullview-news-outer'})
    # Check if a news table was found, and return an empty list if not
    if news_table is None:
        return articles
    # Extract the title and date of each article
    news_rows = news_table.find_all('tr')[1:]
    for row in news_rows:
        date = row.find_all('td')[0].text
        title = row.find_all('td')[1].text
        article = {'date': date, 'title': title}
        articles.append(article)
    return articles



# Define a function that takes a list of articles and returns a dictionary of sentiment scores
def analyze_sentiment(articles):
    sentiment_scores = {}
    # Use a sentiment analysis model to score each article
    sid = SentimentIntensityAnalyzer()
    for article in articles:
        title = article['title']
        sentiment = sid.polarity_scores(title)['compound']
        sentiment_scores[title] = sentiment
    print(sentiment_scores)
    return sentiment_scores


def visualize_sentiment(sentiment_scores):
    # Use data visualization techniques to present the sentiment analysis results
    df = pd.DataFrame.from_dict(sentiment_scores, orient='index')
    # Convert the sentiment scores to numeric values
    df = df.apply(pd.to_numeric, errors='coerce')
    # Check if the DataFrame contains any numeric data
    if df.select_dtypes(include=['number']).empty:
        print('No numeric data found.')
        return
    # Create a bar chart of the sentiment analysis results
    df.plot(kind='bar')
    plt.xlabel('Article Title')
    plt.ylabel('Sentiment Score')
    plt.title('Sentiment Analysis of Stock News Articles')
    # Save the plot as an image file
    plt.savefig('sentiment_analysis.png')


# Define main function
def main():
    # Get stock ticker from user input
    ticker = input('Enter a stock ticker: ')
    # Get list of news articles for the specified stock
    articles = get_stock_news(ticker)
    # Analyze sentiment of the articles
    sentiment_scores = analyze_sentiment(articles)
    # Visualize the sentiment analysis results
    visualize_sentiment(sentiment_scores)


# Run main function
if __name__ == '__main__':
    main()
