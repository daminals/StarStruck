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
import json, os, time, hmac, hashlib
from urllib.error import HTTPError
class CoinbaseAccount:
    def __init__(self, CB_APIKey, CB_APISecret, database):
        self.cb = Client(CB_APIKey, CB_APISecret)
        self.portfoliofb = database.child('portfolio')
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
        for wallet in self.accounts.data:
            value = str(wallet['native_balance']).replace('USD','')
            if float(value) != float(0):
                message.append(str(wallet['name']) + ': ' +   str(wallet['native_balance']).replace('USD ','$') ) # add wallet worth more than $0 to message list
                total += float(value) # add wallets value to total
        total = round(total, 2) # round total to two decimal places
        message.append( 'Total Balance: ' + '$' + str(total) ) # add total to message list
        now = self.graph_now()
        print(now) # write timestamp
        self.portfoliofb.update({now: total})
        return('\n'.join( message ))
    
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

    def get_coin_account(self, coin): # coinbase API does not read the currency field for buy accounts
        accounts = self.accounts.data 
        for wallet in accounts:
            if coin == wallet['balance']['currency']:
                return wallet
        raise noAccountException
class CoinbasePriceAPI: # custom Wrapper since coinbase-py is outdated and poorly documented
    def __init__(self, apikey, apisecret, base_api_uri=None, api_version=None):
        self.api_key = apikey
        self.secret_key = apisecret
        self.authWrapper = cbWalletAuth(self.api_key,self.secret_key)

    def transfer(self, sellCoinID, buyCoinID, amnt, coin):
        try:
            tx = {"amount": str(amnt), "currency": str(coin)}
            r = requests.post(f"https://api.coinbase.com/v2/accounts/:{sellCoinID}/transactions", json=tx, auth=self.authWrapper)
            if r.status_code == 200:
                print(f'We have bought {coin}')
        except:
            print("oops")
    
    def get_price(self,coin, real="USD"):
        url = f'https://api.coinbase.com/v2/prices/{coin}-{real}/spot'
        priceR = requests.get(url)
        price = priceR.json()
        return price['data']['amount']
    
class cbWalletAuth(AuthBase):
    def __init__(self, apikey, apisecret, api_version=None):
        self.api_key = apikey
        self.secret_key = apisecret
        self.API_VERSION = '2021-01-05'
    
    def __call__(self, request):
        timestamp = str(int(time.time()))
        message = (timestamp + request.method + request.path_url).encode("utf-8")
        if request.body:
            message=b''.join([message, request.body])
        signature = hmac.new(bytes(self.secret_key , 'latin-1'), message, hashlib.sha256).hexdigest()

        request.headers.update({
            'CB-ACCESS-SIGN': signature,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-VERSION' : '2020-06-16'
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
