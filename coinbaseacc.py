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
        self.priceAPI = CoinbasePriceAPI(self.cb)
        
    def graph_now(self):
        now = dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        return now
    
    def balance(self):
        total = 0
        message = []
        for wallet in self.accounts.data:
            value = str(wallet['native_balance']).replace('USD','')
            if float(value) != float(0):
                message.append(str(wallet['name']) + ': ' +   str(wallet['native_balance']).replace('USD ','$') )
            total += float(value)
        message.append( 'Total Balance: ' + '$' + str(total) )
        now = self.graph_now()
        print(now)
        self.portfoliofb.update({now: total})
        return('\n'.join( message ))
    
    def listize(bal):
        pass
    
    def current_price(self, coin):
        currency_code = "USD"
        price = self.priceAPI.get_price(coin,currency_code)
        coin_fb = self.p_crypto.child(f'{coin}/POT')
        now = self.graph_now()
        coin_fb.update({now: price})
        return price
    
    def buy(self, coin=None):
        payment_methods = self.cb.get_payment_methods()[0]
        account = self.cb.get_primary_account()
        #print(payment_methods)
    
    def sell(self, coin, amnt):
        price = float(self.current_price(coin))
        print(price)
        amnt = float(amnt)
        print(amnt)
        conversion_rate = amnt/price
        coin_amnt = 1 * conversion_rate
        print(coin_amnt)
        payment_method = self.cb.get_payment_methods()[0]
        account = self.cb.get_primary_account()
        account.sell(amount=coin_amnt, currency="btc", payment_method=payment_method.id)

    


class CoinbasePriceAPI:
    def __init__(self, client):
        self.cb = client
        
    def get_price(self,coin, real="USD"):
        url = f'https://api.coinbase.com/v2/prices/{coin}-{real}/spot'
        priceR = requests.get(url)
        price = priceR.json()
        return price['data']['amount']

    