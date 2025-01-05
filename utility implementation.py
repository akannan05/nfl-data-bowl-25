import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from utility_function import *



line_dataset = pd.read_csv("C:/Users/anime/Downloads/line fitting data.csv")

yac_dataset = pd.read_csv("C:/Users/anime/Downloads/yac data.csv")

players = pd.read_csv("C:/Users/anime/Downloads/players.csv")


#print(full_df['event'].unique())

#print(full_df.iloc[0])

#full_df = full_df[full_df['event'] == 'line_set']

#full_df = full_df[full_df['displayName'] == 'football']

#snap_time = full_df[full_df['event'] == 'ball_snap']

#print(full_df.iloc[0]['x'])

prob_model = construct_probability_model(line_dataset)
yac_model = forecast_yac(yac_dataset)
#

#print(find_utility(dfs[350],line_dataset, yac_dataset, prob_model, yac_model, full_df.iloc[0]['x']))






#plt.plot(times, utilities, 'r')
#plt.title("Utility over Time for Play 1")
#plt.xlabel("Time Since Snap")
#plt.ylabel("Utility of Play")

#plt.show()

paths = ["C:/Users/anime/Downloads/tracking_week_5.csv"]
data_list = []

for x in paths:

    data_list.append(pd.read_csv(x))

    print(x)



all_data = pd.concat(data_list, axis = 0)
all_data = pd.merge(all_data, players, on = 'displayName', how = 'left')

print(all_data)

gameId = []
playId = []
time = []
utils = []

names = []
positions = []
marginals = []
gameIds = []
playIds = []
mar_times = []

def extract_play_utilities(df, gameId, playId):

    gameId = []
    playId = []
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
            gameId.append(x)
            playId.append(y)

        df = pd.DataFrame()
        df['Utility'] = utils
        df['Time'] = time
        df['gameId'] = gameId
        df['playId'] = playId








for x in all_data['gameId'].unique():

    for y in all_data['playId'].unique():

        df = all_data[all_data['gameId'] == x]
        df = df[df['playId'] == y]

        #print(df)
        

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
                gameId.append(x)
                playId.append(y)

                for a in dfs[z]['displayName'].unique():

                    print(a)

                    if a != 'football' and len(players[players['displayName'] == a]) > 0:

                        pos = players[players['displayName'] == a].iloc[0]['position']

                        if pos == 'CB' or pos == 'DE' or pos == 'NT' or pos == 'FS' or pos == 'SS' or pos == 'ILB' or pos == 'OLB':

                            marginals.append(marginal_utility(dfs[z],line_dataset, yac_dataset, prob_model, yac_model, position,a) - find_utility(dfs[z],line_dataset, yac_dataset, prob_model, yac_model, position))
                            positions.append(pos)
                            names.append(a)
                            gameIds.append(x)

                            mar_times.append(dfs[z].iloc[0]['time'])
                            playIds.append(y)

            
            all_play_utility_data = pd.DataFrame()
            all_play_marginal_data = pd.DataFrame()

            all_play_utility_data['gameId'] = gameId
            all_play_marginal_data['gameId'] = gameIds
            all_play_marginal_data['playId'] = playIds
         
            all_play_marginal_data['Name'] = names
            all_play_marginal_data['Positions'] = positions
            all_play_marginal_data['Marginal Utility'] = marginals
            all_play_marginal_data['Marginal Times'] = mar_times
            
            all_play_utility_data['playId'] = playId
            all_play_utility_data['Utility'] = utils
            all_play_utility_data['Time'] = time

            all_play_utility_data.to_csv("C:/Users/anime/Downloads/utility dataset update 1.csv")

            all_play_marginal_data.to_csv("C:/Users/anime/Downloads/marginal dataset update 1.csv")



            









all_play_utility_data = pd.DataFrame()

all_play_utility_data['gameId'] = gameId
all_play_utility_data['playId'] = playId
all_play_utility_data['Utility'] = utils
all_play_utility_data['Time'] = time

all_play_utility_data.to_csv("C:/Users/anime/Downloads/utility dataset.csv")





            
