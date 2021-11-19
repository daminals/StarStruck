# app.py
# Daniel Kogan
# Nov 14 2021

# Flask Imports
from flask import Flask, escape, request, render_template, session, redirect
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
        print(cb.balance()) # update balance
        os.remove("static/graph/Portfolio.png") # refresh graph
        pf.plotpf() # update graph
        cb.coinToCoin("BTC","DOGE",0.1)
    ip_address = request.remote_addr
    print(ip_address)
    bal = str.splitlines(cb.balance())
    return render_template('main.html', bal=bal, imgsrc="static/graph/Portfolio.png")

# crypto pages
@app.route('/<coin>')
def coin_render(coin):
    coin = coin.upper()
    print(coin)
    if coin not in all_coin_wallets:
        abort(404)
    else:
        bal = str.splitlines(cb.balance())        
        return render_template('main.html', bal=bal, imgsrc=f"static/graph/{coin}.png")

@app.route('/coinPostRqs', methods=["GET", "POST"])
def receive():
    if request.method == "POST":
        coin = request.form['data']
        print(cb.balance())
        cb.current_price(coin)
        os.remove(f"static/graph/{coin}.png")
        pf.plotCoin(coin)
    return "reading get request⏳"

@app.route('/cash') # not tracking USD to USD bc $1 will always = $1
def redirect_cash():
    return redirect("/")

if __name__ == '__main__':
    app.run(use_reloader=True,host='0.0.0.0')
