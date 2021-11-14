# portfolio.py
# Daniel Kogan
# Nov 13 2021

#matplotlib
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import time

class Portfolio:
    def __init__(self, portfoliofb):
        self.data = portfoliofb.get()
    
    def plotpf(self):
        self.plot(self.data,"Time","USD $", 'static/portfolio.jpg')
        
    def plot(self, data, xlabel, ylabel, figname):
        xAxis = [key for key, value in data.items()]
        yAxis = [value for key, value in data.items()]
        plt.grid(False)
        plt.plot(xAxis,yAxis, color='maroon')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=90)
        ax = plt.gca()
        ax.axes.xaxis.set_ticks([])
        plt.tight_layout()
        plt.savefig(figname)
