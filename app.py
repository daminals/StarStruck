# app.py
# Daniel Kogan
# Nov 14 2021

# Flask Imports
from flask import Flask, escape, request, render_template, session, redirect, send_file, url_for
from flask import Flask
# os
import os
# wallet import
from wallet import *

app = Flask(__name__)
app.secret_key = SERVERKEY
all_coin_wallets = cb.all_coin_wallets()

@app.route('/', methods=["GET", "POST"])
def main():
    if request.method == "POST":
        print(cb.balance()) # UPDATES FIREBASE DATA
        os.remove("static/graph/Portfolio.png") # refresh graph
        pf.plotpf() # update graph
        for coin in all_coin_wallets:
            cb.current_price(coin)
            pf.plotpfCoin(coin)
            pf.plotCoin(coin)
    bal = str.splitlines(cb.balance())
    return render_template('main.html', bal=bal, imgsrc="static/graph/Portfolio.png")

# crypto pages
@app.route('/<coin>')
def coin_render(coin):
    coin = coin.upper()
    print(coin)
    if coin not in all_coin_wallets:
        return redirect("/404")
    else:
        bal = str.splitlines(cb.balance())        
        return render_template('main.html', bal=bal, imgsrc=f"static/graph/{coin}.png")

@app.route('/<coin>/chart', methods=['GET'])
def birthchart(coin):        
    coin = coin.upper()
    if coin not in all_coin_wallets:
        return redirect("/404")
    else:   
        return f"<title> {coin} Chart </title><img style='height: 100%' src={url_for('static', filename=f'birthcharts/{coin}NatalChart.svg')}/>"

@app.route('/coinPostRqs', methods=["GET", "POST"])
def receive():
    if request.method == "POST":
        coin = request.form['data']
        print(cb.balance())
        os.remove(f"static/graph/{coin}.png")
        pf.plotpf() # update graph
        for coinz in all_coin_wallets:
            cb.current_price(coinz)
            pf.plotpfCoin(coinz)
            pf.plotCoin(coinz)
    return "reading get request⏳"

@app.route('/cash') # not tracking USD to USD bc $1 will always = $1
def redirect_cash():
    return redirect("/")

@app.route('/404')
def page_not_found():
    return f"<link rel='stylesheet' href=\"{ url_for('static', filename='css/style.css') }\"> error 404 page not found lol"

if __name__ == '__main__':
    app.run(use_reloader=True,host='0.0.0.0')
