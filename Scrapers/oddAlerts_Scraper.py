from bs4 import BeautifulSoup
import requests
from secrets import PATH
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

league_url = 'https://oddalerts.com/leagues/portugal/2-division-group-a?id=3284'

a = requests.get(league_url)
soup = BeautifulSoup(a.content, "html.parser")
target_links = soup.find_all("a", {"rel": "nofollow", "class": "oa_card status"})
data_uids = []
for link in target_links:
    data_uid = link.get("data-uid")
    data_uids.append(data_uid)

chromedriver_path = PATH

# Initialize the browser driver with the specified path
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(executable_path=chromedriver_path,options=chrome_options)

lista = []

for data_uid in data_uids:
    dic = {}
    dic['id'] = data_uid
    url = 'https://oddalerts.com/set/quick/' + data_uid
    driver.get(url)
    
    # NAMES, DATE, RESULT
    # Wait for all "title-bar" elements to be present
    title_bars = WebDriverWait(driver, 3).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'title-bar'))
    )
    
    if len(title_bars) > 1:
        title_bar = title_bars[1]
    else:
        title_bar = title_bars[0]
    
    
    # Extract the team names
    team_names = title_bar.find_element(By.TAG_NAME, 'h2').text

    # Extract the text inside the "status" element
    try:
        status_text = title_bar.find_element(By.CLASS_NAME, 'status').text
    except Exception:
        status_text = "N/A"

    print(f"Team Names: {team_names}, Status: {status_text}")
    print(team_names)
    dic['team_names'] = team_names
    dic['status'] = status_text

    # ODDS
    try:

        outcome_list = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'outcome-list'))
        )

        outcome_items = outcome_list.find_elements(By.TAG_NAME, 'li')

        for item in outcome_items[1:4]:  # Skipping the header element
            title = item.find_element(By.CLASS_NAME, 'title').text
            odds_value = item.find_elements(By.CLASS_NAME, 'value')[0].text
            dic[title] = odds_value
            
    except Exception as e:
        print(f"Não há odds para o jogo {team_names}")
    
    # STATS
    
    stats_li = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, "//li[contains(text(), 'Stats')]"))
    )
    
    
    stats_li.click()
    
    # Wait for the element with class "comparison-bar-list" to be present
    try:
        comparison_bar_lists = WebDriverWait(driver, 3).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'comparison-bar-list'))
        )

        # Select the second "comparison-bar-list" element (index 1)
        if len(comparison_bar_lists) > 1:
            comparison_bar_list = comparison_bar_lists[1]
        else:
            comparison_bar_list = comparison_bar_lists[0]

        # Find all "comparison-bar" elements within the "comparison-bar-list"
        comparison_bars = comparison_bar_list.find_elements(By.CLASS_NAME,'comparison-bar')

        for bar in comparison_bars:
            # Locate the title and label elements within each "comparison-bar"
            title_element = bar.find_element(By.CLASS_NAME,'title')
            label_elements = bar.find_elements(By.CLASS_NAME,'label')

            # Extract the text from the title element
            title_text = title_element.text

            try:
                span_element = title_element.find_element(By.TAG_NAME,'span')
                if span_element:
                    title_text = title_text.replace(span_element.text, '').strip()
            except:
                pass

            home_value = label_elements[0].text
            away_value = label_elements[1].text
            dic[f'home_{title_text}'] = home_value
            dic[f'away_{title_text}'] = away_value

    except Exception as e:
        print(e)
        print('There are no stats available for this game')
      
    lista.append(dic)
  
driver.quit()
