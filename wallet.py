# wallet.py
from bitcoinlib.wallets import Wallet, wallet_delete
from bitcoinlib.mnemonic import Mnemonic
from dotenv import load_dotenv
import os

load_dotenv()
key = os.environ.get('key', 3)

passphrase = Mnemonic().generate()
print(passphrase)

wallet = Wallet.create('dwallet', keys=passphrase)
key1 = wallet.new_key()
print(key1.address)
wallet.scan()
wallet.info()