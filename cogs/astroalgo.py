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
    
    def coin_init(self, coin):
        try:
            if self.coin_data.get()[coin]["DOB"] != None:
                print("cannot init already initiated coin")
            return
        except KeyError:
            print("non init coin")
        data_struct = {
            "year": 2020,
            "month": 3,
            "day": 16,
            "hour": 6,
            "min": 29,
            "second": 00,
            "timezone": "San Diego",
            "country": "US"
        }
        self.coin_data.child(coin).update({"DOB": data_struct})
        
            
    def create_coin_instance(self, coin):
        coinDOB = self.readCoin(coin)
        # name year month day hour minute city(EDT)
        coin = KrInstance(coin, coinDOB['year'], coinDOB['month'], coinDOB['day'], coinDOB['hour'], coinDOB['min'], coinDOB['timezone'], coinDOB['country'])
        return coin

    def readCoin(self, coin):
        try:
            coin_DOB = self.coin_data.get()[coin]["DOB"]
            return coin_DOB
        except KeyError:
            self.coin_init(coin)
            raise KeyError
         
    
    def writeCoin(self,coin):
        return self.coin_data.child(coin).child("DOB")
    
    def create_chart(self, coin):
        coin = self.create_coin_instance(coin)
        coin.get_all()
        coinSVG = MakeSvgInstance(coin, new_output_directory=f'static/birthcharts')
        coinSVG.makeSVG()
    
    def starData(self, coin):
        coinInstance = self.create_coin_instance(coin)
        coinInstance.get_all()
        coinDOB = self.writeCoin(coin)
        coinInstance.json_dump(new_output_directory='static/json_data')
        #print(coin, coinInstance.sun)
        
    def prediction(self, coin):
        pass