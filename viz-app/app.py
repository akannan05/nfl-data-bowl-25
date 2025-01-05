from flask import Flask, request, send_file, render_template_string

import matplotlib.pyplot as plt 
import matplotlib.animation as anim 
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D

import numpy as np 
import pandas as pd 
import os 
import io 

import appextract 

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <form action="/generate" method="post">
        <label for="week">Week Number:</label>
        <input type="text" id="week" name="weeknum"><br><br>
        <label for="game">Game ID:</label>
        <input type="number" id="game" name="gameid"><br><br>
        <label for="play">Play ID:</label>
        <input type="number" id="play" name="playid"><br><br>
        <input type="submit" value="Generate Animation">
    </form>
    '''
    
def clean_data(week, game, play):
    extractlist = appextract.extract(week, game, play)
    
    defense = appextract.separate(extractlist)[0]
    offense = appextract.separate(extractlist)[2]
    
    football = appextract.footballdata(week, game, play)
    football.reset_index(drop=True, inplace=True)
    football.index = range(1, len(football) + 1)
    
    football_x = football['x']
    football_y = football['y']
    
    d_names = []
    o_names = []
    for d in defense:
        d_names.append(d.at[1, 'name'])

    for o in offense:
        o_names.append(o.at[1, 'name'])
        
    d_xy = []
    o_xy = []

    for player_name in d_names:
        defense_df = next(df for df in defense if df['name'].iloc[0] == player_name)
        xy_to_append = defense_df[['player_x', 'player_y']]
        d_xy.append(xy_to_append)
        
    for player_name in o_names:
        offense_df = next(df for df in offense if df['name'].iloc[0] == player_name)
        xy_to_append = offense_df[['player_x', 'player_y']]
        o_xy.append(xy_to_append)
        
    dx_list = []
    dy_list = []

    for xy in d_xy:
        dx_list.append(xy['player_x'])
        dy_list.append(xy['player_y'])
        
    #print(dx_list)

    ox_list = []
    oy_list = []

    for xy in o_xy:
        ox_list.append(xy['player_x'])
        oy_list.append(xy['player_y'])
        
    data = []
    data.append(dx_list)
    data.append(dy_list)
    data.append(ox_list)
    data.append(oy_list)
    data.append(football_x)
    data.append(football_y)
    
    return data 

def generate_anim(data):
    fig, ax = plt.subplots()
    ax.set_facecolor('greenyellow')
    defenders = [ax.scatter(data[0][i][1], data[1][i][1], color='b', marker='o', label="Defense") for i in range(len(data[0]))]
    offenders = [ax.scatter(data[2][i][1], data[3][i][1], color='r', marker='^', label="Offense") for i in range(len(data[2]))]
    football = ax.scatter(data[4].iloc[1], data[5].iloc[1], color='k', marker="D", label="Football")
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='b', markersize=10, label='Defense'),  # Blue circle
        Line2D([0], [0], marker='^', color='w', markerfacecolor='r', markersize=10, label='Offense'),   # Red triangle
        Line2D([0], [0], marker='D', color='w', markerfacecolor='k', markersize=10, label='Football')   # Black diamond
    ]
    ax.axis([0, 120, 0, 54])
    ax.set_xlabel("Yards")
    
    ax.axvspan(0,10, color='burlywood')
    ax.axvspan(110,120, color='burlywood')
        
    ax.set_xticks(range(10, 111, 10))
    ax.grid(axis='x', linestyle='--', color='gray')  # Dashed gray gridlines
    
    x_labels = [str(0), str(10), str(20), str(30), str(40), str(50), str(40), str(30), str(20), str(10), str(0)]
    ax.set_xticklabels(x_labels)
    
    ax.legend(handles=legend_elements)

    def update(frame):
        for i in range(len(data[0])):
            defenders[i].set_offsets([data[0][i][frame+1], data[1][i][frame+1]])
        for i in range(len(data[2])):
            offenders[i].set_offsets([data[2][i][frame+1], data[3][i][frame+1]]) 
        football.set_offsets([data[4].iloc[frame+1], data[5].iloc[frame+1]])
        return defenders + offenders + [football]

    file_path = 'static/animation.gif'
    a = FuncAnimation(fig, update, frames=len(data[0][0])-1, blit=True, interval=100)
    a.save(file_path, writer='ffmpeg', fps=10)
    
    return file_path

@app.route('/generate', methods=['POST'])
def generate():
    week = int(request.form['weeknum'])
    game = int(request.form['gameid'])
    play = int(request.form['playid'])
    
    data = clean_data(week, game, play)
    
    gif = generate_anim(data)
    
    return render_template_string('''
            <h1>Generated Animation</h1>
            <img src="{{ url_for('static', filename='animation.gif') }}" alt="Generated Animation">
            <br>
            <a href="/">Go Back</a>
        ''')

if __name__ == '__main__':
    # Ensure the file is removed after serving
    @app.after_request
    def remove_file(response):
        try:
            os.remove('animation.gif')
        except Exception as error:
            app.logger.error("Error removing file", error)
        return response

    app.run(debug=True)