"""
Example of a trading strategy.
"""
import asyncio
import numpy as np
import connect as ibc


amount = 5
ticker = 'EURUSD'
last_buy = None
in_long = False

data = np.array([0,0,0,0])


ib = ibc.ib_connect()
ib.open_connection()
print('Connection established')

def trade_logic():
    global in_long
    global last_buy

    #if not in_long and (data[-1] < data[-4]) and (data[-3] < data[-7]):
    if not in_long and (data[-2] >= data[-3]):
        ib.create_marketorder('BUY', amount)
        last_buy = data[-3]
        in_long = True

    if in_long and data[-2] > last_buy:
        in_long = False
        ib.create_marketorder('SELL', amount)

def process_ticks(tick):
    global data

    data = np.append(data, (tick.askSize, tick.ask, tick.bid, tick.bidSize))

    if len(data) > 100:
        data = data[4:]

def new_tick(tickers):
    for ticker in tickers:
        process_ticks(ticker)

    trade_logic()

ib.start_stream('EURUSD', new_tick)