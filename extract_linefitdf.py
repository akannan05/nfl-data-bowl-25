import pandas as pd
import numpy as np
paths = ["C:/Users/anime/Downloads/tracking_week_1.csv"]
paths = ["C:/Users/anime/Downloads/tracking_week_1.csv", "C:/Users/anime/Downloads/tracking_week_2.csv", "C:/Users/anime/Downloads/tracking_week_3.csv",
         "C:/Users/anime/Downloads/tracking_week_4.csv", "C:/Users/anime/Downloads/tracking_week_5.csv", "C:/Users/anime/Downloads/tracking_week_6.csv",
         "C:/Users/anime/Downloads/tracking_week_7.csv","C:/Users/anime/Downloads/tracking_week_8.csv","C:/Users/anime/Downloads/tracking_week_9.csv"]

list_of_line_fitting_dfs = []

for path in paths:

    print(path)

    week_1 = pd.read_csv(path)
    week_1_complete = week_1[week_1['event'] == 'pass_outcome_caught']
    week_1_incomplete = week_1[week_1['event'] == 'pass_outcome_incomplete']

    players = pd.read_csv("C:/Users/anime/Downloads/players.csv")
    df_one = pd.concat([week_1_complete,week_1_incomplete])
    df_one = pd.merge(df_one,players,on='displayName',how='left')


    df_list = []

    for x in df_one['playId'].unique():

        df_list.append(df_one[df_one['playId'] == x])

    dfs = []
    for x in df_list:

        for y in x['gameId'].unique():

            dfs.append(x[x['gameId'] == y])

    dfl = []

    for x in dfs:

        dfl.append(x[x['displayName'] != 'football'])

    
    for x in range(0, len(dfl)):

        dfl[x]['distancefromweapon'] = 0


    arr = []
    for x in dfl:

        dist = 0
        dist_arr = []

        for i in range(0, len(x)):
            dist = 10000
            
            if x.iloc[i]['position'] == 'SS' or x.iloc[i]['position'] == 'CB' or x.iloc[i]['position'] == 'OLB' or x.iloc[i]['position'] == 'ILB' or x.iloc[i]['position'] == 'FS' or x.iloc[i]['position'] == 'NT' or x.iloc[i]['position'] == 'DE':
                
                for b in range(0, len(x)):

                    if x.iloc[b]['position'] == 'QB' or x.iloc[b]['position'] == 'WR' or x.iloc[b]['position'] == 'TE' or x.iloc[b]['position'] == 'RB':
                        #print('hi')
                        euc = ((x.iloc[i]['x'] - x.iloc[b]['x'])**2 +(x.iloc[i]['y'] - x.iloc[b]['y'])**2)**0.5
                        if euc < dist:
                            #print(euc)
                            dist = euc
            dist_arr.append(dist)

        arr.append(dist_arr)

    for x in range(0, len(arr)):

        dfl[x]['distancefromweapon'] = arr[x]









    for x in range(0, len(dfl)):

        dfl[x]['closestplay'] = 'test'

    
    arr = []
    for x in dfl:

        dist = 0
        dist_arr = []

        for i in range(0, len(x)):
            dist = 10000
            name = 'test'
            
            if x.iloc[i]['position'] == 'SS' or x.iloc[i]['position'] == 'CB' or x.iloc[i]['position'] == 'OLB' or x.iloc[i]['position'] == 'ILB' or x.iloc[i]['position'] == 'FS' or x.iloc[i]['position'] == 'NT' or x.iloc[i]['position'] == 'DE':
                
                for b in range(0, len(x)):

                    if x.iloc[b]['position'] == 'QB' or x.iloc[b]['position'] == 'WR' or x.iloc[b]['position'] == 'TE' or x.iloc[b]['position'] == 'RB':
                       # print('hi')
                        euc = ((x.iloc[i]['x'] - x.iloc[b]['x'])**2 +(x.iloc[i]['y'] - x.iloc[b]['y'])**2)**0.5
                        if euc < dist:
                        #    print(euc)
                            dist = euc
                            name = x.iloc[b]['displayName']

            dist_arr.append(name)

        arr.append(dist_arr)

    for x in range(0, len(arr)):

        dfl[x]['closestplay'] = arr[x]

    





    distance_sums = []
    for x in range(0, len(dfl)):

        dists = []

        for y in range(0, len(dfl[x]['closestplay'].unique())):
            dist_sum = 0
            for z in range(0, len(dfl[x])):
             #   print(dfl[x].iloc[z]['closestplay'])
             #   print(dfl[x]['closestplay'].unique()[y])
                if dfl[x].iloc[z]['closestplay'] == dfl[x]['closestplay'].unique()[y] and dfl[x].iloc[z]['closestplay'] != 'test':

                    dist_sum += (dfl[x].iloc[z]['distancefromweapon'])

            dists.append(dist_sum)

        distance_sums.append(dists)

    


    adjusted_distances = []

    for x in dfl:

        dist = 0
        dist_arr = []

        for i in range(0, len(x)):
            dist = 10000
            vect = []
            dist_e = 0
            dist_w = 0
            dist_n = 0
            dist_s = 0
            
            if x.iloc[i]['position'] == 'SS' or x.iloc[i]['position'] == 'CB' or x.iloc[i]['position'] == 'OLB' or x.iloc[i]['position'] == 'ILB' or x.iloc[i]['position'] == 'FS' or x.iloc[i]['position'] == 'NT' or x.iloc[i]['position'] == 'DE':
                
                for b in range(0, len(x)):

                    if x.iloc[b]['position'] == 'QB' or x.iloc[b]['position'] == 'WR' or x.iloc[b]['position'] == 'TE' or x.iloc[b]['position'] == 'RB':
                        #print('hi')
                        euc = ((x.iloc[i]['x'] - x.iloc[b]['x'])**2 +(x.iloc[i]['y'] - x.iloc[b]['y'])**2)**0.5
                        if euc < dist:
                         #   print(euc)
                            dist = euc
                            dist_n = ((x.iloc[i]['x'] - x.iloc[b]['x'])**2 +((x.iloc[i]['y']+1) - x.iloc[b]['y'])**2)**0.5
                            dist_s = ((x.iloc[i]['x'] - x.iloc[b]['x'])**2 +((x.iloc[i]['y']-1) - x.iloc[b]['y'])**2)**0.5
                            dist_e = (((x.iloc[i]['x'] + 1) - x.iloc[b]['x'])**2 +(x.iloc[i]['y'] - x.iloc[b]['y'])**2)**0.5
                            dist_w =(((x.iloc[i]['x'] - 1) - x.iloc[b]['x'])**2 +(x.iloc[i]['y'] - x.iloc[b]['y'])**2)**0.5

            vect.append(dist_n)
            vect.append(dist_s)
            vect.append(dist_e)
            vect.append(dist_w)

            dist_arr.append(vect)

        adjusted_distances.append(dist_arr)

    for x in range(0, len(adjusted_distances)):

        dfl[x]['adjusted_distances'] = adjusted_distances[x]

    





















    north_difference = []
    south_difference = []
    east_difference = []
    west_difference = []
    max_difference = []

    for x in range(0, len(dfl)):

        north_dist = []
        south_dist = []
        east_dist = []
        west_dist = []
        max_dist = []

        for y in range(0, len(dfl[x]['closestplay'].unique())):
            north_sum = 0
            south_sum = 0
            east_sum = 0
            west_sum = 0
            for z in range(0, len(dfl[x])):
             #   print(dfl[x].iloc[z]['closestplay'])
              #  print(dfl[x]['closestplay'].unique()[y])
                if dfl[x].iloc[z]['closestplay'] == dfl[x]['closestplay'].unique()[y] and dfl[x].iloc[z]['closestplay'] != 'test':

                    north_sum += (np.abs(dfl[x].iloc[z]['distancefromweapon'] - dfl[x].iloc[z]['adjusted_distances'][0]))
                    south_sum += (np.abs(dfl[x].iloc[z]['distancefromweapon'] - dfl[x].iloc[z]['adjusted_distances'][1]))
                    east_sum += (np.abs(dfl[x].iloc[z]['distancefromweapon'] - dfl[x].iloc[z]['adjusted_distances'][2]))
                    west_sum += (np.abs(dfl[x].iloc[z]['distancefromweapon'] - dfl[x].iloc[z]['adjusted_distances'][3]))

            north_dist.append(north_sum)
            south_dist.append(south_sum)
            east_dist.append(east_sum)
            west_dist.append(west_sum)
            max_dist.append(max([north_sum, south_sum, east_sum, west_sum]))


        north_difference.append(north_dist)
        south_difference.append(south_dist)
        east_difference.append(east_dist)
        west_difference.append(west_dist)
        max_difference.append(max_dist)

    










    array = []
    for a in range(0, len(dfl)):

        weapon_dictionary = {}

        for b in range(0, len(max_difference[a])):

            weapon_dictionary[dfl[a]['closestplay'].unique()[b]] = max_difference[a][b]

        array.append(weapon_dictionary)

    



    for a in range(0, len(dfl)):

        dat = pd.DataFrame(list(array[a].items()), columns = ['displayName', 'Adjusted Difference Maximum'])

        dfl[a] = pd.merge(dfl[a], dat, on = 'displayName', how = 'left')


    







    play_data = pd.read_csv("C:/Users/anime/Downloads/plays.csv")




    plays = pd.DataFrame()

    plays['gameId'] = play_data['gameId']
    plays['playId'] = play_data['playId']
    plays['absoluteYardlineNumber'] = play_data['absoluteYardlineNumber']

    all_plays = pd.concat(dfl, axis = 0)


    final_data =pd.merge(all_plays, plays, how='left', on=['gameId', 'playId'])

    final_data['distancefromlos'] = final_data['absoluteYardlineNumber'] - final_data['y']

    player_play = pd.read_csv("C:/Users/anime/Downloads/player_play.csv")

    final_data['nflId'] = final_data['nflId_x']

    final_data = pd.merge(final_data, player_play, on = ['gameId', 'playId', 'nflId'], how = 'left')

    play_list = []

    for x in final_data['playId'].unique():

        play_list.append(final_data[final_data['playId'] == x])


    list_of_plays = []
    for x in play_list:

        for y in x['gameId'].unique():

            list_of_plays.append(x[x['gameId'] == y])

    

    dataframe_columns = ['QB1', 'QB2', 'WR1', 'WR2', 'WR3', 'WR4', 'CB1', 'CB2', 'CB3', 'CB4', 'CB5', 
                     'OLB1', 'OLB2', 'OLB3', 'OLB4', 'ILB1', 'ILB2', 'ILB3',  'FS1', 'FS2', 'FS3', 
                     'NT1', 'NT2', 'TE1', 'TE2', 'TE3', 'DE1', 'DE2', 'DE3', 'DE4', 'RB1', 'RB2', 'Outcome']
    







    rows = []
    for a in range(0, len(list_of_plays)):
        copy = list_of_plays[a].copy()
        row_dict = {}



        used_indexes = []
        
        for b in dataframe_columns:
            row_dict[b] = 0

            

            
            
            for c in range(0, len(copy)):

                if copy.iloc[c]['event'] == 'pass_outcome_caught':

                  #  print(1)

                    row_dict['Outcome'] = 1

                if copy.iloc[c]['event'] == 'pass_outcome_incomplete':

                 #   print(0)

                    row_dict['Outcome'] = 0

            

                if c not in used_indexes and copy.iloc[c]['position'] == b[:len(b) - 1] and (copy.iloc[c]['position'] == 'QB' or 
                                                                copy.iloc[c]['position'] == 'RB' or copy.iloc[c]['position'] == 'TE'
                                                                or copy.iloc[c]['position'] == 'WR'):


                    row_dict[b] = copy.iloc[c]['Adjusted Difference Maximum']

                    used_indexes.append(c)

                # copy.at[c, 'position'] = 'C'

                # print(copy.iloc[c]['position'])

                    break

                    


                if c not in used_indexes and copy.iloc[c]['position'] == b[:len(b) - 1] and (copy.iloc[c]['position'] != 'QB' and
                                                                copy.iloc[c]['position'] != 'RB' and copy.iloc[c]['position'] != 'TE'
                                                                and copy.iloc[c]['position'] != 'WR' and copy.iloc[c]['position'] != 'T' and
                                                                copy.iloc[c]['position'] != 'G' and copy.iloc[c]['position'] != 'C'):
                    

                    row_dict[b] = copy.iloc[c]['distancefromweapon']

                    used_indexes.append(c)

                    #copy.at[c, 'position'] = 'C'
                    break

                #copy.drop(c, inplace = True)

        rows.append(row_dict)    
        


            

  

    line_fitting_df = pd.DataFrame({'QB1':[], 'QB2':[], 'WR1':[], 'WR2':[], 'WR3':[], 'WR4':[], 'CB1':[], 'CB2':[], 'CB3':[], 'CB4':[], 'CB5':[], 
                     'OLB1':[], 'OLB2':[], 'OLB3':[], 'OLB4':[], 'ILB1':[], 'ILB2':[], 'ILB3':[],  'FS1':[], 'FS2':[], 'FS3':[], 
                     'NT1':[], 'NT2':[], 'TE1':[], 'TE2':[], 'TE3':[], 'DE1':[], 'DE2':[], 'DE3':[], 'DE4':[], 'RB1':[], 'RB2':[], 'Outcome':[]})
    
    line_fitting_df = pd.DataFrame.from_dict(rows, orient='columns')


    #line_fitting_df.to_csv("C:/Users/anime/Downloads/week 1 pass probability training.csv")

    list_of_line_fitting_dfs.append(line_fitting_df)




line_dataset = pd.concat(list_of_line_fitting_dfs, axis=0)

line_dataset.to_csv("C:/Users/anime/Downloads/line fitting data.csv")
    


            








    

#copy.reset_index(inplace = False)

        







    















            











