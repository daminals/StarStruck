# app.py
# Daniel Kogan
# Nov 14 2021

# Flask Imports
from flask import Flask, escape, request, render_template, session
from flask import Flask
# os
import os
# wallet import
from wallet import *

app = Flask(__name__)
app.secret_key = SERVERKEY


@app.route('/cash') # not tracking USD to USD bc $1 will always = $1
@app.route('/', methods=["GET", "POST"])
def main():
    if request.method == "POST":
        print(cb_acc.balance()) # update balance
        os.remove("static/graph/Portfolio.png")
        pf.plotpf() # update graph
    bal = str.splitlines(cb_acc.balance())
    return render_template('main.html', bal=bal, imgsrc="static/graph/Portfolio.png")

# crypto pages
@app.route('/btc', methods=["GET", "POST"])
def btc():
    coin = "BTC"
    if request.method == "POST":
        print(cb_acc.balance())
        cb_acc.current_price(coin)
        os.remove(f"static/graph/{coin}.png")
        pf.plotCoin(coin)
    bal = str.splitlines(cb_acc.balance())        
    return render_template('main.html', bal=bal, imgsrc=f"static/graph/{coin}.png")

@app.route('/ltc', methods=["GET", "POST"])
def ltc():
    coin = "LTC"
    if request.method == "POST":
        print(cb_acc.balance())
        cb_acc.current_price(coin)
        pf.plotCoin(coin)
    bal = str.splitlines(cb_acc.balance())
    print(bal)   
    return render_template('main.html', bal=bal, imgsrc=f"static/graph/{coin}.png")

@app.route('/doge', methods=["GET", "POST"])
def doge():
    coin = "DOGE"
    if request.method == "POST":
        print(cb_acc.balance())
        cb_acc.current_price(coin)
        pf.plotCoin(coin)
    bal = str.splitlines(cb_acc.balance())        
    return render_template('main.html', bal=bal, imgsrc=f"static/graph/{coin}.png")

@app.route('/eth', methods=["GET", "POST"])
def eth():
    coin = "ETH"
    if request.method == "POST":
        print(cb_acc.balance())
        cb_acc.current_price(coin)
        pf.plotCoin(coin)
    bal = str.splitlines(cb_acc.balance())        
    return render_template('main.html', bal=bal, imgsrc=f"static/graph/{coin}.png")



if __name__ == '__main__':
    app.run(use_reloader=True,host='0.0.0.0')
