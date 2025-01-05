import pandas as pd
import numpy as np

from utility_function import *

line_dataset = pd.read_csv("C:/Users/anime/Downloads/line fitting data.csv")

yac_dataset = pd.read_csv("C:/Users/anime/Downloads/yac data.csv")

players = pd.read_csv("C:/Users/anime/Downloads/players.csv")

prob_model = construct_probability_model(line_dataset)
yac_model = forecast_yac(yac_dataset)


def extract_play_utilities(df, gameId, playId):

    gameIds = []
    playIds = []
    time = []
    utils = []

    df = df[df['gameId'] == gameId]
    df = df[df['playId'] == playId]

    if ('pass_outcome_caught' in df['event'].unique() or 'pass_outcome_incomplete' in df['event'].unique()
        or 'interception' in df['event'].unique()) and ('line_set' in df['event'].unique() and 'ball_snap' in df['event'].unique()):
            
        print('hello')
       
        position = df[df['displayName'] == 'football'][df['event'] == 'ball_snap'].iloc[0]['x']

        dfs = extract_play_df_list(df)

        for z in range(0, len(dfs)):
            print(len(dfs))
            print(len(dfs) - z)
            print(dfs[z].iloc[0]['time'])

            utils.append(find_utility(dfs[z],line_dataset, yac_dataset, prob_model, yac_model, position))
            time.append(dfs[z].iloc[0]['time'])
            gameIds.append(gameId)
            playIds.append(playId)

        df = pd.DataFrame()
        df['Utility'] = utils
        df['Time'] = time
        df['gameId'] = gameIds
        df['playId'] = playIds

    return df
all_data = pd.merge(pd.read_csv("C:/Users/anime/Downloads/tracking_week_1.csv"), players, on = 'displayName', how = 'left')
extract_play_utilities(all_data, 2022091200, 109).to_csv("C:/Users/anime/Downloads/utility visual.csv")