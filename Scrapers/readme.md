# Web Scrapers

## FBref Scraper
This scraper is capable of collecting player and team data from [FBref](https://fbref.com/), which scrapes all the matches from the given football leagues. All the game statistics and players are included.

The scraper code is fully functional and can be found in the [fbref_scraper.py](https://github.com/joaof9352/ML_Portfolio/blob/main/Scrapers/FBRef_Scraper.py) file. 

## ZeroZero Scraper
This scraper is not yet functional but will be capable of collecting data from the [ZeroZero.pt](https://www.zerozero.pt/), getting all the data from the given league.

## Football-Data Scraper
This scraper is capable of collecting data from the [Football-Data](https://www.football-data.co.uk/), which provides football data from various leagues, including Premier League, La Liga, Serie A, Bundesliga, and others.

The scraper code is fully functional and can be found in the football_data_scraper.py file. The usage is very simple: Add all the urls from the leagues you want to the variable "urls" and full_dataset.csv will be created with all the info in it. 

## How to Use
To use the scrapers, you will need to have Python 3.x installed on your system, as well as the libraries listed in the requirements.txt file. It is recommended to create a Python virtual environment to manage the dependencies.

*Each scraper has its own class defined in its file, which can be imported and used as needed. Additionally, there are examples of how to use each scraper in example_usage.py.*

## Contribution
Feel free to contribute to this project. Any type of help is welcome, from bug fixes to the implementation of new features. If you find an issue or have an idea to improve this project, please open an issue or send a pull request.
