# coinbaseacc.py
# Daniel Kogan
# Nov 13 2021

# coinbase
from coinbase.wallet.client import Client
from coinbase.wallet.error import AuthenticationError
from coinbase.wallet.auth import HMACAuth
from requests.auth import AuthBase
from coinbase.wallet.util import check_uri_security
# datetime
import datetime as dt
# requests
import requests
import urllib.request
from requests.utils import to_native_string
import json, os, time, hmac, hashlib, base64
from urllib.error import HTTPError
class CoinbaseAccount:
    def __init__(self, CB_APIKey, CB_APISecret, database):
        self.cb = Client(CB_APIKey, CB_APISecret)
        self.portfoliofb = database.child('portfolio')
        self.portfolioTOTAL = self.portfoliofb.child("TOTAL")
        self.p_crypto = database.child('crypto')
        self.user = self.cb.get_current_user()
        self.accounts = self.cb.get_accounts()
        self.priceAPI = CoinbasePriceAPI(CB_APIKey, CB_APISecret) # use custom API
    
    def graph_now(self):
        now = dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        return now
    
    def balance(self): # add up entire wallet
        total = 0
        message = []
        now = self.graph_now()
        for wallet in self.accounts.data:
            value = str(wallet['native_balance']).replace('USD','')
            if float(value) != float(0): # if the value is not 0
                message.append(str(wallet['name']) + ': ' +   str(wallet['native_balance']).replace('USD ','$') ) # add wallet worth more than $0 to message list
                coin = str(wallet["name"])[:-7] # "COIN wallet" except no "wallet"
                if wallet['name'] != "Cash (USD)": # don't graph value of cash
                    self.portfoliofb.child(coin).update({now: value})
                total += float(value) # add wallets value to total
        total = round(total, 2) # round total to two decimal places
        message.append( 'Total Balance: ' + '$' + str(total) ) # add total to message list
        self.portfolioTOTAL.update({now: total})
        return('\n'.join(message))
    
    def all_coin_wallets(self):
        all_wallets = []
        for wallet in self.accounts.data:
            value = str(wallet['native_balance']).replace('USD','')
            if float(value) != float(0):
                if wallet['name'] != "Cash (USD)":
                    all_wallets.append(str(wallet['name'])[:-7])
        return all_wallets
    
    def current_price(self, coin):
        currency_code = "USD"
        price = self.priceAPI.get_price(coin,currency_code)
        coin_fb = self.p_crypto.child(f'{coin}/POT')
        now = self.graph_now() # write timestamp to update graph
        coin_fb.update({now: price}) # update firebase with new data
        return float(price)
    
    def priceToCoin(self, coin, amnt: float):
        price = self.current_price(coin) # read coin price
        conversion_rate = amnt/price # calculate conversion rate
        coin_amnt = conversion_rate # since we are converting dollars to coins we are taking the conversion rate of $x to 1 coin and the conversion rate is the percentage
        return float(coin_amnt)
    
    def buy(self, coin, amnt: float):
        coin_amnt = self.priceToCoin(coin, amnt)
        payment_method = self.cb.get_payment_methods()[0]
        account = self.get_coin_account(coin)
        account.buy(amount=coin_amnt,
                    currency=coin,
                    payment_method=payment_method.id)
        return True
    
    def sell(self, coin, amnt: float): # NEVER USE THIS!!!!! FEES TOO HIGH
        coin_amnt = self.priceToCoin(coin, amnt) # since we are converting dollars to coins we are taking the conversion rate of $x to 1 coin and the conversion rate is the percentage
        payment_method = self.cb.get_payment_methods()[0] # use first payment method
        account = self.cb.get_primary_account() # get account
        raise sellException
        #account.sell(amount=coin_amnt, currency=coin, payment_method=payment_method.id)
        return True
    
    def coinToCoin(self,sellCoin,buyCoin, amnt):
        sellCoinAcc = self.get_coin_account(sellCoin)
        buyCoinAcc = self.get_coin_account(buyCoin)
        self.priceAPI.transfer(sellCoinAcc.id, buyCoinAcc.id, amnt, sellCoin)
    
    def getUser(self, sellCoin):
        sellCoinAcc = self.get_coin_account(sellCoin)
        self.priceAPI.getUser(sellCoinAcc.id)

    def test_buy(self):
        acc = self.cb.get_primary_account() # get account
        payment_method = self.cb.get_payment_methods()[0] # use first payment method
        self.priceAPI.buyCoin(acc.id, payment_method)

    def get_coin_account(self, coin): # coinbase API does not read the currency field for buy accounts
        accounts = self.accounts.data 
        for wallet in accounts:
            if coin == wallet['balance']['currency']:
                return wallet
        raise noAccountException
