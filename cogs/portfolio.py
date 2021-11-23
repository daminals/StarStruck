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
import time, json

class Portfolio:
    def __init__(self, data):
        portfoliofb = data.child('portfolio') # read firebase databases 
        crypto = data.child('crypto') # and be able to write to them
        self.portfoliofb = portfoliofb
        self.crypto = crypto       
    
    def plotpf(self): # plot portfolio
        portfolio_get = self.portfoliofb.child("TOTAL").get()
        self.plot(portfolio_get,"Time","USD $", 'static/graph/Portfolio.png')
        
    def plotpfCoin(self, coin): # plot value of coin wallet
        portfolioCoin_get = self.portfoliofb.child(coin).get()
        self.plot(portfolioCoin_get,"Time","USD $", f'static/graph/Portfolio/{coin}.png')
        
    def plotCoin(self, coin): # plot coin
        POT = self.crypto.child(f'{coin}/POT').get() # price over time
        self.plot(POT, "Time", f"{coin} in $", f"static/graph/{coin}.png", True)
        
    def plot(self, data, xlabel, ylabel, figname, coin_true=False):
        xAxis = [key for key, value in data.items()] # list comprehension;
        yAxis = [value for key, value in data.items()] # turn firebase into lists for matplotlib axes
        plt.grid(False) # not gridded
        plt.plot(xAxis,yAxis, color='maroon')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.xticks(rotation=90) # technically unecessary since i stopped displaying timestamps but rip lol
        ax = plt.gca()
        if coin_true:
            plt.gca().invert_yaxis()
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
                'DOB': {"year": 2009,
                        "month": 1,
                        "day": 3,
                        "hour": 13,
                        "min": 15,
                        "second": 5,
                        "timezone": "EDT"},
                'POT': {
                    'TIMESTAMP': 'PRICE'
                }
            },
            'DOGE': {
                'DOB': {"year": 2013,
                        "month": 12,
                        "day": 6,
                        "hour": 12,
                        "min": 0,
                        "second": 0,
                        "timezone": "EDT"},
                'POT': {
                    'TIMESTAMP': 'PRICE'
                }
            },
            'ETH': {
                'DOB': {"year": 2015,
                        "month": 7,
                        "day": 30,
                        "hour": 22,
                        "min": 26,
                        "second": 13,
                        "timezone": "EDT"},
                'POT': {
                    'TIMESTAMP': 'PRICE'
                }
            },
            'LTC': {
                'DOB': {"year": 2011,
                        "month": 10,
                        "day": 13,
                        "hour": 10,
                        "min": 31,
                        "second": 0,
                        "timezone": "EDT"},
                'POT': {
                    'TIMESTAMP': 'PRICE'
                }
            }
        })