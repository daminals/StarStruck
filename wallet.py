# wallet.py
from dotenv import load_dotenv
import os, coinbase, json
from coinbase.wallet.client import Client
from coinbase.wallet.error import AuthenticationError
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
#print(ref.get()) #prints whole firebase database

# information
cb = Client(CB_APIKey, CB_APISecret)
user = cb.get_current_user()
accounts = cb.get_accounts()
def balance(accounts):
    total = 0
    message = []
    for wallet in accounts.data:
        message.append( str(wallet['name']) + ' ' +   str(wallet['native_balance']) )
        value = str( wallet['native_balance']).replace('USD','')
        total += float(value)
    message.append( 'Total Balance: ' + 'USD ' + str(total) )
    return('\n'.join( message ))



print(balance(accounts))
#cb.get_buy_price(currency_pair = 'BTC-USD')
