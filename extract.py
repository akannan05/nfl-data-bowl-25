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

def euc_distance(pos1, pos2):
    dist = []
    for p in range(len(pos1)):
        dist.append(math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2))
    return dist

def findclosest(defense, weapons):
    '''
    input: list of defense players at a specific play, list of weapons at a specific player
    output: new defense list with modified dfs containing info on closest weapon for each defender 
    '''
    pos_weapons = []
    pos_defense = []
    new_defense = []
    for w in weapons:
        pos_weapons.append(w[['name', 'player_x', 'player_y']])
    for d in defense:
        pos_defense.append(d[['name', 'player_x', 'player_y']])
        
    # for defense_position in pos_defense:
    #     dist_each_weapon = []
    #     pos1 =  
    #     for weapon_position in pos_weapons:
            
    
    return new_defense
    
    
def main():
    extractlist = extract(2022091200, 109)
    
    defense = separate(extractlist)[0]
    weapons = separate(extractlist)[1]
    
    defense = findclosest(defense, weapons)
        
if __name__ == "__main__":
    main()