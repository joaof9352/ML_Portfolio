import os
import requests
from bs4 import BeautifulSoup
import threading
from pandas.errors import ParserError
import pandas as pd
import sqlite3
import time

url = 'https://www.olx.pt/ads/?search%5Border%5D=created_at:desc'

con = sqlite3.connect("olx.db")

while True:
    print(f"[{time.asctime()}] - A adicionar ...")
    response = requests.get(url)

    # parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")
    
    divs = soup.find_all('div', {'data-cy': 'l-card'})

    hrefs = []

    for div in divs:
        links = div.find_all('a')
        price_div = div.find('div', {'class': 'css-1apmciz'})
        if price_div is not None:
            title = price_div.find('h6', {'class': 'css-16v5mdi er34gjf0'})
            price = price_div.find('p', {'data-testid': 'ad-price'})
            try:
                float(price.text.replace('.','').replace('€','').replace(',','.').split(' ')[0].rstrip())
                hrefs += [(link['href'],title.text,'NULL',float(price)) for link in links]
            except:
                continue

    # Print the list of hrefs
    # hrefs = [(href,'NULL','NULL',0) for href in hrefs if not (href.startswith('https://www.standvirtual.com/') or href.startswith('https://www.imovirtual.com/'))]
    hrefs = [href for href in hrefs if not (href[0].startswith('https://www.standvirtual.com/') or href[0].startswith('https://www.imovirtual.com/'))]

    
    cur = con.cursor()
    cur.executemany("INSERT OR IGNORE INTO produto VALUES(?,?,?,?,datetime())", hrefs)
    con.commit()
    cur.close()
    print(f"[{time.asctime()}] - Fim, wait de 20 segundos ...")
    time.sleep(20)
