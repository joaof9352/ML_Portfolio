import pandas as pd
from bs4 import BeautifulSoup
import requests
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
import re
import time

dfs = []
#URL From a league, page of results and calendars
urls = ['https://fbref.com/pt/comps/32/cronograma/Primeira-Liga-Resultados-e-Calendarios#sched_2022-2023_32_1']

for url in urls:

    df = pd.read_html(url, extract_links="all")
    df = df[0]

    df.columns = [col[0] for col in df.columns]

    df_getSecondTuple = ['Relatório da Partida']

    for column in df.columns:
        if column not in df_getSecondTuple:
            df[column] = df[column].apply(lambda x: x[0])
        else:
            df[column] = df[column].apply(lambda x: x[1])
                
    df['goals_home'] = df['Resultado'].str.split('–').str[0]
    df['goals_away'] = df['Resultado'].str.split('–').str[1]
    df.drop(['Resultado','Notas'],axis=1,inplace=True)
    df = df.dropna().reset_index().drop('index',axis=1)
    df.rename({'xG': 'xG_home', '(': 'xG_away', 'Em casa': 'home', 'Visitante': 'away', 'Público': 'Assistance', 'Sem': 'Jornada'}, axis=1, inplace=True)

    for index, row in df.iterrows():
        
        if 'jogador1_home' not in df.columns or pd.isnull(df.loc[index,'jogador1_home']):
        
            start = time.time()

            url = row['Relatório da Partida']
            print(url)
            r = requests.get('http://fbref.com' + url)
            soup = BeautifulSoup(r.content, 'html.parser')
            tables = soup.find_all('table')
            table = tables[0]
            table2 = tables[1]
            home_players = pd.read_html(str(table))[0].drop(11)
            away_players = pd.read_html(str(table2))[0].drop(11)
            df.loc[index,'formacao_home'] = home_players.columns[0].split('(')[1][:-1]
            df.loc[index,'formacao_away'] = away_players.columns[0].split('(')[1][:-1]
            home_players = home_players.transpose().reset_index().drop('index',axis=1)
            away_players = away_players.transpose().reset_index().drop('index',axis=1)

            print(f'meio: {time.time() - start}')
            
            stats_div = soup.find('div', {'id': 'team_stats_extra'})

            # extrai o conteúdo da div
            stats_text = stats_div.text

            linhas = stats_text.split('\n')
            palavras_chave = ['Faltas', 'Escanteios', 'Cruzamentos', 'Contatos', 'Bote defensivo', 'Cortes', 'Jogadas aéreas', 'Defesas', 'Impedimentos', 'Tiro de meta', 'Cobrança de lateral', 'Bolas longas']

            lista_strings = [string for string in linhas for palavra in palavras_chave if palavra in string]

            nova_lista = []
            for string in lista_strings:
                match = re.match(r'^(\d+)([a-zA-Z\s]+)(\d+)$', string)
                if match:
                    nova_lista.append([int(match.group(1)), match.group(2).strip(), int(match.group(3))])
            
            for x in nova_lista:
                df.loc[index, f"{x[1]}_home"] = x[0]
                df.loc[index, f"{x[1]}_away"] = x[2]
                
                
            cards = {
                'home_team': {
                    'yellow_card': 0,
                    'red_card': 0,
                    'yellow_red_card': 0
                },
                'away_team': {
                    'yellow_card': 0,
                    'red_card': 0,
                    'yellow_red_card': 0
                }
            }

            home_team_cards_div = soup.find_all('div', class_='cards')[0]
            home_team_cards_spans = home_team_cards_div.find_all('span')
            for span in home_team_cards_spans:
                cards['home_team'][span['class'][0]] += 1

            away_team_cards_div = soup.find_all('div', class_='cards')[1]
            away_team_cards_spans = away_team_cards_div.find_all('span')
            for span in away_team_cards_spans:
                cards['away_team'][span['class'][0]] += 1
            
            df.loc[index, 'yellow_card_home'] = cards['home_team']['yellow_card']
            df.loc[index, 'red_card_home'] = cards['home_team']['red_card']
            df.loc[index, 'yellow_red_card_home'] = cards['home_team']['yellow_red_card']
            df.loc[index, 'yellow_card_away'] = cards['away_team']['yellow_card']
            df.loc[index, 'red_card_away'] = cards['away_team']['red_card']
            df.loc[index, 'yellow_red_card_away'] = cards['away_team']['yellow_red_card']
            
            for i in range(len(home_players.columns) - 1):
                column_name = f'jogador{i+1}_home'
                df.loc[index, column_name] = home_players.iloc[1, i]
            for i in range(len(away_players.columns) - 1):
                column_name = f'jogador{i+1}_away'
                df.loc[index, column_name] = away_players.iloc[1, i]

            #Request limit: 30 per minute
            print(f'fim: {time.time() - start}')
            if time.time() - start < 2.0:
                time.sleep(2.1 - (time.time() - start))

    dfs.append(df)

result_df = pd.concat(dfs)
result_df = result_df.sort_values('Data').reset_index(drop=True)

result_df.to_csv('output.csv')
