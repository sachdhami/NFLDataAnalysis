"""
Submission: api_access.py as part of the CSE163 Final Project
CSE163 Section A: Lucas Swanson, Sachin Dhami, Zach Rinehart

api_access.py is a python script that is structured to pull data from a
specific API (sportsdata.io) to retrieve data from a new source not covered
in CSE 163. This file will access the API, confirm that the API is online
and functional, reformats the data, and saves the data as a CSV accessible
in spreadsheet editors like Microsoft Excel.
"""

import requests as rq
import pandas as pd

def main():
    uri = "https://api.sportsdata.io"
    endpoint = "/v3/nfl/scores/json/Players"
    apikey = __getkey__()    
    #retrieve data and convert to dataframe.
    player_info = get_player_info(uri, endpoint, apikey)
    player_infodf = pd.DataFrame(player_info)
    #add the player's full name to the dataframe
    player_infodf["LastFirst"] = (player_infodf['LastName'] + ", " 
                                  + player_infodf['FirstName'])

    player_metrics = get_player_metrics(uri, endpoint, apikey)
    player_metricsdf = pd.DataFrame(player_metrics)
    #convert datasets to csv's
    player_metricsdf.to_csv("player_metrics.csv", index=False, header=False)
    player_infodf.to_csv("player_info.csv", index=False, header=False)


def get_player_info(uri, endpoint, apikey):
    """
    get_player_info takes a uri, endpoint, and apikey as parameters. It gets a
    response from the player info api, then formats and returns that response.
    
    """
    response = rq.get(uri + endpoint + apikey)
    print("get_player_info() request returned with code "
          + str(response.status_code))
    return pd.json_normalize(response.json())


def get_player_metrics(uri, endpoint, apikey):
    """
    get_player_metrics takes a uri, endpoint, and apikey as parameters. It
    gets a response from the player stats api, then formats and returns 
    that response.
    """
    response = rq.get(uri + endpoint + apikey)
    print("get_player_metrics () request returned with code "
          + str(response.status_code))
    return response.json()


def __getkey__():
    """
    __getkey__() is a private method to securely store an api key. Replace
    this key with your key when running the program.
    """
    return "?key=afd7b6f84e454af5a11c8731dfa9f796"


if __name__ == "__main__":
    main()