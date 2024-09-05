from bs4 import BeautifulSoup
import requests
import json
import os
import urllib.request
import math
import sqlite3
from urllib.request import urlretrieve
from nba_api.stats.static import players

def find_IDs_and_names():
    all_players = players.get_active_players()
    #print(type(all_players))
    name_and_ids = [(player["full_name"].replace('\\', ''), f"ID:{player['id']}") for player in all_players]
    #name_and_ids = json.dumps(name_and_ids)
    #print(type(name_and_ids))
    
    #with open("name_and_ids.json", "w", encoding="utf-8") as file:
        #file.write(name_and_ids +"\n")
    
    return name_and_ids


def get_IDs():
    names_and_ids = find_IDs_and_names()
    IDs = []
    #print(names_and_ids)
    for combo in names_and_ids:
        for item in combo:
            colon_index = item.find(":")
            if colon_index != -1:
                ID = item[colon_index+1:]
                IDs.append(ID)
    with open("IDs.json", "w", encoding = "utf-8") as file:
        json.dump(IDs, file, indent = 4)
    return IDs



def get_Names():
    names_and_ids = find_IDs_and_names()
    names= [player[0] for player in names_and_ids]
    with open("names.json", "w", encoding = "utf-8") as file:
        json.dump(names, file, indent = 4)
    return names

def get_HeadShots_ID():
    """
    Retrieve the headshots from the ESPN site for players given their ID

    :return a single headshot
    """
    IDs = get_IDs()
    base_URL = "https://cdn.nba.com/headshots/nba/latest/260x190/"

    for ID in IDs:
        url = f"{base_URL}{ID}.png"
        print(url)
        response = requests.get(url)
        print(response)

        if response.status_code == 200:
            with open(f"nba_headshots/{ID}.png", "wb") as f:
                f.write(response.content)
            print(f"Downloaded {ID}")
        else:
            print(f"Failed to download {ID}")


def get_worth():
    with open("player_ratings.json") as file:
        data = json.load(file)
    ratings = list(data.values())
    ratings = [0 if math.isnan(r) else round(r,2) for r in ratings]
    with open("Real_Worth.json", "w") as file:
        json.dump(ratings,file, indent = 4)
    return ratings




