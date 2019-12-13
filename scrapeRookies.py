import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

def scrapePlayersByName(letter):
  if letter == 'x':
    return pd.DataFrame()

  url = 'https://www.basketball-reference.com/players/' + letter + '/'
  response = requests.get(url)

  cleanedSource = response.text.replace("<!--", "")
  cleanedSource = cleanedSource.replace("-->", "")

  soup = BeautifulSoup(cleanedSource, "html.parser")
  soup.prettify()

  soup = soup.find_all("table", id="players")
  table_head = soup[0].find("thead")
  table_head = table_head.find_all("tr")
  headers = pd.DataFrame(table_head)

  for col in headers.columns:
    if headers.at[0, col] == "\n":
      headers = headers.drop(columns=[col], axis=1)
    else:
      headers.at[0, col] = headers.at[0, col].text

  headers.columns = np.arange(len(headers.columns))
  header_list = headers.iloc[0].values.tolist()

  table_data = soup[0].find("tbody")
  table_data = table_data.find_all("tr")
  data = pd.DataFrame(table_data)

  for col in data.columns: 
    for row in range(len(data.index)):
      if not col == 0:
        data.at[row, col] = data.at[row, col].text

  data.columns = header_list
  data = data.drop(columns=["Pos", "Ht", "Wt", "Colleges"], axis=1)

  data = data.loc[data['To'] == "2020"]

  return data

all_rookies = pd.DataFrame()

# BBallRef's data is organized by last name initial
# Must call each page and scape 
for letter in alphabet:
  print(letter)
  if letter == 'a':
    all_rookies = scrapePlayersByName('a')
  else:
    all_rookies = all_rookies.append(scrapePlayersByName(letter))

print(all_rookies)
