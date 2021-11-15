# app.py
# Daniel Kogan
# Nov 14 2021

# Flask Imports
from flask import Flask, escape, request, render_template
from flask import Flask
# wallet import
from wallet import *

app = Flask(__name__)
@app.route('/', methods=["GET", "POST"])
def main():
    if request.method == "POST":
        print(cb_acc.balance())
        pf.plotpf()
    bal = str.splitlines(cb_acc.balance())        
    ltc,eth,doge,btc,total = bal # instead of this, will eventually turn into a split list
    return render_template('main.html', btc=btc,doge=doge,eth=eth,ltc=ltc,total=total)

@app.route('/btc')
def btc():
    bal = str.splitlines(cb_acc.balance())        
    ltc,eth,doge,btc,total = bal # instead of this, will eventually turn into a split list
    return render_template('main.html', btc=btc,doge=doge,eth=eth,ltc=ltc,total=total)

@app.route('/doge')
def doge():
    bal = str.splitlines(cb_acc.balance())        
    ltc,eth,doge,btc,total = bal # instead of this, will eventually turn into a split list
    return render_template('main.html', btc=btc,doge=doge,eth=eth,ltc=ltc,total=total)

if __name__ == '__main__':
    app.run(use_reloader=True)
