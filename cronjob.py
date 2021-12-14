# cronjob.py
# Daniel Kogan
# December 9 2021

# os
import os
# wallet import
from wallet import *

all_coin_wallets = cb.all_coin_wallets()
def cronj():
    print(cb.balance())
    pf.plotpf() # update graph
    for coin in all_coin_wallets:
        cb.current_price(coin)
        pf.plotpfCoin(coin)
        pf.plotCoin(coin)

def log(): #TODO: host server, point to files instead of using system so no excessive rewrites of images
    with open("cronlog.txt", "a") as log_file:
        log_file.write(f"Successfully updated database at {cb.graph_now()} \n")

if __name__ == '__main__':
    cronj()
    log()