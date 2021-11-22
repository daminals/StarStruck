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
        
    
    def create_chart(self, coin):
        # name year month day hour minute city(EDT)
        coin = KrInstance(coin, 2009, 1, 3, 13, 15, "New York")
        coin.get_all()
        coinSVG = MakeSvgInstance(coin, Cdir='static/birthcharts')
        coinSVG.makeSVG()
    