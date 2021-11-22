# asotralgo.py
# Daniel Kogan
# Nov 13 2021
from kerykeion import KrInstance
from kerykeion.utilities.charts import MakeSvgInstance

class AstrologyAlgorithm:
    def __init__(self, database):
        self.coin_data = database.child("crypto")
    
    def readCoin(self, coin):
        coin_DOB = self.coin_data.get()[coin]["DOB"]
        return coin_DOB
    
    def create_chart(self, coin):
        coinDOB = self.readCoin(coin)
        # name year month day hour minute city(EDT)
        coin = KrInstance(coin, coinDOB['year'], coinDOB['month'], coinDOB['day'], coinDOB['hour'], coinDOB['min'], coinDOB['timezone'])
        coin.get_all()
        coinSVG = MakeSvgInstance(coin, Cdir='static/birthcharts')
        coinSVG.makeSVG()
    