import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

url = 'http://www.basketball-reference.com/teams/BOS/2020.html'
response = requests.get(url)

cleanedSource = response.text.replace("<!--", "")
cleanedSource = cleanedSource.replace("-->", "")

soup = BeautifulSoup(cleanedSource, "html.parser")

per_game = soup.find_all("div", id="all_per_game")

per_game_header = per_game[0].find("thead")
per_game_header = per_game_header.find("tr")
pg_head_df = pd.DataFrame(per_game_header)
pg_head_df = pg_head_df.transpose()
for col in pg_head_df.columns:
  if col == 3:
    pg_head_df.at[0, 3] = "Name"
  elif pg_head_df.at[0, col] == "\n":
    pg_head_df = pg_head_df.drop(columns=[col], axis=1)
  else:
    pg_head_df.at[0, col] = pg_head_df.at[0, col].text

pg_head_df.columns = np.arange(len(pg_head_df.columns))

header_list = pg_head_df.iloc[0].values.tolist()


per_game_data = per_game[0].find("tbody")
per_game_data = per_game_data.find_all("tr")
pg_data_df = pd.DataFrame(per_game_data)

bball_ref_player_ids = {}

for col in pg_data_df.columns:
  for row in range(len(pg_data_df.index)):
    if col == 1:
      bball_ref_player_ids[pg_data_df.at[row, col].text] = pg_data_df.at[row, col]['data-append-csv']
    pg_data_df.at[row, col] = pg_data_df.at[row, col].text
    
pg_data_df.columns = header_list
pg_data_df = pg_data_df.drop(columns=['Rk'], axis=1)

print(pg_data_df)

jsonResult = pg_data_df.to_json(orient='index');

print(jsonResult)

print(bball_ref_player_ids)


def getPlayerGameLogs(player_id):
  player_str = str(player_id)
  print('https://www.basketball-reference.com/players/' + player_str[(player_str.index(' ') + 1)] + '/' + str(bball_ref_player_ids[player_id]) + '/gamelog/2020')
  url = 'https://www.basketball-reference.com/players/' + player_str[(player_str.index(' ') + 1)] + '/' + str(bball_ref_player_ids[player_id]) + '/gamelog/2020'
  #response = requests.get(url)

  #cleanedSource = response.text.replace("<!--", "")
  #cleanedSource = cleanedSource.replace("-->", "")

  #soup = BeautifulSoup(cleanedSource, "html.parser")  

for player in bball_ref_player_ids:
  getPlayerGameLogs(player)
