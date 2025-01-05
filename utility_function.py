from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
from imblearn.over_sampling import SMOTE


def construct_probability_model(df):

    model = RandomForestClassifier(n_estimators = 100)

    df = df.fillna(0)


    X = df.drop(['Unnamed: 0','Outcome'], axis = 1)

    print(X.columns)
    y = df['Outcome']

    smote = SMOTE( sampling_strategy = 1.0, random_state=101)
    X, y = smote.fit_resample(X,y)

    model.fit(X,y)

    return model



def forecast_yac(df):

    model = RandomForestRegressor(n_estimators = 100)

    df = df.fillna(0)

    df = df[df['YAC'] >= 0]

    df = df.loc[(df!=0).any(axis=1)]

    X = df.drop(['Unnamed: 0','YAC', 'WR2', 'WR3', 'WR4','CB4','CB5','OLB3','OLB4','ILB3', 'TE2', 'TE3', 'DE4', 'RB2', 'CB3',
                'WR2S',  'CB4S','CB5S','OLB3S',  'DE4S', 'RB2S', 'CB3S',
                'WR2A',  'CB4A','CB5A', 'DE4A', 'RB2A', 'CB3A'], axis = 1)

    #X = df.drop('YAC', axis = 1)
    y = df['YAC']

    model.fit(X,y)

    return model

def marginal_calculate_aggregate_openness_percentage(play_df, displayName):

    sum = 0
    marginal = 0

    players = pd.read_csv("C:/Users/anime/Downloads/players.csv")


    for x in range(0, len(play_df)):

        if play_df.iloc[x]['displayName'] == displayName:

            marginal += play_df.iloc[x]['Adjusted Difference Maximum']

        if play_df.iloc[x]['closestplay'] == displayName:

            marginal += play_df.iloc[x]['distancefromweapon']

        if play_df.iloc[x]['displayName'] in play_df['closestplay'].unique() and play_df.iloc[x]['position'] != 'QB':



            sum += play_df.iloc[x]['Adjusted Difference Maximum']


        if play_df.iloc[x]['closestplay'] != 'test':

            if (play_df.iloc[x]['position'] == 'NT' or play_df.iloc[x]['position'] == 'DE' or play_df.iloc[x]['position'] == 'CB'
                or play_df.iloc[x]['position'] == 'FS' or play_df.iloc[x]['position'] == 'OLB' or play_df.iloc[x]['position'] == 'ILB' 
                and players[players['displayName'] == play_df.iloc[x]['closestplay']].iloc[0]['position'] != 'QB'):

                sum += play_df.iloc[x]['distancefromweapon']

    return marginal/sum
def calculate_aggregate_openness_percentage(play_df, displayName):

    sum = 0
    marginal = 0

    players = pd.read_csv("C:/Users/anime/Downloads/players.csv")


    for x in range(0, len(play_df)):

        if play_df.iloc[x]['displayName'] == displayName:

            marginal += play_df.iloc[x]['Adjusted Difference Maximum']

        if play_df.iloc[x]['closestplay'] == displayName:

            marginal += play_df.iloc[x]['distancefromweapon']

        if play_df.iloc[x]['displayName'] in play_df['closestplay'].unique() and play_df.iloc[x]['position'] != 'QB':

            sum += play_df.iloc[x]['Adjusted Difference Maximum']
        print(play_df.iloc[x]['closestplay'])

        if (play_df.iloc[x]['position'] == 'NT' or play_df.iloc[x]['position'] == 'DE' or play_df.iloc[x]['position'] == 'CB'
            or play_df.iloc[x]['position'] == 'FS' or play_df.iloc[x]['position'] == 'OLB' or play_df.iloc[x]['position'] == 'ILB' 
            and players[players['displayName'] == play_df.iloc[x]['closestplay']].iloc[0]['position'] != 'QB'):

            sum += play_df.iloc[x]['distancefromweapon']

    return marginal/sum





