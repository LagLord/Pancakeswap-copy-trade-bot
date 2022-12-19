import asyncio
import inspect
import time
from threading import Thread
import requests
from hexbytes import HexBytes
from web3.datastructures import AttributeDict
from config2 import *
from web3 import Web3
import warnings
import sys, os

# sys.stdout = open(f"{os.getcwd()}/output.txt", "w")
print("test sys.stdout")

warnings.filterwarnings("ignore")

trx_list = []
holdings = {}
# abi = '[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'
abi = '[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'

lp_abi = '''[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount0Out","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1Out","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Swap","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint112","name":"reserve0","type":"uint112"},{"indexed":false,"internalType":"uint112","name":"reserve1","type":"uint112"}],"name":"Sync","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"MINIMUM_LIQUIDITY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"burn","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_token0","type":"address"},{"internalType":"address","name":"_token1","type":"address"}],"name":"initialize","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"mint","outputs":[{"internalType":"uint256","name":"liquidity","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"price0CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"price1CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"skim","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount0Out","type":"uint256"},{"internalType":"uint256","name":"amount1Out","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"swap","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"sync","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]'''

web3 = Web3(Web3.HTTPProvider(bsc2))

if web3.isConnected(): print("Connected to BSC")

bsc2 = "https://bsc.getblock.io/d966a047-cc84-4595-b0bc-586be1a124c5/mainnet/"
web2 = Web3(Web3.HTTPProvider(bsc2))
if web2.isConnected(): print("Connected to BSC web2")

lp_contract = web3.eth.contract(address=web3.toChecksumAddress('0x6dB23b5360c9D2859fDcbf41c56494e7b8573649'),
                                abi=lp_abi)


def get_trx_receipt(trx):
    url = f"https://api.bscscan.com/api?module=proxy&action=eth_getTransactionReceipt&txhash={trx}&apikey={bscan_api_key}"
    res = requests.get(url).json()
    if res['result']:
        return res['result']
    else:
        return None


def decode_swap(data_list):
    return_data = {'path': []}
    to = None
    from_ = data_list[0]['topics'][1]
    for data in data_list:
        hash = data['topics'][0]
        try:
            hash = data['topics'][0].hex()
        except:
            pass
        if hash.lower() == transfer_hash:
            data = dict(data)
            address = data['address']
            input_data = int(data['data'], 16)
            print(input_data)
            if to is None or to == data['topics'][1]:
                return_data['path'].append(web3.toChecksumAddress(address))
                if 'amountIn' not in return_data:
                    return_data['amountIn'] = input_data
                else:
                    if from_ == data['topics'][-1]:
                        return_data['amountOutMin'] = input_data
                        print(return_data)
                        return return_data
                to = data['topics'][-1]


def decode_data(receipt):
    decoded = receipt
    # print(decoded['effectiveGasPrice'], decoded['to'], decoded['gasUsed'], decoded)
    main_dict = {}
    print(decoded['logs'])
    for trx in decoded['logs']:
        hash = trx['topics'][0]
        try:
            hash = trx['topics'][0].hex()
        except:
            pass
        if hash.lower() == swap_hash:
            trx = dict(trx)
            # print('LP contract address: ', trx['address'])

            try:

                main_dict = decode_swap(decoded['logs'])

            except Exception as e:
                print("Decoding Failed!", e)
            break

    # print(main_dict)
    return main_dict


rec = dict(web2.eth.get_transaction_receipt('0x1561b551a91e2df8a2e64d010a282c6c13d32d825b3fd55ef1e1ad2b071d3de3'))
print(rec)
decode_data(rec)
# tec = dict(web2.eth.get_transaction('0x1561b551a91e2df8a2e64d010a282c6c13d32d825b3fd55ef1e1ad2b071d3de3'))

pancakeswap_address = web3.toChecksumAddress(pancakeswap_address)
router = pancakeswap_address
# Setup the PancakeSwap contract
# panbi = get_abi(pancakeswap_address)
address_to_track = web3.toChecksumAddress(address_to_track)
contract_to_track = web3.toChecksumAddress(contract_to_track)
holding_address = web3.toChecksumAddress(holding_address)
track_list = [address_to_track, holding_address]
if address_to_track == holding_address:
    track_list = [address_to_track]
sender_address = web3.toChecksumAddress(my_address)

nonce = None
print("Nonce ", nonce)

contract = web3.eth.contract(address=web3.toChecksumAddress(pancakeswap_address.upper()), abi=abi)

for token in token_addresses:

    token_addresses[token] = web3.toChecksumAddress(token_addresses[token])
    sellTokenContract = web3.eth.contract(token_addresses[token], abi=short_abi)
    x = sellTokenContract.functions.allowance(sender_address, pancakeswap_address).call()
    balance = sellTokenContract.functions.balanceOf(sender_address).call()

    # print("Allowance: ", x)
    if int(x) < int(balance):
        old_nonce = web3.eth.get_transaction_count(sender_address)
        approve = sellTokenContract.functions.approve(web3.toChecksumAddress(pancakeswap_address),
                                                      balance * 10000).buildTransaction({
            'from': sender_address,
            'gasPrice': web3.toWei(7, 'gwei'),
            'nonce': old_nonce,
        })

        signed_txn = web3.eth.account.sign_transaction(approve, private_key=private_key)
        tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        nonce = old_nonce
        # print("Approved: " + web3.toHex(tx_token))
        time.sleep(10)



