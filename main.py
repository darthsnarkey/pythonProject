import pandas as pd
import pandas_ta as ta
from pandasgui import show
import ccxt, csv, time

def get_indicators(df, bid):
    st_10 = df.ta.supertrend(period=10, multiplier=3)
    st_11 = df.ta.supertrend(period=11, multiplier=2)
    st_12 = df.ta.supertrend(period=12, multiplier=1)
    sts = [st_10, st_11, st_12]
    st_res = supert(sts)
    ema = df.ta.ema(period=200)
    zscore = df.ta.zscore(period=21).abs()
    if ema.iloc[-1] < bid:
        ema = True
    else:
        ema = False
    zscore = df.ta.zscore()
    rsi = df.ta.rsi()
    if rsi.iloc[-1] > 50:
        if rsi.iloc[-1] > 80:
            rsiw = 'Oversold'
        else:
            rsiw = 'Up'
    elif rsi.iloc[-1] < 50:
        if rsi.iloc[-1] < 20:
            rsiw = 'Overbought'
        else:
            rsiw = 'Down'
    adx = df.ta.adx()
    if adx.iloc[-1,1] > 25:
        adxw = True
    else:
        adxw = False
    if st_res == True and ema == True and rsiw == 'Oversold' and adxw == True and zscore.iloc[-1] > 0:
        sig = 'Buy'
    else:
        sig = 'Neutral'
    return pd.DataFrame(data=[st_res, ema, rsiw, adxw, zscore.iloc[-1], sig])

def supert(sts):
    count=0
    for st in sts:
        if st.iloc[-1,1] == 1:
            count = count+1
    if count >= 2:
        return True
    else:
        return False

def get_info(coin_df, coins, p):
    for coin in coins:
        data = exchange.fetch_ohlcv(coin, timeframe=p)
        bid_raw = exchange.fetch_ticker(coin)
        df = pd.DataFrame(data, columns=["Time", "Open", "High", "Low", "Close", "Volume"])
        bid = bid_raw['bid']
        symbol = bid_raw['symbol']
        coin_df[bid_raw['symbol']] = get_indicators(df, bid)
    return coin_df
def main_app(p, coin_df,coins):
    coin_df = get_info(coin_df, coins, p)
    coin_df = coin_df.transpose()
    show(coin_df)
exchange = ccxt.coinbasepro()
coins = []
with open('./coins', newline='') as f:
    for row in csv.reader(f):
        coins.append(row[0])
    f.close()
cnt = 1
p = '15m'
coin_df = pd.DataFrame()
main_app(p, coin_df, coins)

