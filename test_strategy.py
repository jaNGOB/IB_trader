"""
Example of a trading strategy implementation.

Jan Gobeli, 07.05.2021.
"""
import numpy as np
import tableprint as tp
from datetime import datetime
import connect as ibc

### PARAMETERS ###
amount = 5          # Amount that will be traded on each signal.
t_ticker = 'EURUSD'   # Trading ticker.
last_buy = None     # 
in_long = False     # Flag to check if we are currently in a position.
lookback = 100      # Amount of data is needed for the trade logic.

spread = 0.00002
trade_open = False

###################

data = np.array([0])

ib = ibc.ib_connect()
ib.open_connection()

print('Connection established')

def print_statement():
    """
    Print a table using tableprint containing relevant information captured by the 
    loopback function.
    """
    headers = ['Time', 'Midprice']
    out = [[datetime.now(), data[-1]]]
    tp.table(out, headers, style='clean')


def print_trade(side: str, price: float) -> print:
    """
    Print statement that will output the trade submitted and at which price to the
    terminal that runs the code.

    :param side: (str) which side of the trade was submitted
    :param price: (float) at which price was the trade submitted
    """
    print('--------------------------------')
    print('Submitted a {} order at {}'.format(side, price))
    print('--------------------------------')


def trade_logic():
    """
    This is the main function that will perform the trading strategy itself.
    It will be called every time a new tick arrives to check the trading condition.
    If the dicision is made to trade, the trades are directly executed using functions
    defined in the connect.py file.
    """
    global in_long
    global trade_open
    global last_buy

    ib.sleep(2)

    something_open = ib.open_orders()

    if something_open:
        if in_long:
            last_buy = ib.modify_limit_order(last_buy, data[-1] - spread)
        else:
            last_buy = ib.modify_limit_order(last_buy, data[-1] + spread)
    else:
        able_to_trade = ib.balance_check(amount)
        if not in_long and able_to_trade:
            last_buy = ib.create_limitorder('Buy', amount, data[-1] - spread)
            print_trade('Buy', data[-1] - spread)
            in_long = True

        elif able_to_trade:
            last_buy = ib.create_limitorder('Sell', amount, data[-1] + spread)
            print_trade('Sell', data[-1] - spread)
            in_long = False

    """
    #if not in_long and (data[-1] < data[-4]) and (data[-3] < data[-7]):
    if not in_long and (data[-2] >= data[-3]):
        ib.create_marketorder('BUY', amount)
        last_buy = data[-3]
        in_long = True

    if in_long and data[-2] > last_buy:
        in_long = False
        ib.create_marketorder('SELL', amount)
    """

def process_ticks(tick):
    """
    This function processes incoming ticks and saves them to a local dataframe.
    The dataframe is then cut so it will only contain the n most recent ticks 
    necessary for the trading strategy.

    :param tick: tick from IB that needs to be processed. 
    """
    global data

    #data = np.append(data, (tick.askSize, tick.ask, tick.bid, tick.bidSize))
    data = np.append(data, ((tick.ask + tick.bid) / 2))
    print_statement()

    if len(data) > lookback:
        data = data[1:]


def new_tick(tickers):
    """
    This function is the main loopback function which will be automatically executed 
    by IB whenever a new tick arrives. The tick is then added to the local dataframe
    using process_ticks and then the trading logic is executed.

    :param tickers: Tick changes in the market.
    """
    for ticker in tickers:  
        process_ticks(ticker)

    trade_logic()

ib.start_stream('forex', t_ticker, new_tick)
