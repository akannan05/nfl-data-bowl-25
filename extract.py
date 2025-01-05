import pandas as pd
import numpy as np
import math

import matplotlib.pyplot as plt

week_1 = pd.read_csv('data/tracking_week_1.csv')
players = pd.read_csv('data/players.csv')

def extract(gameId, playId):
    myGame = week_1[week_1['gameId'] == gameId]
    myPlay = myGame[myGame['playId'] == playId]
    
    everyone = []
    playerList = myPlay['displayName'].unique()
    playerList = np.delete(playerList, playerList.size - 1)
    
    for player in playerList:
        player_info = players[players['displayName'] == player]
        player_data = myPlay[myPlay['displayName'] == player]
        cleaned_player_data = pd.DataFrame({
            'name': player_info['displayName'],
            'position': player_info['position'],
            'player_x': player_data['x'],
            'player_y': player_data['y'],
            'player_a': player_data['a'],
            'player_s': player_data['s'],
            'player_dir': player_data['dir'],
            'player_dis': player_data['dis'],   
            'outcome': player_data['event']
        })
        everyone.append(cleaned_player_data)
    
    return everyone

def separate(totallist):
    '''
    input: list of dataframes of every player's in a specific play
    output: array [defensive players, weapon players, offensive players]
    note: we define weapon players as 'QB', 'RB', 'WR', 'TE'
    '''
    offenselist = []
    defenselist = []
    weaponlist = []
    
    for jit in totallist:
        jit[['name', 'position']] = jit[['name', 'position']].ffill()
        jit = jit.iloc[1:]
        jit = jit.reset_index(drop=True)
        jit.index = range(1, len(jit) + 1)
        if jit.at[1, 'position'] in ['QB', 'RB', 'WR', 'G', 'TE', 'C', 'T']:
             offenselist.append(jit)
        else:
             defenselist.append(jit)
             
    for jit in offenselist:
        if jit.at[1, 'position'] in ['QB', 'RB', 'WR', 'TE']:
            weaponlist.append(jit)
             
    return defenselist, weaponlist, offenselist

def proto_euc_distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def findclosest(defense, weapons):
    '''
    input: list of defense players at a specific play, list of weapons at a specific player
    output: new defense list with modified dfs containing info on closest weapon for each defender 
    '''
    pos_defense = []
    pos_weapon = []
    for d in defense:
        pos_defense.append(d[['name', 'player_x', 'player_y']])
    for w in weapons:
        pos_weapon.append(w[['name', 'player_x', 'player_y']])
    
    pos_each_def = []
    pos_each_weap = []

    for pos in pos_defense:
        new_df = pd.DataFrame({'euc_position': [list(xy) for xy in zip(pos['player_x'], pos['player_y'])]})
        new_df['name'] = pos.at[1, 'name']
        new_df = new_df[['name', 'euc_position']]
        pos_each_def.append(new_df)
        
    for pos in pos_weapon:
        new_df = pd.DataFrame({'euc_position': [list(xy) for xy in zip(pos['player_x'], pos['player_y'])]})
        new_df['name'] = pos.at[1, 'name']
        new_df = new_df[['name', 'euc_position']]
        pos_each_weap.append(new_df)
        
    num_weps = len(pos_each_weap)
    defs_and_distances_total = []
    for p_def in pos_each_def:
        pos_def_to_wep = []
        for w_def in pos_each_weap:
            combine = pd.DataFrame({
                'name_def': p_def['name'],
                'pos_def': p_def['euc_position'],
                'name_wep': w_def['name'],
                'pos_wep': w_def['euc_position']
            })
            combine['distance'] = combine.apply(lambda row: proto_euc_distance(row['pos_def'], row['pos_wep']), axis=1)
            pos_def_to_wep.append(combine)
        min_distances = []
        min_distances_weps = []
        for i in range(pos_def_to_wep[0].shape[0]):
            min_distance = 130**2  # some distance that is greater than the football field
            min_distance_wep = ""
            for k in range(num_weps):
                if pos_def_to_wep[k].at[i, 'distance'] < min_distance:
                    min_distance = pos_def_to_wep[k].at[i, 'distance']
                    min_distance_wep = pos_def_to_wep[k].at[i, 'name_wep'] 
            min_distances.append(min_distance)
            min_distances_weps.append(min_distance_wep)
        defs_and_distances = pd.DataFrame({
            'name_def': p_def['name'],
            'pos_def': p_def['euc_position'],
            'min_distance_wep': min_distances_weps,
            'min_distance': min_distances,
        })        
        defs_and_distances_total.append(defs_and_distances)
        
    merged_defenders = []
    for idx, df in enumerate(defs_and_distances_total):
        df_t = defense[idx]
        df_t = df_t.merge(df, left_index=True, right_index=True)
        merged_defenders.append(df_t)
        
    return merged_defenders
    
    
def main():
    extractlist = extract(2022091200, 109)
    
    defense = separate(extractlist)[0]
    weapons = separate(extractlist)[1]
    
    # defense = findclosest(defense, weapons)
        
if __name__ == "__main__":
    main()