# start = time.time()
# sellTokenContract2 = web3.eth.contract(web3.toChecksumAddress('0x55d398326f99059fF775485246999027B3197955'), abi='[{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]')
# balance = sellTokenContract2.functions.balanceOf(sender_address).call()
# print(balance)
# end = time.time()
# print(end-start)


async def handle_event(event):
    try:
        # remove the quotes in the transaction hash
        # print(event)
        transaction = Web3.toJSON(event).strip('"')
        # use the transaction hash (that we removed the '"' from to get the details of the transaction
        # start = time.time()
        transaction = dict(web3.eth.get_transaction(transaction))

        # end = time.time()
        # print(end - start)
        # print(transaction)
        # set the variable to the "to" address in the message
        to = web3.toChecksumAddress(transaction['to'])
        # print(transaction['transactionHash'].hex(), to)
        # if the to address in the message is the router

        if to == contract_to_track:
            # print the transaction and its details
            # print(transaction)
            print('found_hash', transaction['hash'].hex())
            receipt = None
            try:
                receipt = web3.eth.get_transaction_receipt(transaction['hash'].hex())

            except:
                loop.create_task(get_receipt_force(transaction, transaction['hash'].hex()))
                return
            data = decode_data(receipt)
            # print(data)
            # print("Check STARTED")
            # check_success = check_holders_1k(data['path'][-1])

            if True:
                # print("HOLDER Check SUCCESS")
                try:
                    await swap_tokenv2(transaction, data)
                except Exception as e:
                    print(e)

        else:
            pass

    except Exception as err:
        # print transactions with errors. Expect to see transactions people submitted with errors
        pass
        # print(f'error: {err}: ', exc_tb.tb_lineno)


async def log_loop(event_filter, poll_interval):
    while True:
        added_tasks = []
        start = time.time()
        for event in event_filter.get_new_entries():
            task = loop.create_task(handle_event(event))
            added_tasks.append(task)

            # print(diff)
        results = await asyncio.gather(*added_tasks)
        end = time.time()
        diff = poll_interval - (end - start)
        print('done running tasks: ', abs(diff))
        await asyncio.sleep(abs(diff) if abs(diff) < poll_interval else 0)


async def get_receipt_force(trx, hash):
    receipt = None
    for i in range(0, 15):
        try:
            receipt = web3.eth.get_transaction_receipt(hash)
            break
        except:
            try:
                receipt = web2.eth.get_transaction_receipt(hash)
                break
            except:
                await asyncio.sleep(0.4)
    if receipt == None:
        print("Can't retrieve receipt for : ", hash)
        return
    data = decode_data(receipt)
    # print(data)
    # print("Check STARTED")
    # check_success = check_holders_1k(data['path'][-1])

    if True:
        # print("HOLDER Check SUCCESS")
        try:
            await swap_tokenv2(trx, data)
        except Exception as e:
            print(e)


