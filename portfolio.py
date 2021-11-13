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
    
    def plot(self):
        xAxis = [key for key, value in self.data.items()]
        yAxis = [value for key, value in self.data.items()]
        plt.grid(False)
        
        plt.plot(xAxis,yAxis, color='maroon')
        plt.xlabel('Time')
        plt.ylabel('USD $')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig('static/portfolio.jpg')