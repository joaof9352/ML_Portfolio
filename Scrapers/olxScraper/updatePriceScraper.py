import os
import requests
from bs4 import BeautifulSoup
import threading
from pandas.errors import ParserError
import pandas as pd
import sqlite3
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

con = sqlite3.connect("olx.db")
cur = con.cursor()
cur.execute("SELECT url FROM anuncio WHERE removido=0")
urls = cur.fetchall()
cur.close()

#urls = [('/d/anuncio/trotinete-eltrica-ninebot-d18e-IDHwMQf.html',)]

for url in urls:

    driver = webdriver.Chrome()    
    driver.get('https://www.olx.pt' + url[0])
    
    wait = WebDriverWait(driver, 10)
    span = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="page-view-text"]')))
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    span = soup.find('span', {'data-testid': "page-view-text"})
    text = span.text
    views = int(text.split(': ')[-1])
    
    span = soup.find('h3', {'class': "css-ddweki er34gjf0"})
    text = span.text
    price = int(text[0])
    
    span = soup.find('p', {'class': "css-1cju8pu er34gjf0"})
    freguesia = span.text[0]
    
    span = soup.find('p', {'class': "css-b5m1rv er34gjf0"})
    concelho = span.text
    

    print(number, views, freguesia, concelho)
    
    driver.close()
