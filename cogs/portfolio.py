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
        portfoliofb = data.child('portfolio') # read firebase databases 
        crypto = data.child('crypto') # and be able to write to them
        self.portfoliofb = portfoliofb 
        self.crypto = crypto
    
    def plotpf(self): # plot portfolio
        portfolio_get = self.portfoliofb.get()
        self.plot(portfolio_get,"Time","USD $", 'static/graph/Portfolio.png')
        
    def plotCoin(self, coin): # plot coin
        POT = self.crypto.child(f'{coin}/POT').get() # price over time
        self.plot(POT, "Time", f"{coin} in $", f"static/graph/{coin}.png")
        
        
    def plot(self, data, xlabel, ylabel, figname):
        xAxis = [key for key, value in data.items()] # list comprehension;
        yAxis = [value for key, value in data.items()] # turn firebase into lists for matplotlib axes
        plt.grid(False) # not gridded
        plt.plot(xAxis,yAxis, color='maroon')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=90) # technically unecessary since i stopped displaying timestamps but rip lol
        ax = plt.gca()
        ax.axes.xaxis.set_ticks([]) # don't display bottom timestamps
        plt.tight_layout() # show off whole graphs no cutoffs 
        plt.savefig(figname, transparent=True) #png
        plt.close()

class firebaseStruct:
    def __init__(self, portfoliofb):
        self.portfoliofb = portfoliofb
    
    def __struct__():
        users_ref = ref.child('crypto') # price over time = POT
        users_ref.set({
            'BTC': {
                'DOB': '03.01.2009 | 13:15:05 GMT', # 3 jan 2009
                'POT': {
                    'TIMESTAMP': 'PRICE'
                }
            },
            'DOGE': {
                'DOB': '06.12,2013 | 12:00:00 EDT', # 6 december 2013
                'POT': {
                    'TIMESTAMP': 'PRICE'
                }
            },
            'ETH': {
                'DOB': '06.12,2013 | ', # 30 july 2015
                'POT': {
                    'TIMESTAMP': 'PRICE'
                }
            },
            'LTC': {
                'DOB': '13.10.2011 | ', # 13 october 2011
                'POT': {
                    'TIMESTAMP': 'PRICE'
                }
            }
        })
