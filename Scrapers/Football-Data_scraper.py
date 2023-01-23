import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas.errors import ParserError
import shutil
# specify the URL of the website

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

for url in urls:
  # make a request to the website
  response = requests.get(url)

  # parse the HTML content
  soup = BeautifulSoup(response.content, "html.parser")

  # find all the anchor tags (links)
  links = soup.find_all("a")

  # iterate through the links
  for link in links:
      # get the link's href attribute
      link_url = link.get("href")
      # check if the link is a .csv file
      if link_url is not None and link_url.endswith(".csv"):# and link_url.startswith("http"):
          # check if the text between parentheses contains "match stats" and "AH odds"
          # download the file
          print(link_url)
          file_data = requests.get("https://www.football-data.co.uk/" + link_url)

          parts = link_url.split("/")
          # get the year (the second to last element)
          year = parts[1]
          # create the directory if it doesn't exist
          os.makedirs(year, exist_ok=True)
          # create the full file path
          file_path = os.path.join(year, os.path.basename(link_url)) 

          # create a file with the same name as the link
          with open(file_path, "wb") as f:
              f.write(file_data.content)

# list of years
years = [dir for dir in os.listdir()][1:-1]
print(years)

# create an empty list to store the DataFrames
dfs = []

# iterate through the years
for year in years:
    # create the directory path
    dir_path = os.path.join(".", year)
    # get a list of the csv files in the directory
    csv_files = [f for f in os.listdir(dir_path) if f.endswith(".csv")]
    # iterate through the csv files
    for csv_file in csv_files:
        # create the full file path
        error = False
        file_path = os.path.join(dir_path, csv_file)
        # read the csv file into a DataFrame
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
        except ParserError:
            error = True
            continue
        except Exception:
            try:
                df = pd.read_csv(file_path, encoding='ANSI')
            except Exception:
                error = True
                continue
        # append the DataFrame to the list
        if not error:
            dfs.append(df)

# concatenate all DataFrames
merged_df = pd.concat(dfs, ignore_index=True)

merged_df = merged_df[['Div', 'Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'HTHG', 'HTAG', 'HTR', 'HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'PSH', 'PSD', 'PSA']]
merged_df['Date'] = pd.to_datetime(merged_df['Date'])
merged_df = merged_df[merged_df['Date'].notnull()]
merged_df = merged_df.sort_values(by='Date').reset_index()
merged_df = merged_df.drop('index',axis=1)
merged_df.index.name = 'Index'
merged_df.to_csv('full_dataset.csv')

for year in years:
     shutil.rmtree(year)
