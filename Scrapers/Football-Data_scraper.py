import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas.errors import ParserError
import shutil

urls = [#"https://www.football-data.co.uk/argentina.php", "https://www.football-data.co.uk/austria.php", "https://www.football-data.co.uk/brazil.php", "https://www.football-data.co.uk/china.php", "https://www.football-data.co.uk/denmark.php", "https://www.football-data.co.uk/finland.php", "https://www.football-data.co.uk/ireland.php", "https://www.football-data.co.uk/japan.php", "https://www.football-data.co.uk/mexico.php", "https://www.football-data.co.uk/norway.php", "https://www.football-data.co.uk/poland.php", "https://www.football-data.co.uk/romania.php", "https://www.football-data.co.uk/russia.php","https://www.football-data.co.uk/sweden.php","https://www.football-data.co.uk/switzerland.php", "https://www.football-data.co.uk/usa.php",
"https://www.football-data.co.uk/englandm.php",
"https://www.football-data.co.uk/scotlandm.php",
"https://www.football-data.co.uk/germanym.php",
"https://www.football-data.co.uk/italym.php",
"https://www.football-data.co.uk/spainm.php",
"https://www.football-data.co.uk/francem.php",
"https://www.football-data.co.uk/netherlandsm.php",
"https://www.football-data.co.uk/belgiumm.php",
"https://www.football-data.co.uk/portugalm.php",
"https://www.football-data.co.uk/turkeym.php",
"https://www.football-data.co.uk/greecem.php"]

dfs = []
lock = threading.Lock()
threads = []

def scrap_country(url):
    response = requests.get(url)

    # parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")
    
    # find all the anchor tags (links)
    links = soup.find_all("a")
    
    # iterate through the links
    for link in links:
        
        link_url = link.get("href")
        error = False
        
        if link_url is not None and link_url.endswith(".csv"):
            try:
                df = pd.read_csv("https://www.football-data.co.uk/" + link_url, encoding='utf-8')
            except ParserError:
                print(f'ParserError: Error in {link_url}')
                error = True
            except Exception:
                try:
                    df = pd.read_csv("https://www.football-data.co.uk/" + link_url, encoding='ANSI')
                except Exception:
                    print(f'EncodingError: Error in {link_url}')
                    error = True
        
            if not error:
                with lock:
                    dfs.append(df) 

for url in urls:
    t = threading.Thread(target=scrap_country, args=[url])
    t.start()
    threads.append(t)
    
for thread in threads:
    thread.join()

merged_df = pd.concat(dfs, ignore_index=True)

merged_df = merged_df[['Div', 'Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'HTHG', 'HTAG', 'HTR', 'HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'PSH', 'PSD', 'PSA']]
merged_df = merged_df[merged_df['Date'].notnull()]
merged_df['Date'] = pd.to_datetime(merged_df['Date'], dayfirst=True)
merged_df = merged_df.sort_values(by='Date').reset_index()
merged_df = merged_df.drop('index',axis=1)
merged_df.index.name = 'Index'
merged_df.to_csv('full_dataset.csv')