def find_utility(play_df, line_fitting_dataset, yac_dataset, prob_model, yac_model, los_x):

   # prob_model = construct_probability_model(line_fitting_dataset)
   # yac_model = forecast_yac(yac_dataset)

    

    play_df['distancefromweapon'] = 0
    play_df['closestplay'] = 'test'

    #print('done')

    #print("There are " + str(len(dfl[0])) + "rows")


    arr = []
    #names = []

    for i in range(0, len(play_df)):
        dist = 10000

           # print(len(x) - i)

        #    print(len(x))
            
        if play_df.iloc[i]['position'] == 'SS' or play_df.iloc[i]['position'] == 'CB' or play_df.iloc[i]['position'] == 'OLB' or play_df.iloc[i]['position'] == 'ILB' or play_df.iloc[i]['position'] == 'FS' or play_df.iloc[i]['position'] == 'NT' or play_df.iloc[i]['position'] == 'DE':
                
            for b in range(0, len(play_df)):

                if play_df.iloc[b]['position'] == 'QB' or play_df.iloc[b]['position'] == 'WR' or play_df.iloc[b]['position'] == 'TE' or play_df.iloc[b]['position'] == 'RB':
                        #print('hi')
                    euc = ((play_df.iloc[i]['x'] - play_df.iloc[b]['x'])**2 +(play_df.iloc[i]['y'] - play_df.iloc[b]['y'])**2)**0.5
                    if euc < dist:
                            #print(euc)
                        dist = euc
                      #  name = play_df.iloc[i]['displayName']
        #dist_arr.append(dist)

        arr.append(dist)
      #  names.append(name)


    
    
    play_df['distancefromweapon'] = arr

    arr = []
    

    dist = 0
    dist_arr = []

    for i in range(0, len(play_df)):
        dist = 10000
        name = 'test'
            
        if play_df.iloc[i]['position'] == 'SS' or play_df.iloc[i]['position'] == 'CB' or play_df.iloc[i]['position'] == 'OLB' or play_df.iloc[i]['position'] == 'ILB' or play_df.iloc[i]['position'] == 'FS' or play_df.iloc[i]['position'] == 'NT' or play_df.iloc[i]['position'] == 'DE':
                
            for b in range(0, len(play_df)):

                    if play_df.iloc[b]['position'] == 'QB' or play_df.iloc[b]['position'] == 'WR' or play_df.iloc[b]['position'] == 'TE' or play_df.iloc[b]['position'] == 'RB':
                       # print('hi')
                        euc = ((play_df.iloc[i]['x'] - play_df.iloc[b]['x'])**2 +(play_df.iloc[i]['y'] - play_df.iloc[b]['y'])**2)**0.5
                        if euc < dist:
                        #    print(euc)
                            dist = euc
                            name = play_df.iloc[b]['displayName']

        dist_arr.append(name)

    arr = dist_arr

    #for x in range(0, len(arr)):

    play_df['closestplay'] = arr

    #play_df['closestplay'] = names


    distance_sums = []
    

    dists = []

    for y in range(0, len(play_df['closestplay'].unique())):
        dist_sum = 0
        for z in range(0, len(play_df)):
             #   print(dfl[x].iloc[z]['closestplay'])
             #   print(dfl[x]['closestplay'].unique()[y])
            if play_df.iloc[z]['closestplay'] == play_df['closestplay'].unique()[y] and play_df.iloc[z]['closestplay'] != 'test':

                dist_sum += (play_df.iloc[z]['distancefromweapon'])

        dists.append(dist_sum)

    distance_sums = dists

    


    adjusted_distances = []

    

    dist = 0
    dist_arr = []

    for i in range(0, len(play_df)):
        dist = 10000
        vect = []
        dist_e = 0
        dist_w = 0
        dist_n = 0
        dist_s = 0
            
        if play_df.iloc[i]['position'] == 'SS' or play_df.iloc[i]['position'] == 'CB' or play_df.iloc[i]['position'] == 'OLB' or play_df.iloc[i]['position'] == 'ILB' or play_df.iloc[i]['position'] == 'FS' or play_df.iloc[i]['position'] == 'NT' or play_df.iloc[i]['position'] == 'DE':
                
            for b in range(0, len(play_df)):

                if play_df.iloc[b]['position'] == 'QB' or play_df.iloc[b]['position'] == 'WR' or play_df.iloc[b]['position'] == 'TE' or play_df.iloc[b]['position'] == 'RB':
                        #print('hi')
                    euc = ((play_df.iloc[i]['x'] - play_df.iloc[b]['x'])**2 +(play_df.iloc[i]['y'] - play_df.iloc[b]['y'])**2)**0.5
                    if euc < dist:
                         #   print(euc)
                        dist = euc
                        dist_n = ((play_df.iloc[i]['x'] - play_df.iloc[b]['x'])**2 +((play_df.iloc[i]['y']+1) - play_df.iloc[b]['y'])**2)**0.5
                        dist_s = ((play_df.iloc[i]['x'] - play_df.iloc[b]['x'])**2 +((play_df.iloc[i]['y']-1) - play_df.iloc[b]['y'])**2)**0.5
                        dist_e = (((play_df.iloc[i]['x'] + 1) - play_df.iloc[b]['x'])**2 +(play_df.iloc[i]['y'] - play_df.iloc[b]['y'])**2)**0.5
                        dist_w =(((play_df.iloc[i]['x'] - 1) - play_df.iloc[b]['x'])**2 +(play_df.iloc[i]['y'] - play_df.iloc[b]['y'])**2)**0.5

        vect.append(dist_n)
        vect.append(dist_s)
        vect.append(dist_e)
        vect.append(dist_w)

        dist_arr.append(vect)

    adjusted_distances = dist_arr

   

    play_df['adjusted_distances'] = adjusted_distances










    north_difference = []
    south_difference = []
    east_difference = []
    west_difference = []
    max_difference = []

    

    north_dist = []
    south_dist = []
    east_dist = []
    west_dist = []
    max_dist = []

    for y in range(0, len(play_df['closestplay'].unique())):
        north_sum = 0
        south_sum = 0
        east_sum = 0
        west_sum = 0
        for z in range(0, len(play_df)):
             #   print(dfl[x].iloc[z]['closestplay'])
              #  print(dfl[x]['closestplay'].unique()[y])
            if play_df.iloc[z]['closestplay'] == play_df['closestplay'].unique()[y] and play_df.iloc[z]['closestplay'] != 'test':

                north_sum += (np.abs(play_df.iloc[z]['distancefromweapon'] - play_df.iloc[z]['adjusted_distances'][0]))
                south_sum += (np.abs(play_df.iloc[z]['distancefromweapon'] - play_df.iloc[z]['adjusted_distances'][1]))
                east_sum += (np.abs(play_df.iloc[z]['distancefromweapon'] - play_df.iloc[z]['adjusted_distances'][2]))
                west_sum += (np.abs(play_df.iloc[z]['distancefromweapon'] - play_df.iloc[z]['adjusted_distances'][3]))

        north_dist.append(north_sum)
        south_dist.append(south_sum)
        east_dist.append(east_sum)
        west_dist.append(west_sum)
        max_dist.append(sum([north_sum, south_sum, east_sum, west_sum])/4)


    north_difference = north_dist
    south_difference = south_dist
    east_difference = east_dist
    west_difference = west_dist
    max_difference = max_dist

    








  

    array = []
    

    weapon_dictionary = {}

   
    for b in range(0, len(max_difference)):

        weapon_dictionary[play_df['closestplay'].unique()[b]] = max_difference[b]

    array.append(weapon_dictionary)

    



    

    dat = pd.DataFrame(list(weapon_dictionary.items()), columns = ['displayName', 'Adjusted Difference Maximum'])

    play_df = pd.merge(play_df, dat, on = 'displayName', how = 'left')

    players = pd.read_csv("C:/Users/anime/Downloads/players.csv")









    rows = []

    dataframe_columns = ['QB1', 'QB2', 'WR1', 'WR2', 'WR3', 'WR4', 'CB1', 'CB2', 'CB3', 'CB4', 'CB5', 
                     'OLB1', 'OLB2', 'OLB3', 'OLB4', 'ILB1', 'ILB2', 'ILB3',  'FS1', 'FS2', 'FS3', 
                     'NT1', 'NT2', 'TE1', 'TE2', 'TE3', 'DE1', 'DE2', 'DE3', 'DE4', 'RB1', 'RB2']

    copy = play_df.copy()
    row_dict = {}



    used_indexes = []
        
    for b in dataframe_columns:
        row_dict[b] = 0
        speed_column = b + 'S'
        acc_column = b + 'A'
        row_dict[speed_column] = 0
        row_dict[acc_column] = 0

            

            
            
        for c in range(0, len(copy)):

         

            

            if c not in used_indexes and copy.iloc[c]['position'] == b[:len(b) - 1] and (copy.iloc[c]['position'] == 'QB' or 
                                                                copy.iloc[c]['position'] == 'RB' or copy.iloc[c]['position'] == 'TE'
                                                                or copy.iloc[c]['position'] == 'WR'):


                row_dict[b] = copy.iloc[c]['Adjusted Difference Maximum']
                speed_column = b + 'S'
                acc_column = b + 'A'
                row_dict[speed_column] = copy.iloc[c]['s']
                row_dict[acc_column] = copy.iloc[c]['a']


                used_indexes.append(c)

                # copy.at[c, 'position'] = 'C'

                # print(copy.iloc[c]['position'])

                break

                    


            if c not in used_indexes and copy.iloc[c]['position'] == b[:len(b) - 1] and (copy.iloc[c]['position'] != 'QB' and
                                                                copy.iloc[c]['position'] != 'RB' and copy.iloc[c]['position'] != 'TE'
                                                                and copy.iloc[c]['position'] != 'WR' and copy.iloc[c]['position'] != 'T' and
                                                                copy.iloc[c]['position'] != 'G' and copy.iloc[c]['position'] != 'C'):
                    

                row_dict[b] = copy.iloc[c]['distancefromweapon']

                speed_column = b + 'S'
                acc_column = b + 'A'
                row_dict[speed_column] = copy.iloc[c]['s']
                row_dict[acc_column] = copy.iloc[c]['a']


                used_indexes.append(c)

                    #copy.at[c, 'position'] = 'C'
                break

                #copy.drop(c, inplace = True)

    rows.append(row_dict)

   # line_fitting_df = pd.DataFrame({'QB1':[], 'QB2':[], 'WR1':[], 'WR2':[], 'WR3':[], 'WR4':[], 'CB1':[], 'CB2':[], 'CB3':[], 'CB4':[], 'CB5':[], 
    ##                'NT1':[], 'NT2':[], 'TE1':[], 'TE2':[], 'TE3':[], 'DE1':[], 'DE2':[], 'DE3':[], 'DE4':[], 'RB1':[], 'RB2':[], 'Outcome':[]})
    
    line_fitting_df = pd.DataFrame.from_dict(rows, orient='columns')

    print(line_fitting_df.columns)

    line_fitting_df = line_fitting_df.reindex(columns = line_fitting_dataset.drop(['Outcome', 'Unnamed: 0'], axis = 1).columns)

    completion_probability = prob_model.predict_proba(line_fitting_df) 

    rows = []


    
    copy = play_df.copy()

    closestweapon_list = []

   

    for x in copy['closestplay'].unique():

        concat_list = []

        if x != 'test' and players[players['displayName'] == x].iloc[0]['position'] != 'QB':

            concat_list.append(copy[copy['displayName'] == x])
            concat_list.append(copy[copy['closestplay'] == x])
            closestweapon_list.append(pd.concat(concat_list, axis = 0))

    
    for x in closestweapon_list:

        copy = x.copy()


        row_dict = {}



        used_indexes = []
        dataframe_columns = ['WR1', 'WR2', 'WR3', 'WR4', 'CB1', 'CB2', 'CB3', 'CB4', 'CB5', 
                        'OLB1', 'OLB2', 'OLB3', 'OLB4', 'ILB1', 'ILB2', 'ILB3',  'FS1', 'FS2', 'FS3', 
                        'NT1', 'NT2', 'TE1', 'TE2', 'TE3', 'DE1', 'DE2', 'DE3', 'DE4', 'RB1', 'RB2', 'Name']
            
        for b in dataframe_columns:
            row_dict[b] = 0

            row_dict['Name'] = copy.iloc[0]['displayName']

            speed_column = b + 'S'
            acc_column = b + 'A'
            row_dict[speed_column] = 0
            row_dict[acc_column] = 0
          



                

        

                

                
            for c in range(0, len(copy)):



                    

                if c not in used_indexes and copy.iloc[c]['position'] == b[:len(b) - 1] and (copy.iloc[c]['position'] == 'QB' or 
                                                                        copy.iloc[c]['position'] == 'RB' or copy.iloc[c]['position'] == 'TE'
                                                                        or copy.iloc[c]['position'] == 'WR'):


                    row_dict[b] = copy.iloc[c]['Adjusted Difference Maximum']

                    speed_column = b + 'S'
                    acc_column = b + 'A'
                    row_dict[speed_column] = copy.iloc[c]['s']
                    row_dict[acc_column] = copy.iloc[c]['a']


                    used_indexes.append(c)

                        # copy.at[c, 'position'] = 'C'

                        # print(copy.iloc[c]['position'])

                    break

                            


                if c not in used_indexes and copy.iloc[c]['position'] == b[:len(b) - 1] and (copy.iloc[c]['position'] != 'QB' and
                                                                        copy.iloc[c]['position'] != 'RB' and copy.iloc[c]['position'] != 'TE'
                                                                        and copy.iloc[c]['position'] != 'WR' and copy.iloc[c]['position'] != 'T' and
                                                                        copy.iloc[c]['position'] != 'G' and copy.iloc[c]['position'] != 'C'):
                            

                    row_dict[b] = copy.iloc[c]['distancefromweapon']

                    speed_column = b + 'S'
                    acc_column = b + 'A'
                    row_dict[speed_column] = copy.iloc[c]['s']
                    row_dict[acc_column] = copy.iloc[c]['a']


                    used_indexes.append(c)

                            #copy.at[c, 'position'] = 'C'
                    break

                        #copy.drop(c, inplace = True)

        rows.append(row_dict)    
        


            

  

   # yac_df = pd.DataFrame({ 'WR1':[], 'WR2':[], 'WR3':[], 'WR4':[], 'CB1':[], 'CB2':[], 'CB3':[], 'CB4':[], 'CB5':[], 
    #                 'OLB1':[], 'OLB2':[], 'OLB3':[], 'OLB4':[], 'ILB1':[], 'ILB2':[], 'ILB3':[],  'FS1':[], 'FS2':[], 'FS3':[], 
     #                'NT1':[], 'NT2':[], 'TE1':[], 'TE2':[], 'TE3':[], 'DE1':[], 'DE2':[], 'DE3':[], 'DE4':[], 'RB1':[], 'RB2':[], 'YAC':[]})
    
    yac_df = pd.DataFrame.from_dict(rows, orient='columns')

    #yac_forecast = yac_model.predict(yac_df.drop('Name', axis = 1))

    play_data = pd.read_csv("C:/Users/anime/Downloads/plays.csv")
    players = pd.read_csv("C:/Users/anime/Downloads/players.csv")


    #print('play merging')

    plays = pd.DataFrame()

    plays['gameId'] = play_data['gameId']
    plays['playId'] = play_data['playId']
    plays['absoluteYardlineNumber'] = play_data['absoluteYardlineNumber']

    play_df =pd.merge(play_df, plays, how='left', on=['gameId', 'playId'])

    play_df['distancefromlos'] =  play_df['x'] - play_df['absoluteYardlineNumber']

    utility = 0



    for x in play_df['closestplay'].unique():
        #print(utility)



        if x != 'test' and players[players['displayName'] == x].iloc[0]['position'] != 'QB':

            
            play_df['distancefromlos'] = play_df['distancefromlos'].fillna(0)
            data = play_df[play_df['displayName'] == x]
            #print(data.iloc[0]['distancefromlos'])

            dist = float(data.iloc[0]['x']) - float(los_x)

            if data.iloc[0]['playDirection'] == 'left':

                dist = float(los_x) - float(data.iloc[0]['x'])
            #print(len(data))

            #print(type(completion_probability))
            #print(completion_probability[0][1])

            yac =yac_df[yac_df['Name'] == x].drop(['Name', 'NameS', 'NameA','WR2', 'WR3', 'WR4','CB4','CB5','OLB3','OLB4','ILB3', 'TE2', 'TE3', 'DE4', 'RB2', 'CB3',
                'WR2S',  'CB4S','CB5S','OLB3S',  'DE4S', 'RB2S', 'CB3S',
                'WR2A',  'CB4A','CB5A', 'DE4A', 'RB2A', 'CB3A', 'ILB3A', 'ILB3S', 'OLB4A', 'OLB4S', 'TE2A', 'TE2S',
                'TE3A', 'TE3S', 'WR3A', 'WR3S', 'WR4A', 'WR4S'], axis = 1).reindex(columns = yac_dataset.drop(['Unnamed: 0','YAC', 'WR2', 'WR3', 'WR4','CB4','CB5','OLB3','OLB4','ILB3', 'TE2', 'TE3', 'DE4', 'RB2', 'CB3',
                'WR2S',  'CB4S','CB5S','OLB3S',  'DE4S', 'RB2S', 'CB3S',
                'WR2A',  'CB4A','CB5A', 'DE4A', 'RB2A', 'CB3A'], axis = 1).columns)
            



            
            utility += completion_probability[0][1] * ((dist + yac_model.predict(yac)) * calculate_aggregate_openness_percentage(play_df, x))

    
    return utility


