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
lookback = 100

data = np.array([0,0,0,0])


ib = ibc.ib_connect()
ib.open_connection()
print('Connection established')

def print_statement():
    pass

def trade_logic():
    """
    This is the main function that will perform the trading strategy itself.
    It will be called every time a new tick arrives to check the trading condition.
    If the dicision is made to trade, the trades are directly executed using functions
    defined in the connect.py file.
    """
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
    """
    This function processes incoming ticks and saves them to a local dataframe.
    The dataframe is then cut so it will only contain the n most recent ticks 
    necessary for the trading strategy.

    :param tick: tick from IB that needs to be processed. 
    """

    data = np.append(data, (tick.askSize, tick.ask, tick.bid, tick.bidSize))

    if len(data) > lookback:
        data = data[4:]

def new_tick(tickers):
    """
    This function is the main loopback function which will be automatically executed 
    by IB whenever a new tick arrives. The tick is then added to the local dataframe
    using process_ticks and then the trading logic is executed.
    """
    for ticker in tickers:
        process_ticks(ticker)

    trade_logic()

ib.start_stream('EURUSD', new_tick)
