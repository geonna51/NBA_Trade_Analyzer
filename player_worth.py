from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import SeasonAll
from nba_api.stats.endpoints import playergamelogs
import pandas as pd
import json
import time
season = 2023

timeout = 60
with open("IDs.json","r") as file:
        IDs = json.load(file)


def get_stats(player_id):
    gamelog_id = playergamelog.PlayerGameLog(season = season, player_id = player_id)
    gamelog_id = gamelog_id.get_data_frames()[0]
    PTS = gamelog_id["PTS"].mean()
    REBOUNDS = gamelog_id["REB"].mean()
    ASSISTS = gamelog_id["AST"].mean()
    STEALS = gamelog_id["STL"].mean()
    BLOCKS = gamelog_id["BLK"].mean()
    TURNOVERS = gamelog_id["TOV"].mean()
    FG = gamelog_id["FG_PCT"].mean()
    FG3 = gamelog_id["FG3_PCT"].mean()
    FT = gamelog_id["FT_PCT"].mean()
    Rating = (PTS * 0.5)+(REBOUNDS * 0.5) + (ASSISTS*0.3) + (STEALS*0.5) + (BLOCKS*0.5) - (TURNOVERS*0.3)+(FG*10)
    return(Rating)

try:
    with open("player_ratings.json","r") as file:
        player_ratings = json.load(file)
except FileNotFoundError:
     player_ratings ={}

for player_id in IDs:
    if str(player_id) not in player_ratings:
        try:
            rating = get_stats(player_id)
            player_ratings[str(player_id)] = rating
            print(f"Processed player ID: {player_id}, Rating: {rating}")
            
            # Save after each successful request
            with open("player_ratings.json", "w") as file:
                json.dump(player_ratings, file)
            
            # Wait for the specified timeout
            time.sleep(timeout)
        except Exception as e:
            print(f"Error processing player ID {player_id}: {str(e)}")
    else:
        print(f"Player ID {player_id} already processed. Skipping.")

print("All players processed.")


