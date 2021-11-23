# asotralgo.py
# Daniel Kogan
# Nov 13 2021
from kerykeion import KrInstance
from kerykeion.utilities.charts import MakeSvgInstance
import requests
class AstrologyAlgorithm:
    def __init__(self, database):
        self.coin_data = database.child("crypto")
        
    def __total_reset__(self): # reset every birth chart
        for coin in self.coin_data.get():
            self.create_chart(coin)
    
    def readCoin(self, coin):
        coin_DOB = self.coin_data.get()[coin]["DOB"]
        print(coin_DOB)
        return coin_DOB
    
    def create_chart(self, coin):
        coinDOB = self.readCoin(coin)
        # name year month day hour minute city(EDT)
        coin = KrInstance(coin, coinDOB['year'], coinDOB['month'], coinDOB['day'], coinDOB['hour'], coinDOB['min'], coinDOB['timezone'], "US")
        coin.get_all()
        coinSVG = MakeSvgInstance(coin, Cdir='static/birthcharts')
        coinSVG.makeSVG()
    
    def prediction(self, coin):
        pass