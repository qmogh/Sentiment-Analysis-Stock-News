from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as BS



finviz_url = 'https://finviz.com/quote.ashx?t='
tickers = ['AMZN', 'AMD', 'FB', 'CRBP', 'SATX', 'XPEV', 'DOW', 'AVDL']


news_tables = {}
for ticker in tickers: 
    url = finviz_url + ticker

    req = Request(url=url, headers={'user-agent': 'my-app'})
    response = urlopen(req)
 
    

    html = BS(response, 'html')
    news_table = html.find(id='news-table')
    news_tables[ticker] = news_table
    break



parsed_data = []
for ticker, news_table in news_tables.items():
    for row in news_table.findAll('tr'):
        title = row.a.text
        date_data = row.td.text.split(' ')

        if len(date_data) == 1:
            time = date_data[0]
        else:
            date = date_data[0]
            time = date_data[1]

        parsed_data.append([ticker, date, time, title])

print(parsed_data)
    

