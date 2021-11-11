# wallet.py
from bitcoinlib.wallets import Wallet, wallet_delete, wallet_create_or_open
from bitcoinlib.mnemonic import Mnemonic
from dotenv import load_dotenv
import os, coinbase
from firebase import firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate("ssfbkey.json")

load_dotenv()
CB_APIKey = os.environ.get('CB_APIKey', 3)
CB_APISecret = os.environ.get('CB_APISecret', 3)
FIREBASE = os.environ.get('FIREBASE', 3)
FIREBASE_NAME = os.environ.get('FIREBASE_NAME', 3)

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': FIREBASE
})

# As an admin, the app has access to read and write all data, regradless of Security Rules
ref = db.reference('app/')
print(ref.get())

#passphrase = Mnemonic().generate()
#print(passphrase)

cb = coinbase.Coinbase.with_api_key(CB_APIKey, CB_APISecret)


balance = cb.get_balance()