def extract_play_df_list(df):

   # df = pd.read_csv(week_data_path)

    

   # players = pd.read_csv("C:/Users/anime/Downloads/players.csv")

  #  df = pd.merge(df, pd.read_csv("C:/Users/anime/Downloads/players.csv"), on = 'displayName', how = 'left')

   # df = df[df['gameId'] == gameId]

   # df = df[df['playId'] == playId]

    df.reset_index(inplace = True)

    df['time'] = df['time'].astype(str).str.split().str[1]

    for x in range(0, len(df['time'])):

        print(x)

        print(len(df['time']))

        print(df['time'])

       # from datetime import datetime

        if '.' in df['time'][x]:

            df['time'][x] = (datetime.strptime(df['time'][x], "%H:%M:%S.%f") - datetime(1900, 1, 1)).total_seconds()

        else:

            df['time'][x] = (datetime.strptime(df['time'][x], "%H:%M:%S") - datetime(1900, 1, 1)).total_seconds()

   # print(df['time'].min())



    df['time'] = df['time'] - df['time'].min()

    df_list = []

    x_location = df[df['event'] == 'line_set'].iloc[0]['x']

    snap_time = df[df['event'] == 'ball_snap'].iloc[0]['time']

    

    df = df[df['time'] > snap_time]

    df['time'] = df['time'] - snap_time

    df['time'] = np.round(df['time'], 2)

    df = df.sort_values(by = 'time')
    copy = df.drop_duplicates(subset = ['time'])
    
    copy.reset_index(inplace = True)

    copy = copy["time"]

    df.reset_index(inplace=True)



    for x in range(0, len(copy), 10):

        df_list.append(df[df['time'] == copy[x]])

    

    return df_list


