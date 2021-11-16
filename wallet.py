# wallet.py
# Daniel Kogan
# Nov 11 2021

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
#classes
from cogs.portfolio import Portfolio
from cogs.coinbaseacc import CoinbaseAccount
from cogs.astroalgo import AstrologyAlgorithm

cred = credentials.Certificate("ssfbkey.json") #firebase key

load_dotenv()
# crypto
CB_APIKey = os.environ.get('CB_APIKey', 3)
CB_APISecret = os.environ.get('CB_APISecret', 3)
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

cb_acc = CoinbaseAccount(cb, ref)
pf = Portfolio(ref)

def main():
    #print(cb_acc.balance())
    #pf.plotpf()
    #cb_acc.current_price("BTC")
    #pf.plotCoin("BTC")
    #cb_acc.sell("BTC",1) # fee was 99 cents bruh
    pass



if __name__ == '__main__':
    main()