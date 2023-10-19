import requests
import json
import pandas as pd
import numpy as np

headers = {
    'authority': 'api.sofascore.com',
    'accept': '*/*',
    'accept-language': 'pt-PT,pt;q=0.9',
    'cache-control': 'no-cache',
    'origin': 'https://www.sofascore.com',
    'pragma': 'no-cache',
    'referer': 'https://www.sofascore.com/',
    'sec-ch-ua': '"Chromium";v="118", "Brave";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
}


def scrapCompetition(id_competition:int, id_season:[int]) -> pd.DataFrame:
    dfs = []
    for id in id_season:
        dfs.append(_scrapSeason(id_competition,id))

    merged = pd.merge(dfs)
    return merged

def _scrapSeason(id_competition: int, id_season:int)->pd.DataFrame:
    event_data = []
    response = json.loads(requests.get(f'https://api.sofascore.com/api/v1/unique-tournament/{id_competition}/season/{id_season}/rounds',headers=headers).content)
    for i in range(1,response['rounds'][-1]['round']+1):
        
        url = f'https://api.sofascore.com/api/v1/unique-tournament/{id_competition}/season/{id_season}/events/round/{i}'
        response = json.loads(requests.get(url,headers=headers).content)

        for event in response['events']:
            idGame = event['id']
            event_dict = {
                "Event ID": idGame,
                "Jornada": i,
                "Home Team": event["homeTeam"]["name"],
                "Home ID": event["homeTeam"]["id"],
                "Home 1st Period Goals": np.nan,
                "Home 2nd Period Goals": np.nan,
                "Away Team": event["awayTeam"]["name"],
                "Away ID": event["homeTeam"]["id"],
                "Away 1st Period Goals": np.nan,
                "Away 2nd Period Goals": np.nan
            }




            has_rating = bool(event['tournament']['uniqueTournament']['hasEventPlayerStatistics'])

            if int(event['status']['code']) == 100:
                event_dict["Home 1st Period Goals"] = event['homeScore']['period1']
                event_dict["Home 2nd Period Goals"] = event['homeScore']['period2']
                event_dict["Away 1st Period Goals"] = event['awayScore']['period1']
                event_dict["Away 2nd Period Goals"] = event['awayScore']['period2']          

            ######################################################## PREGAME
            url_form = f'https://api.sofascore.com/api/v1/event/{idGame}/pregame-form'
            ratings = json.loads(requests.get(url_form,headers=headers).content)

            try:

                event_dict["Home Form"]: ''.join(ratings['homeTeam']['form'])
                event_dict["Home Points"]: ratings['homeTeam']['value']
                event_dict["Home Position"]: ratings['homeTeam']['position']
                event_dict["Away Form"]: ''.join(ratings['awayTeam']['form'])
                event_dict["Away Points"]: ratings['awayTeam']['value']
                event_dict["Away Position"]: ratings['awayTeam']['position']
                if has_rating:
                    event_dict["Home Avg Rating"] = ratings['homeTeam']['avgRating']
                    event_dict["Away Avg Rating"] = ratings['awayTeam']['avgRating']         

            except:
                pass

            url_stats = f'https://api.sofascore.com/api/v1/event/{idGame}/statistics'
            json_data = json.loads(requests.get(url_stats, headers=headers).content)

            try:
                only_all = len(json_data['statistics']) == 1
                for statistic in json_data['statistics']:
                    period = statistic['period']

                    if only_all or (period != 'ALL'):
                        for group in statistic['groups']:
                            for item in group['statisticsItems']:

                                # Prepare the column names for the database
                                home_column_name = f'Home {period} {item["name"]}'
                                away_column_name = f'Away {period} {item["name"]}'

                                event_dict[home_column_name] = item['home']
                                event_dict[away_column_name] = item['away']
            except:
                pass



            event_data.append(event_dict)

    df = pd.DataFrame(event_data)
    df['Season'] = id_season
    return df

