# portfolio.py
# Daniel Kogan
# Nov 13 2021

#matplotlib
import datetime as dt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import time

class Portfolio:
    def __init__(self, data):
        portfoliofb = data.child('portfolio')
        crypto = data.child('crypto')
        self.portfoliofb = portfoliofb
        self.crypto = crypto
    
    def plotpf(self):
        portfolio_get = self.portfoliofb.get()
        self.plot(portfolio_get,"Time","USD $", 'static/graph/Portfolio.png')
        
    def plotCoin(self, coin):
        POT = self.crypto.child(f'{coin}/POT').get() # price over time
        self.plot(POT, "Time", f"{coin} in $", f"static/graph/{coin}.png")
        
        
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
        plt.savefig(figname, transparent=True)
        plt.close()
