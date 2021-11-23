# asotralgo.py
# Daniel Kogan
# Nov 13 2021
from kerykeion import KrInstance, output
from kerykeion.utilities.charts import MakeSvgInstance
import requests
class AstrologyAlgorithm:
    def __init__(self, database):
        self.coin_data = database.child("crypto")
        
    def __total_reset__(self): # reset every birth chart
        for coin in self.coin_data.get():
            self.create_chart(coin)
            
    def create_coin_instance(self, coin):
        coinDOB = self.readCoin(coin)
        # name year month day hour minute city(EDT)
        coin = KrInstance(coin, coinDOB['year'], coinDOB['month'], coinDOB['day'], coinDOB['hour'], coinDOB['min'], coinDOB['timezone'], "US")
        return coin

    def readCoin(self, coin):
        coin_DOB = self.coin_data.get()[coin]["DOB"]
        return coin_DOB 
    
    def writeCoin(self,coin):
        return self.coin_data.child(coin).child("DOB")
    
    def create_chart(self, coin):
        coin = self.create_coin_instance(coin)
        coin.get_all()
        coinSVG = MakeSvgInstance(coin, Cdir='static/birthcharts')
        coinSVG.makeSVG()
    
    def starData(self, coin):
        coinInstance = self.create_coin_instance(coin)
        coinInstance.get_all()
        coinDOB = self.writeCoin(coin)
        print(coin, coinInstance.sun)
        
    def prediction(self, coin):
        pass