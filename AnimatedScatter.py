import pandas as pd 
import numpy as np 

import matplotlib.pyplot as plt 
import matplotlib.animation as anim 

import itertools 

import math 

import extract 

week_1 = pd.read_csv('data/tracking_week_1.csv')
players = pd.read_csv('data/players.csv')

class AnimatedScatter(object):
    def __init__(self, gameID, playID):
        extractlist = extract.extract(gameID, playID)
        defense = extract.separate(extractlist)[0]
        offense = extract.separate(extractlist)[2]
        
        self.numpoints = 22
        self.stream = self.data_stream()
        
        self.fig, self.ax = plt.subplots()
        
        self.ani = anim.FuncAnimation(self.fig, self.update, interval=5, init_func=self.setup_plot, blit=True)
        
    def setup_plot(self):
        x, y, s, c = next(self.stream).T 
        self.scat = self.ax.scatter(x, y, c=c, )
        self.ax.axis([0, 120, 0, 54])
        
        return self.scat,
    
    def data_stream(self):
        xy 
        

def main():
    
    
if __name__ == "__main__":
    main()