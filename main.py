import asyncio
import json
import time
from web3 import Web3
import requests
from config import *

trx_list = []

bsc = 'https://bsc-dataseed.binance.org/'
# bsc = "https://rpc.ankr.com/bsc_testnet_chapel"
web3 = Web3(Web3.HTTPProvider(bsc))
if web3.isConnected(): print("Connected to BSC")

# converting addresses to suitable format for web3

pancakeswap_address = web3.toChecksumAddress(pancakeswap_address)
sender_address = web3.toChecksumAddress(my_address)
for token in token_addresses:
    token_addresses[token] = web3.toChecksumAddress(token_addresses[token])

# Setup the PancakeSwap contract
contract = web3.eth.contract(address=pancakeswap_address, abi=panabi)


# def save_abi_keys():
#     for name in token_addresses:
#         token_abi_list[name] = get_abi(token_addresses[name])


# def calcSell(tokenAddress):
#     oneToken = web3.toWei(1, 'Ether')
#     price = contract.functions.getAmountsOut(oneToken, [tokenAddress, token_addresses['WBNB']]).call()
#     normalizedPrice = web3.fromWei(price[1], 'Ether')
#     return normalizedPrice


# print(calcSell(token_addresses['BUSD']))


def get_abi(address):
    url = f"https://api.bscscan.com/api?module=contract&action=getabi&address={address}&apikey={bscan_api_key}"
    res = requests.get(url).json()
    # print(res)
    print(res)

    if str(res['status']) == '0':
        print("ABI not found")
        return
    return res['result']


# save_abi_keys()
# print(token_abi_list)


def get_trx_receipt(trx):
    url = f"https://api.bscscan.com/api?module=proxy&action=eth_getTransactionByHash&txhash={trx}&apikey={bscan_api_key}"
    res = requests.get(url).json()
    print(res)
    data = contract.decode_function_input(res['result']['input'])
    print("swap" in str(data[0]))
    print(type(data[0]), data[1])

    return data[1], res['result'], data[0]


def swap_token(hash):
    data, trx, swap_function = get_trx_receipt(hash)
    if "swap" in str(swap_function):

        balance = web3.eth.get_balance(sender_address)
        print(balance)
        print(int(trx['value'], 0), int(int(trx['gas'], 0) * (1 + gas_percent / 100)),
              int(int(trx['gasPrice'], 0) * (1 + gas_percent / 100)))
        print(web3.toWei(int(trx['value'], 0) / 10 ** 18, 'ether'))
        print(web3.toWei(int(trx['gas'], 0) * int(trx['gasPrice'], 0) / 10 ** 18, 'ether'))

        if 'amountIn' not in data:
            max_bnb = max_limit['BNB'] * (10 ** 18)
            data['amountIn'] = int(trx['value'], 0) if int(trx['value'], 0) <= max_bnb else max_bnb
        elif data['path'][0] == token_addresses['BUSD'] or data['path'][0] == token_addresses['USDT']:
            max_usdt = max_limit['BUSD'] * (10 ** 18)
            data['amountIn'] = data['amountIn'] if int(data['amountIn']) <= max_usdt else max_usdt

        if "swapExactETHForTokens" in str(swap_function) or "swapETHForExactTokens" in str(swap_function):
            pancakeswap2_txn = swap_function(
                data['amountOutMin'],
                data['path'],
                sender_address,
                (int(time.time()) + 100)
            ).buildTransaction({
                'from': sender_address,
                'value': data['amountIn'],
                'gas': int(int(trx['gas'], 0) * (1 + gas_percent / 100)),
                'gasPrice': int(int(trx['gasPrice'], 0) * (1 + gas_percent / 100)),
                'nonce': web3.eth.get_transaction_count(sender_address),
            })

            signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=private_key)
            tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            print(web3.toHex(tx_token))

        else:

            sellTokenContract = web3.eth.contract(data['path'][0], abi=short_abi)
            x = sellTokenContract.functions.allowance(sender_address, pancakeswap_address).call()

            print("Allowance: ", x)
            if int(x) == 0:
                balance = sellTokenContract.functions.balanceOf(sender_address).call()

                approve = sellTokenContract.functions.approve(web3.toChecksumAddress(pancakeswap_address),
                                                              balance).buildTransaction({
                    'from': sender_address,
                    'gasPrice': int(int(trx['gasPrice'], 0) * (1 + gas_percent / 100)),
                    'nonce': web3.eth.get_transaction_count(sender_address),
                })
                signed_txn = web3.eth.account.sign_transaction(approve, private_key=private_key)
                tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
                print("Approved: " + web3.toHex(tx_token))

                time.sleep(10)

            pancakeswap2_txn = swap_function(
                data['amountIn'],
                data['amountOutMin'],
                data['path'],
                sender_address,
                (int(time.time()) + 100)
            ).buildTransaction({
                'from': sender_address,
                'gas': int(int(trx['gas'], 0) * (1 + gas_percent / 100)),
                'gasPrice': int(int(trx['gasPrice'], 0) * (1 + gas_percent / 100)),
                'nonce': web3.eth.get_transaction_count(sender_address),
            })

            signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=private_key)
            tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            print(web3.toHex(tx_token))


def check_holders_1k(token_address):
    url = f"https://api.covalenthq.com/v1/56/tokens/{token_address}/token_holders/?format=JSON&page-size=1000&key={covalent_api_key}"

    res = requests.get(url).json()
    # print(res)
    try:
        if int(res['error_code']) == 406:
            print("Too many Holders")
            return True
    except:
        pass
    holders = res['data']['items']
    print(len(holders))

    return len(holders) == 1000


def get_latest_trxs():
    url = f"https://api.bscscan.com/api?module=account&action=tokentx&address={address_to_track}&page=1&offset=10&startblock=0&endblock=999999999&sort=desc&apikey={bscan_api_key}"
    res = requests.get(url).json()
    # print(res)
    print(res)
    global trx_list
    print("List :", trx_list)
    if trx_list == []:
        trx_list = [i['hash'] for i in res['result']]
        return

    if str(res['status']) == '0':
        print("BSCscan API not working")
        return

    for trx in res['result']:

        if trx['hash'] not in trx_list:
            print('Sent Tokens ' if trx['from'].lower() == address_to_track.lower() else "Got tokens ", trx)
            print(f"{int(trx['value']) / 10 ** 18} {trx['tokenSymbol']}")
            # Carry out trade
            check_success = check_holders_1k(trx['contractAddress'])
            if check_success:
                try:
                    swap_token(trx['hash'])
                except Exception as e:
                    print(f'Error: {e}')


            trx_list.append(trx)


while True:
    get_latest_trxs()
    time.sleep(0.2)
