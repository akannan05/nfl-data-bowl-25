import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from utility_function import *



line_dataset = pd.read_csv("C:/Users/anime/Downloads/line fitting data.csv")

yac_dataset = pd.read_csv("C:/Users/anime/Downloads/yac data.csv")




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

paths = ["C:/Users/anime/Downloads/tracking_week_1.csv"]
data_list = []

for x in paths:

    data_list.append(pd.read_csv(x))

    print(x)



all_data = pd.concat(data_list, axis = 0)

print(all_data)

gameId = []
playId = []
time = []
utils = []


for x in all_data['gameId'].unique():

    for y in all_data['playId'].unique():

        df = all_data[all_data['gameId'] == x]
        df = df[df['playId'] == y]

        #print(df)
        

        if ('pass_outcome_caught' in df['event'].unique() or 'pass_outcome_incomplete' in df['event'].unique()
        or 'interception' in df['event'].unique()) and ('line_set' in df['event'].unique() and 'ball_snap' in df['event'].unique()):
            
            print('hello')
       
            position = df[df['displayName'] == 'football'][df['event'] == 'ball_snap'].iloc[0]['x']

            dfs = extract_play_df_list(week_data_path=paths[0], gameId = x, playId = y)

            for z in dfs:

                utils.append(find_utility(z,line_dataset, yac_dataset, prob_model, yac_model, position))
                time.append(z.iloc[0]['time'])
                gameId.append(x)
                playId.append(y)

            
            all_play_utility_data = pd.DataFrame()

            all_play_utility_data['gameId'] = gameId
            all_play_utility_data['playId'] = playId
            all_play_utility_data['Utility'] = utils
            all_play_utility_data['Time'] = time

            all_play_utility_data.to_csv("C:/Users/anime/Downloads/utility dataset.csv")

            









all_play_utility_data = pd.DataFrame()

all_play_utility_data['gameId'] = gameId
all_play_utility_data['playId'] = playId
all_play_utility_data['Utility'] = utils
all_play_utility_data['Time'] = time

all_play_utility_data.to_csv("C:/Users/anime/Downloads/utility dataset.csv")





            
