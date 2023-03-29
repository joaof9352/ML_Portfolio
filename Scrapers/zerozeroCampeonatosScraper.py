import os
import requests
from bs4 import BeautifulSoup
import threading
from pandas.errors import ParserError
import pandas as pd
import sqlite3
import time
import selenium

url = 'https://www.zerozero.pt/edition.php?jornada_in=1&id_edicao=166955'

#response = requests.get(url)

headers_necess = {
  "Cookie": "",
  "Host": "www.zerozero.pt",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
  "Accept-Language": "en-US,en;q=0.5",
  "Accept-Encoding": "identity",
  "Connection": "keep-alive",
  "Referer": url,
  "Sec-Fetch-Dest": "style",
  "Sec-Fetch-Mode": "no-cors",
  "Sec-Fetch-Site": "same-origin",
  "DNT": "1",
  "Pragma": "no-cache",
  "Cache-Control": "no-cache",
  "TE": "trailers"
}

response = requests.get(url, headers=headers_necess)

# parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

divs = soup.find_all('div', {'id': "fixture_games"})