def marginal_utility(play_df, line_fitting_dataset, yac_dataset, prob_model, yac_model, los_x, player_name):

   # prob_model = construct_probability_model(line_fitting_dataset)
   # yac_model = forecast_yac(yac_dataset)

    

    play_df['distancefromweapon'] = 0
    play_df['closestplay'] = 'test'

    #print('done')

    #print("There are " + str(len(dfl[0])) + "rows")


    arr = []
    #names = []

    for i in range(0, len(play_df)):
        dist = 10000

           # print(len(x) - i)

        #    print(len(x))
            
        if play_df.iloc[i]['displayName'] != player_name and (play_df.iloc[i]['position'] == 'SS' or play_df.iloc[i]['position'] == 'CB' or play_df.iloc[i]['position'] == 'OLB' or play_df.iloc[i]['position'] == 'ILB' or play_df.iloc[i]['position'] == 'FS' or play_df.iloc[i]['position'] == 'NT' or play_df.iloc[i]['position'] == 'DE'):
                
            for b in range(0, len(play_df)):

                if play_df.iloc[b]['position'] == 'QB' or play_df.iloc[b]['position'] == 'WR' or play_df.iloc[b]['position'] == 'TE' or play_df.iloc[b]['position'] == 'RB':
                        #print('hi')
                    euc = ((play_df.iloc[i]['x'] - play_df.iloc[b]['x'])**2 +(play_df.iloc[i]['y'] - play_df.iloc[b]['y'])**2)**0.5
                    if euc < dist:
                            #print(euc)
                        dist = euc
                      #  name = play_df.iloc[i]['displayName']
        #dist_arr.append(dist)

        arr.append(dist)
      #  names.append(name)


    
    
    play_df['distancefromweapon'] = arr

    arr = []
    

    dist = 0
    dist_arr = []

    for i in range(0, len(play_df)):
        dist = 10000
        name = 'test'
            
        if play_df.iloc[i]['displayName'] != player_name and (play_df.iloc[i]['position'] == 'SS' or play_df.iloc[i]['position'] == 'CB' or play_df.iloc[i]['position'] == 'OLB' or play_df.iloc[i]['position'] == 'ILB' or play_df.iloc[i]['position'] == 'FS' or play_df.iloc[i]['position'] == 'NT' or play_df.iloc[i]['position'] == 'DE'):
                
            for b in range(0, len(play_df)):

                    if play_df.iloc[b]['position'] == 'QB' or play_df.iloc[b]['position'] == 'WR' or play_df.iloc[b]['position'] == 'TE' or play_df.iloc[b]['position'] == 'RB':
                       # print('hi')
                        euc = ((play_df.iloc[i]['x'] - play_df.iloc[b]['x'])**2 +(play_df.iloc[i]['y'] - play_df.iloc[b]['y'])**2)**0.5
                        if euc < dist:
                        #    print(euc)
                            dist = euc
                            name = play_df.iloc[b]['displayName']

        dist_arr.append(name)

    arr = dist_arr

    #for x in range(0, len(arr)):

    play_df['closestplay'] = arr

    #play_df['closestplay'] = names


    distance_sums = []
    

    dists = []

    for y in range(0, len(play_df['closestplay'].unique())):
        dist_sum = 0
        for z in range(0, len(play_df)):
             #   print(dfl[x].iloc[z]['closestplay'])
             #   print(dfl[x]['closestplay'].unique()[y])
            if play_df.iloc[z]['closestplay'] == play_df['closestplay'].unique()[y] and play_df.iloc[z]['closestplay'] != 'test':

                dist_sum += (play_df.iloc[z]['distancefromweapon'])

        dists.append(dist_sum)

    distance_sums = dists

    


    adjusted_distances = []

    

    dist = 0
    dist_arr = []

    for i in range(0, len(play_df)):
        dist = 10000
        vect = []
        dist_e = 0
        dist_w = 0
        dist_n = 0
        dist_s = 0
            
        if play_df.iloc[i]['displayName'] != player_name and (play_df.iloc[i]['position'] == 'SS' or play_df.iloc[i]['position'] == 'CB' or play_df.iloc[i]['position'] == 'OLB' or play_df.iloc[i]['position'] == 'ILB' or play_df.iloc[i]['position'] == 'FS' or play_df.iloc[i]['position'] == 'NT' or play_df.iloc[i]['position'] == 'DE'):
                
            for b in range(0, len(play_df)):

                if play_df.iloc[b]['position'] == 'QB' or play_df.iloc[b]['position'] == 'WR' or play_df.iloc[b]['position'] == 'TE' or play_df.iloc[b]['position'] == 'RB':
                        #print('hi')
                    euc = ((play_df.iloc[i]['x'] - play_df.iloc[b]['x'])**2 +(play_df.iloc[i]['y'] - play_df.iloc[b]['y'])**2)**0.5
                    if euc < dist:
                         #   print(euc)
                        dist = euc
                        dist_n = ((play_df.iloc[i]['x'] - play_df.iloc[b]['x'])**2 +((play_df.iloc[i]['y']+1) - play_df.iloc[b]['y'])**2)**0.5
                        dist_s = ((play_df.iloc[i]['x'] - play_df.iloc[b]['x'])**2 +((play_df.iloc[i]['y']-1) - play_df.iloc[b]['y'])**2)**0.5
                        dist_e = (((play_df.iloc[i]['x'] + 1) - play_df.iloc[b]['x'])**2 +(play_df.iloc[i]['y'] - play_df.iloc[b]['y'])**2)**0.5
                        dist_w =(((play_df.iloc[i]['x'] - 1) - play_df.iloc[b]['x'])**2 +(play_df.iloc[i]['y'] - play_df.iloc[b]['y'])**2)**0.5

        vect.append(dist_n)
        vect.append(dist_s)
        vect.append(dist_e)
        vect.append(dist_w)

        dist_arr.append(vect)

    adjusted_distances = dist_arr

   

    play_df['adjusted_distances'] = adjusted_distances










    north_difference = []
    south_difference = []
    east_difference = []
    west_difference = []
    max_difference = []

    

    north_dist = []
    south_dist = []
    east_dist = []
    west_dist = []
    max_dist = []

    for y in range(0, len(play_df['closestplay'].unique())):
        north_sum = 0
        south_sum = 0
        east_sum = 0
        west_sum = 0
        for z in range(0, len(play_df)):
             #   print(dfl[x].iloc[z]['closestplay'])
              #  print(dfl[x]['closestplay'].unique()[y])
            if play_df.iloc[z]['closestplay'] == play_df['closestplay'].unique()[y] and play_df.iloc[z]['closestplay'] != 'test':

                north_sum += (np.abs(play_df.iloc[z]['distancefromweapon'] - play_df.iloc[z]['adjusted_distances'][0]))
                south_sum += (np.abs(play_df.iloc[z]['distancefromweapon'] - play_df.iloc[z]['adjusted_distances'][1]))
                east_sum += (np.abs(play_df.iloc[z]['distancefromweapon'] - play_df.iloc[z]['adjusted_distances'][2]))
                west_sum += (np.abs(play_df.iloc[z]['distancefromweapon'] - play_df.iloc[z]['adjusted_distances'][3]))

        north_dist.append(north_sum)
        south_dist.append(south_sum)
        east_dist.append(east_sum)
        west_dist.append(west_sum)
        max_dist.append(sum([north_sum, south_sum, east_sum, west_sum])/4)


    north_difference = north_dist
    south_difference = south_dist
    east_difference = east_dist
    west_difference = west_dist
    max_difference = max_dist

    








  

    array = []
    

    weapon_dictionary = {}

   
    for b in range(0, len(max_difference)):

        weapon_dictionary[play_df['closestplay'].unique()[b]] = max_difference[b]

    array.append(weapon_dictionary)

    



    

    dat = pd.DataFrame(list(weapon_dictionary.items()), columns = ['displayName', 'Adjusted Difference Maximum'])

    play_df = pd.merge(play_df, dat, on = 'displayName', how = 'left')

    players = pd.read_csv("C:/Users/anime/Downloads/players.csv")









    rows = []

    dataframe_columns = ['QB1', 'QB2', 'WR1', 'WR2', 'WR3', 'WR4', 'CB1', 'CB2', 'CB3', 'CB4', 'CB5', 
                     'OLB1', 'OLB2', 'OLB3', 'OLB4', 'ILB1', 'ILB2', 'ILB3',  'FS1', 'FS2', 'FS3', 
                     'NT1', 'NT2', 'TE1', 'TE2', 'TE3', 'DE1', 'DE2', 'DE3', 'DE4', 'RB1', 'RB2']

    copy = play_df.copy()
    row_dict = {}



    used_indexes = []
        
    for b in dataframe_columns:
        row_dict[b] = 0

        speed_column = b + 'S'
        acc_column = b + 'A'
        row_dict[speed_column] = 0
        row_dict[acc_column] = 0



            

            
            
        for c in range(0, len(copy)):

         

            

            if c not in used_indexes and copy.iloc[c]['position'] == b[:len(b) - 1] and (copy.iloc[c]['position'] == 'QB' or 
                                                                copy.iloc[c]['position'] == 'RB' or copy.iloc[c]['position'] == 'TE'
                                                                or copy.iloc[c]['position'] == 'WR'):


                row_dict[b] = copy.iloc[c]['Adjusted Difference Maximum']

                speed_column = b + 'S'
                acc_column = b + 'A'
                row_dict[speed_column] = copy.iloc[c]['s']
                row_dict[acc_column] = copy.iloc[c]['a']

                used_indexes.append(c)

                # copy.at[c, 'position'] = 'C'

                # print(copy.iloc[c]['position'])

                break

                    


            if c not in used_indexes and copy.iloc[c]['displayName'] != player_name and copy.iloc[c]['position'] == b[:len(b) - 1] and (copy.iloc[c]['position'] != 'QB' and
                                                                copy.iloc[c]['position'] != 'RB' and copy.iloc[c]['position'] != 'TE'
                                                                and copy.iloc[c]['position'] != 'WR' and copy.iloc[c]['position'] != 'T' and
                                                                copy.iloc[c]['position'] != 'G' and copy.iloc[c]['position'] != 'C'):
                    

                row_dict[b] = copy.iloc[c]['distancefromweapon']

                speed_column = b + 'S'
                acc_column = b + 'A'
                row_dict[speed_column] = copy.iloc[c]['s']
                row_dict[acc_column] = copy.iloc[c]['a']

                used_indexes.append(c)

                    #copy.at[c, 'position'] = 'C'
                break

                #copy.drop(c, inplace = True)

    rows.append(row_dict)

    line_fitting_df = pd.DataFrame({'QB1':[], 'QB2':[], 'WR1':[], 'WR2':[], 'WR3':[], 'WR4':[], 'CB1':[], 'CB2':[], 'CB3':[], 'CB4':[], 'CB5':[], 
                     'OLB1':[], 'OLB2':[], 'OLB3':[], 'OLB4':[], 'ILB1':[], 'ILB2':[], 'ILB3':[],  'FS1':[], 'FS2':[], 'FS3':[], 
                     'NT1':[], 'NT2':[], 'TE1':[], 'TE2':[], 'TE3':[], 'DE1':[], 'DE2':[], 'DE3':[], 'DE4':[], 'RB1':[], 'RB2':[], 'Outcome':[]})
    
    line_fitting_df = pd.DataFrame.from_dict(rows, orient='columns')

    line_fitting_df = line_fitting_df.reindex(columns = line_fitting_dataset.drop(['Outcome', 'Unnamed: 0'], axis = 1).columns)

    completion_probability = prob_model.predict_proba(line_fitting_df) 

    rows = []


    
    copy = play_df.copy()

    closestweapon_list = []

   

    for x in copy['closestplay'].unique():

        concat_list = []

        if x != 'test' and players[players['displayName'] == x].iloc[0]['position'] != 'QB':

            concat_list.append(copy[copy['displayName'] == x])
            concat_list.append(copy[copy['closestplay'] == x])
            closestweapon_list.append(pd.concat(concat_list, axis = 0))

    
    for x in closestweapon_list:

        copy = x.copy()


        row_dict = {}



        used_indexes = []
        dataframe_columns = ['WR1', 'WR2', 'WR3', 'WR4', 'CB1', 'CB2', 'CB3', 'CB4', 'CB5', 
                        'OLB1', 'OLB2', 'OLB3', 'OLB4', 'ILB1', 'ILB2', 'ILB3',  'FS1', 'FS2', 'FS3', 
                        'NT1', 'NT2', 'TE1', 'TE2', 'TE3', 'DE1', 'DE2', 'DE3', 'DE4', 'RB1', 'RB2', 'Name']
            
        for b in dataframe_columns:
            row_dict[b] = 0

            row_dict['Name'] = copy.iloc[0]['displayName']

            speed_column = b + 'S'
            acc_column = b + 'A'
            row_dict[speed_column] = 0
            row_dict[acc_column] = 0
          



                

        

                

                
            for c in range(0, len(copy)):



                    

                if c not in used_indexes and copy.iloc[c]['position'] == b[:len(b) - 1] and (copy.iloc[c]['position'] == 'QB' or 
                                                                        copy.iloc[c]['position'] == 'RB' or copy.iloc[c]['position'] == 'TE'
                                                                        or copy.iloc[c]['position'] == 'WR'):


                    row_dict[b] = copy.iloc[c]['Adjusted Difference Maximum']

                    speed_column = b + 'S'
                    acc_column = b + 'A'
                    row_dict[speed_column] = copy.iloc[c]['s']
                    row_dict[acc_column] = copy.iloc[c]['a']

                    used_indexes.append(c)

                        # copy.at[c, 'position'] = 'C'

                        # print(copy.iloc[c]['position'])

                    break

                            


                if c not in used_indexes and copy.iloc[c]['displayName'] != player_name and copy.iloc[c]['position'] == b[:len(b) - 1] and (copy.iloc[c]['position'] != 'QB' and
                                                                        copy.iloc[c]['position'] != 'RB' and copy.iloc[c]['position'] != 'TE'
                                                                        and copy.iloc[c]['position'] != 'WR' and copy.iloc[c]['position'] != 'T' and
                                                                        copy.iloc[c]['position'] != 'G' and copy.iloc[c]['position'] != 'C'):
                            

                    row_dict[b] = copy.iloc[c]['distancefromweapon']

                    speed_column = b + 'S'
                    acc_column = b + 'A'
                    row_dict[speed_column] = copy.iloc[c]['s']
                    row_dict[acc_column] = copy.iloc[c]['a']

                    used_indexes.append(c)

                            #copy.at[c, 'position'] = 'C'
                    break

                        #copy.drop(c, inplace = True)

        rows.append(row_dict)    
        


            

  

    yac_df = pd.DataFrame({ 'WR1':[], 'WR2':[], 'WR3':[], 'WR4':[], 'CB1':[], 'CB2':[], 'CB3':[], 'CB4':[], 'CB5':[], 
                     'OLB1':[], 'OLB2':[], 'OLB3':[], 'OLB4':[], 'ILB1':[], 'ILB2':[], 'ILB3':[],  'FS1':[], 'FS2':[], 'FS3':[], 
                     'NT1':[], 'NT2':[], 'TE1':[], 'TE2':[], 'TE3':[], 'DE1':[], 'DE2':[], 'DE3':[], 'DE4':[], 'RB1':[], 'RB2':[], 'YAC':[]})
    
    yac_df = pd.DataFrame.from_dict(rows, orient='columns')

    #yac_forecast = yac_model.predict(yac_df.drop('Name', axis = 1))

    play_data = pd.read_csv("C:/Users/anime/Downloads/plays.csv")
    players = pd.read_csv("C:/Users/anime/Downloads/players.csv")


    #print('play merging')

    plays = pd.DataFrame()

    plays['gameId'] = play_data['gameId']
    plays['playId'] = play_data['playId']
    plays['absoluteYardlineNumber'] = play_data['absoluteYardlineNumber']

    play_df =pd.merge(play_df, plays, how='left', on=['gameId', 'playId'])

    play_df['distancefromlos'] =  play_df['x'] - play_df['absoluteYardlineNumber']

    utility = 0



    for x in play_df['closestplay'].unique():
        #print(utility)

        check = 0

        for a in range(0, len(play_df[play_df['closestplay'] == x])):

            if play_df[play_df['closestplay'] == x].iloc[a]['displayName'] == player_name:

                check = 1



        if check == 0 and players[players['displayName'] == x].iloc[0]['position'] != 'QB':

            
            play_df['distancefromlos'] = play_df['distancefromlos'].fillna(0)
            data = play_df[play_df['displayName'] == x]
            #print(data.iloc[0]['distancefromlos'])

            dist = float(data.iloc[0]['x']) - float(los_x)

            if data.iloc[0]['playDirection'] == 'left':

                dist = float(los_x) - float(data.iloc[0]['x'])
            #print(len(data))

            #print(type(completion_probability))
            #print(completion_probability[0][1])

            yac =yac_df[yac_df['Name'] == x].drop(['Name', 'NameS', 'NameA','WR2', 'WR3', 'WR4','CB4','CB5','OLB3','OLB4','ILB3', 'TE2', 'TE3', 'DE4', 'RB2', 'CB3',
                'WR2S',  'CB4S','CB5S','OLB3S',  'DE4S', 'RB2S', 'CB3S',
                'WR2A',  'CB4A','CB5A', 'DE4A', 'RB2A', 'CB3A', 'ILB3A', 'ILB3S', 'OLB4A', 'OLB4S', 'TE2A', 'TE2S',
                'TE3A', 'TE3S', 'WR3A', 'WR3S', 'WR4A', 'WR4S'], axis = 1).reindex(columns = yac_dataset.drop(['Unnamed: 0','YAC', 'WR2', 'WR3', 'WR4','CB4','CB5','OLB3','OLB4','ILB3', 'TE2', 'TE3', 'DE4', 'RB2', 'CB3',
                'WR2S',  'CB4S','CB5S','OLB3S',  'DE4S', 'RB2S', 'CB3S',
                'WR2A',  'CB4A','CB5A', 'DE4A', 'RB2A', 'CB3A'], axis = 1).columns)
            



            
            utility += completion_probability[0][1] * ((dist + yac_model.predict(yac)) * marginal_calculate_aggregate_openness_percentage(play_df, x))

    
            



            
            
    return utility
















































