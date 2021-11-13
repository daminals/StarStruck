# wallet.py
from dotenv import load_dotenv
import os, coinbase, json
#matplotlib
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import time
#coinbase
from coinbase.wallet.client import Client
from coinbase.wallet.error import AuthenticationError
#firebase
from firebase import firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("ssfbkey.json") #firebase key

load_dotenv()
# crypto
CB_APIKey = os.environ.get('CB_APIKey', 3)
CB_APISecret = os.environ.get('CB_APISecret', 3)

btckey = os.environ.get('btckey', 3)
dogekey = os.environ.get('dogekey', 3)
ltckey = os.environ.get('ltckey', 3)
ethkey = os.environ.get('ethkey', 3)

# firebase
FIREBASE = os.environ.get('FIREBASE', 3)
FIREBASE_NAME = os.environ.get('FIREBASE_NAME', 3)

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': FIREBASE
})

# As an admin, the app has access to read and write all data, regradless of Security Rules
ref = db.reference('app/')
portfoliofb = ref.child('portfolio')
#print(ref.get()) #prints whole firebase database

# information
cb = Client(CB_APIKey, CB_APISecret)
class CoinbaseAccount:
    def __init__(self, client):
        self.cb = client
        self.user = cb.get_current_user()
        self.accounts = cb.get_accounts()
    
    def balance(self):
        total = 0
        message = []
        for wallet in self.accounts.data:
            value = str( wallet['native_balance']).replace('USD','')
            if float(value) != float(0):
                message.append( str(wallet['name']) + ' ' +   str(wallet['native_balance']) )
            total += float(value)
        message.append( 'Total Balance: ' + 'USD ' + str(total) )
        now = dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        print(now)
        portfoliofb.update({now: total})
        return('\n'.join( message ))

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
        plt.savefig('portfolio.jpg')
        #print(self.data)

cb_acc = CoinbaseAccount(cb)
pf = Portfolio(portfoliofb)

print(cb_acc.balance())
pf.plot()
