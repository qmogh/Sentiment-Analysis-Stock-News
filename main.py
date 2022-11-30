from urllib.request import urlopen, Request
from bs4 import BeautifulSoup



finviz_url = 'https://finviz.com/quote.ashx?t='
tickers = ['AMZN', 'AMD', 'FB', 'CRBP', 'SATX', 'XPEV', 'DOW', 'AVDL']


news_tables = {}
for ticker in tickers: 
    url = finviz_url + ticker

    req = Request(url=url, headers={'user-agent': 'my-app'})
    response = urlopen(req)
    print(response)
    

    html = BeautifulSoup(response, 'html')
    news_table = html.find(id='news-table')
    news_tables[ticker] = news_table
    break

print(news_table)