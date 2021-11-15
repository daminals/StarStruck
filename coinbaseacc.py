# coinbaseacc.py
# Daniel Kogan
# Nov 13 2021

# coinbase
from coinbase.wallet.client import Client
from coinbase.wallet.error import AuthenticationError
# datetime
import datetime as dt
# requests
import requests
import urllib.request
import json


class CoinbaseAccount:
    def __init__(self, client, database):
        self.cb = client
        self.portfoliofb = database.child('portfolio')
        self.p_crypto = database.child('crypto')
        self.user = self.cb.get_current_user()
        self.accounts = self.cb.get_accounts()
        self.priceAPI = CoinbasePriceAPI(self.cb) # use custom API
        
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
    
    def listize(bal):
        pass
    
    def current_price(self, coin):
        currency_code = "USD"
        price = self.priceAPI.get_price(coin,currency_code)
        coin_fb = self.p_crypto.child(f'{coin}/POT')
        now = self.graph_now() # write timestamp to update graph
        coin_fb.update({now: price}) # update firebase with new data
        return price
    
    def buy(self, coin=None):
        payment_methods = self.cb.get_payment_methods()[0]
        account = self.cb.get_primary_account()
        #print(payment_methods)
    
    def sell(self, coin, amnt: float): # NEVER USE THIS!!!!! FEES TOO HIGH
        price = float(self.current_price(coin)) # read coin price
        conversion_rate = amnt/price # calculate conversion rate
        coin_amnt = conversion_rate # since we are converting dollars to coins we are taking the conversion rate of $x to 1 coin and the conversion rate is the percentage
        print(coin_amnt)
        payment_method = self.cb.get_payment_methods()[0] # use first payment method
        account = self.cb.get_primary_account() # get account
        raise sellException
        #account.sell(amount=coin_amnt, currency="btc", payment_method=payment_method.id)

class CoinbasePriceAPI: # custom Wrapper since coinbase-py is outdated and poorly documented
    def __init__(self, client):
        self.cb = client
        
    def get_price(self,coin, real="USD"):
        url = f'https://api.coinbase.com/v2/prices/{coin}-{real}/spot'
        priceR = requests.get(url)
        price = priceR.json()
        return price['data']['amount']
    
class Error(Exception):
    """Base class for other exceptions"""
    pass
class sellException(Exception): # custom exception so i don't lose my money to transaction fees lol
    def __init__(self, message="Transaction fees too high"):
        self.message = message
        super().__init__(self.message)
