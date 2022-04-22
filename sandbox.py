import pandas_ta as ta
import ccxt

ex = ccxt.coinbasepro()
coin = 'XYO/USD'
info = ex.fetch_ticker(coin)
print(info)