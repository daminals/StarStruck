# app.py
# Daniel Kogan
# Nov 14 2021

# Flask Imports
from flask import Flask, escape, request, render_template
from flask import Flask
# Coinbase import
from wallet import *

app = Flask(__name__)
@app.route('/')
def main():
    bal = str.splitlines(cb_acc.balance())        
    ltc,eth,doge,btc,total = bal
    return render_template('main.html', btc=btc,doge=doge,eth=eth,ltc=ltc,total=total)
