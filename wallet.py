from constants import *
import os
import subprocess
import json
from web3 import Web3
from dotenv import load_dotenv
from web3.middleware import geth_poa_middleware
from eth_account import Account

from pathlib import Path
from getpass import getpass

from bit import wif_to_key
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI

load_dotenv()


# enter your personal mnemonic here

mnemonic = os.getenv('MNEMONIC', 'work want afford grace rubber build chair sudden valley certain capital club')


# Function to provide your wallet address

def wallet_address(coins,depth):
    
    command = f"../derive -g --mnemonic='{mnemonic}' --cols=path,address,privkey,pubkey --coin={coins} --numderive={depth} --format=json"
    
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    keys = json.loads(output)
    
    return keys


#ETH wallets
wallet_address("ETH",3)

#BTC Test Wallets
wallet_address("btc-test",3)

#BTC wallets
wallet_address("btc",3)



def priv_key_to_account(coin,priv_key):
    if coin == "ETH":
        w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        #account_one = Account.from_key(os.getenv("PRIVATE_KEY"))
        #account_one = Account.from_key(PRIVATE_KEY)
        account_one = Account.privateKeyToAccount(priv_key)
        print(account_one)
        return account_one
    
    elif coin == "btc-test":
        btc_account= PrivateKeyTestnet(priv_key)
        
        return btc_account
    
    
    
def create_tx(coin, account, recipient, amount):
    if coin == "ETH":
        gasEstimate = w3.eth.estimateGas(
            {"from": account.address, "to": recipient, "value": amount}
        )
        return {
            "from": account.address,
            "to": recipient,
            "value": amount,
            "gasPrice": round(w3.eth.gasPrice),
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address),
        }

    elif coin == "btc-test":
        btc_tx = PrivateKeyTestnet.prepare_transaction(account.address, [(recipient, amount, BTC)])
        
        return btc_tx 

    

def send_tx(coin, account, recipient, amount):
    if coin == "ETH":
        tx = create_tx(coin,account, recipient, amount)
        signed_tx = account.sign_transaction(tx)
        result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(result.hex())
        return result.hex()
    
    elif coin == "btc-test":
        btc_tx = create_tx(coin,account, recipient, amount)
        tx_hex = key.sign_transaction(btc_tx)
        result = NetworkAPI.broadcast_tx_testnet(tx_hex)
        
        return tx_hex
    
    
#Sending ETH Transaction

# Enter your ETH private key with funding

eth_address1 = "0x9eDeBC9f308848F247595e663e0796CFF62A965a"
eth_priv_key1 = '0x75ade74425d7272a2a82f77efb632fe7e5b706f6fbe7da72637da3f795e0ab7e'
#priv_key2 = '0xe7a541bd8483c99a489baeaf337ac3acc7175d4aa1b444c1632a45db21b1a039'
account_one = priv_key_to_account("ETH",eth_priv_key1)
account_one


# Check the balance

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.eth.getBalance(eth_address1)

# Create unsigned transaction ticket using the function above and enter the receipient and amount
receipient_eth1 = "0x146ff600884a2c5e25216e30b52EC7D033E797d6"
create_tx("ETH",account_one,receipient_eth1,8888)


# now signed the contract and send transaction ticket
send_tx("ETH",account_one,receipient_eth1,8888)


w3.eth.getTransactionReceipt("0x92059faea613acf46f772ef649a4afe81198b35cdcefaf1469d93195a1592990")

w3.eth.getTransaction("0x92059faea613acf46f772ef649a4afe81198b35cdcefaf1469d93195a1592990")


#Sending ETH Transaction

#enter your private key and check the balance

btc_priv_key1="cRSFSFMH242PYahfUaM3HMMkRwGMc8jyALZSkVnh6QEtaQJXo8dw"

key = wif_to_key(btc_priv_key1)

key.get_balance('btc')

# get BTC account address from private key

btc_account_one = priv_key_to_account("btc-test",btc_priv_key1)
btc_account_one


# Create unsigned transaction ticket using the function above and enter the receipient and amount

receipient_btc1 = "mnHT7DTSDV5LpSkz6RNBoQV4GpP1s78Pup"
create_tx("btc-test",btc_account_one,receipient_btc1,0.003)


# now signed the contract and send transaction ticket
send_tx("btc-test",btc_account_one,receipient_btc1,0.003)