async def swap_tokenv2(receipt, data):
    data, trx = data, dict(receipt)
    if data['path'] != []:
        global nonce
        # print(balance)
        # print(int(trx['value']), int(int(trx['gas']) * (1 + gas_percent / 100)),
        #       int(int(trx['gasPrice']) * (1 + gas_percent / 100)))
        # print(web3.toWei(int(trx['value']) / 10 ** 18, 'ether'))
        # print(web3.toWei(int(trx['gas']) * int(trx['gasPrice']) / 10 ** 18, 'ether'))
        print("Swap_started")
        if data['amountOutMin']:
            data['amountOutMin'] = int(data['amountOutMin'] * (1 - extra_slippage_percent / 100))

        if 'amountIn' not in data and 'amountOut' not in data:

            data['amountIn'] = int(trx['value']) if int(trx['value']) <= max_limit['BNB'] * (10 ** 18) else max_limit[
                                                                                                                'BNB'] * (
                                                                                                                    10 ** 18)
            if data['amountIn'] == max_limit['BNB'] * (10 ** 18):
                data['amountOutMin'] = int(data['amountOutMin'] * int(trx['value']) / data['amountIn'])

        elif data['path'][0] == token_addresses['BUSD'] or data['path'][0] == token_addresses['USDT']:
            old_amount = data['amountIn']
            data['amountIn'] = data['amountIn'] if int(data['amountIn']) <= max_limit['BUSD'] * (10 ** 18) else \
                max_limit['BUSD'] * (10 ** 18)
            if data['amountIn'] == max_limit['BUSD'] * (10 ** 18):
                data['amountOutMin'] = int(data['amountOutMin'] * data['amountIn'] / old_amount)
        try:
            if data['amountIn'] > holdings[data['path'][0]]:
                if holdings[data['path'][0]] == 0:
                    return
                old_amount = data['amountIn']
                data['amountIn'] = holdings[data['path'][0]]
                data['amountOutMin'] = int(data['amountOutMin'] * data['amountIn'] / old_amount)

        except:
            pass
        try:
            if data['amountInMax'] > holdings[data['path'][0]]:
                if holdings[data['path'][0]] == 0:
                    return
                old_amount = data['amountInMax']
                data['amountInMax'] = holdings[data['path'][0]]
                data['amountOut'] = int(data['amountOut'] * data['amountIn'] / old_amount)

        except:
            pass

        # print("amountIn: ", data['amountIn'])
        old_nonce = web3.eth.get_transaction_count(sender_address)
        if token_addresses['WBNB'] == data['path'][0]:

            old_value = data['amountIn']
            data['amountIn'] = old_value if old_value <= max_limit['BNB'] * (10 ** 18) else max_limit[
                                                                                                'BNB'] * (
                                                                                                    10 ** 18)

            data['amountIn'] = int(data['amountIn'])

            if data['amountIn'] == max_limit['BNB'] * (10 ** 18):
                data['amountOutMin'] = int(data['amountOutMin'] * data['amountIn'] / old_value)

            pancakeswap2_txn = contract.functions.swapExactETHForTokensSupportingFeeOnTransferTokens(
                data['amountOutMin'],
                data['path'],
                sender_address,
                (int(time.time()) + 100)
            ).buildTransaction({
                'from': sender_address,
                'value': data['amountIn'],
                'gas': int(int(trx['gas']) * (1 + gas_percent / 100)),
                'gasPrice': int(int(trx['gasPrice']) * (1 + gas_percent / 100)),
                'nonce': old_nonce if old_nonce != nonce else nonce + 1,
            })

            signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=private_key)
            tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            print(web3.toHex(tx_token))
            nonce = old_nonce

        elif token_addresses['WBNB'] == data['path'][-1]:
            pancakeswap2_txn = contract.functions.swapExactTokensForETHSupportingFeeOnTransferTokens(
                data['amountIn'],
                data['amountOutMin'],
                data['path'],
                sender_address,
                (int(time.time()) + 100)
            ).buildTransaction({
                'from': sender_address,
                'gas': int(int(trx['gas']) * (1 + gas_percent / 100)),
                'gasPrice': int(int(trx['gasPrice']) * (1 + gas_percent / 100)),
                'nonce': old_nonce if old_nonce != nonce else nonce + 1,
            })

            signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=private_key)
            tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            print(web3.toHex(tx_token))
            nonce = old_nonce

        else:

            pancakeswap2_txn = contract.functions.swapExactTokensForTokensSupportingFeeOnTransferTokens(
                data['amountIn'],
                data['amountOutMin'],
                data['path'],
                sender_address,
                (int(time.time()) + 100)
            ).buildTransaction({
                'from': sender_address,
                'gas': int(int(trx['gas']) * (1 + gas_percent / 100)),
                'gasPrice': int(int(trx['gasPrice']) * (1 + gas_percent / 100)),
                'nonce': old_nonce if old_nonce != nonce else nonce + 1,
            })

            signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=private_key)
            print("signed")
            tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            print(web3.toHex(tx_token))
            nonce = old_nonce

        sellTokenContract = web3.eth.contract(data['path'][-1], abi=short_abi)
        x = sellTokenContract.functions.allowance(sender_address, pancakeswap_address).call()

        # print("Allowance: ", x)
        old_nonce = web3.eth.get_transaction_count(my_address)
        if int(x) < data['amountOutMin'] * 10 ** 4:
            approve = sellTokenContract.functions.approve(web3.toChecksumAddress(pancakeswap_address),
                                                          data['amountOutMin'] * 10 ** 6).buildTransaction({
                'from': sender_address,
                'gasPrice': int(int(trx['gasPrice']) * (1 + gas_percent / 100)),
                'nonce': old_nonce if old_nonce != nonce else nonce + 1,
            })

            signed_txn = web3.eth.account.sign_transaction(approve, private_key=private_key)
            tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            nonce = old_nonce
            # print("Approved: " + web3.toHex(tx_token))
        sellTokenContract2 = web3.eth.contract(data['path'][0], abi=short_abi)

        await asyncio.sleep(15)
        balance = sellTokenContract.functions.balanceOf(sender_address).call()
        if data['path'][-1] not in list(token_addresses.values()):
            holdings[data['path'][-1]] = int(balance)

        balance2 = sellTokenContract2.functions.balanceOf(sender_address).call()
        if data['path'][0] not in list(token_addresses.values()):
            holdings[data['path'][0]] = int(balance2)
    else:
        print("Not a Swap Transaction")


loop = asyncio.get_event_loop()

def main():
    # filter for pending transactions
    tx_filter = web3.eth.filter('pending')

    # print(tx_filter.get_all_entries())

    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(tx_filter, 3)))
    finally:
        loop.close()


if __name__ == '__main__':
    main()