class CoinbasePriceAPI: # custom Wrapper since coinbase-py is outdated and poorly documented
    def __init__(self, apikey, apisecret, base_api_uri=None, api_version='2021-01-05'):
        self.api_key = apikey
        self.secret_key = apisecret
        self.authWrapper = cbWalletAuth(self.api_key,self.secret_key)
        
    def writeJSON(self, r, filename):
        bytejson = json.loads(r.content.decode("utf8").replace("'",'"'))
        with open(filename, 'w') as outfile:
            json.dump(bytejson, outfile, indent=4,sort_keys=True)
        return True

    def transfer(self, sellCoinID, buyCoinID, amnt, coin): # TODO: amount should be converted from $ to coin amnt
        tx = {'type': 'transfer',
              'to': buyCoinID, 
              'amount': str(amnt), 
              'currency': str(coin)}
        r = requests.post(f"https://api.coinbase.com/v2/accounts/{sellCoinID}/transactions", data=tx, auth=self.authWrapper)
        # returns entire transaction history as a get request
        # self.writeJSON(r, 'return.json')
        print(r.content, r.status_code)
        if r.status_code == 200:
            print(f'StarStruck bought {amnt} {coin}')
    
    def buyCoin(self, acc_id, payment_method):
        tx = {"amount": "1.00",
              "currency": "BTC",
              "payment_method": payment_method}
        r = requests.post(f"https://api.coinbase.com/v2/accounts/{acc_id}/buys", data=tx, auth=self.authWrapper)
        # returns no data as a get request
        # self.writeJSON(r, 'buyreturn.json')
        print(r.content, r.status_code)

    def getUser(self, acc_id=None):
        r = requests.get(f"https://api.coinbase.com/v2/accounts/{acc_id}", auth=self.authWrapper)
        print(r.content, r.status_code)
        
    def get_price(self,coin, real="USD"):
        url = f'https://api.coinbase.com/v2/prices/{coin}-{real}/spot'
        priceR = requests.get(url)
        price = priceR.json()
        return price['data']['amount']
        
class cbWalletAuth(AuthBase):
    def __init__(self, apikey, apisecret, api_version='2021-01-05'):
        self.api_key = apikey
        self.secret_key = apisecret
        self.API_VERSION = api_version
    
    def __call__(self, request):
        timestamp = str(int(time.time()))
        secret = self.secret_key
        message = timestamp + request.method + request.path_url
        if request.body:
            message = message + request.body
        if not isinstance(message, bytes):
            message = message.encode()
        if not isinstance(secret, bytes):
            secret = secret.encode()

        signature = hmac.new(secret, message, hashlib.sha256).hexdigest() 
        request.headers.update({
            to_native_string('CB-VERSION') : '2021-11-11',
            to_native_string('CB-ACCESS-SIGN'): signature,
            to_native_string('CB-ACCESS-TIMESTAMP'): timestamp,
            to_native_string('CB-ACCESS-KEY'): self.api_key,
            # application/json
            to_native_string('Accept'): 'application/json',
            to_native_string('Content-Type'): 'application/json',
            to_native_string('User-Agent'): 'coinbase/python/2.0'
        })
        return request    
class Error(Exception):
    """Base class for other exceptions"""
    pass
class sellException(Exception): # custom exception so i don't lose my money to transaction fees lol
    def __init__(self, message="Transaction fees too high"):
        self.message = message
        super().__init__(self.message)
class noAccountException(Exception):
        def __init__(self, message="Account for desired coin could not be found"):
            self.message = message
            super().__init__(self.message)
