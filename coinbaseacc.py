# coinbaseacc.py
# Daniel Kogan
# Nov 13 2021

# coinbase
from coinbase.wallet.client import Client
from coinbase.wallet.error import AuthenticationError
# datetime
import datetime as dt

class CoinbaseAccount:
    def __init__(self, client, portfoliofb):
        self.cb = client
        self.portfoliofb = portfoliofb
        self.user = self.cb.get_current_user()
        self.accounts = self.cb.get_accounts()
    
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
        self.portfoliofb.update({now: total})
        return('\n'.join( message ))
    
    def current_price(self, coin):
        pass
    
    def buy(self, coin):
        pass
    
    def sell(self, coin):
        pass