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
# flask secret key
SERVERKEY = os.environ.get('SERVERKEY', 3)

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
cb = CoinbaseAccount(CB_APIKey, CB_APISecret, ref)
pf = Portfolio(ref)
astro = AstrologyAlgorithm(ref)

def main():
    #print(cb_acc.balance())
    #pf.plotpf()
    #cb.current_price("BTC")
    #pf.plotCoin("BTC")
    #cb.sell("BTC",0.25) # fee was 99 cents bruh
    #cb.buy("DOGE", 0.25)
    #cb.getUser("BTC")
    cb.coinToCoin("DOGE","BTC",0.15)
    cb.test_buy()
    #astro.create_chart("ETH")
    #astro.starData("BTC")


if __name__ == '__main__':
    main()