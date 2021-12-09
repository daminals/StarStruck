# cronjob.py
# Daniel Kogan
# December 9 2021

# os
import os
# wallet import
from wallet import *

all_coin_wallets = cb.all_coin_wallets()
def cronj():
    pf.plotpf() # update graph
    print("portfolio")
    for coin in all_coin_wallets:
        print(coin)
        pf.plotpfCoin(coin)
        pf.plotCoin(coin)

def log():
    with open("cronlog.txt", "a") as log_file:
        log_file.write(f"Successfully updated database at {cb.graph_now()}")

if __name__ == '__main__':
    cronj()
    log()