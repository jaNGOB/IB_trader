"""
Connection class that serves as the backbone of the strategy.
It contains the functionalities of a trading strategy so to separate the
process of creating the strategy and the technical part.

June, 2021
"""
from ib_insync import *
import nest_asyncio
nest_asyncio.apply()

class ib_connect:
    def __init__(self, host='127.0.0.1', port=7497, client_id=1):
        """
        Initial parameters of the IB Connection.
        """
        self.host = host            # Localhost
        self.port = port            # Port IB uses.
        self.client_id = client_id 

        self.open_order = False     # flag if there are open orders
        self.ticker = None          # flag that will take the ticker of the strategy file.

        self.ib = IB()


    def open_connection(self):
        """ open the connection to IB """
        self.ib.connect(self.host, self.port, clientId=self.client_id)


    def close_connection(self):
        """ close the connection to IB """
        self.ib.disconnect()


    def start_stream(self, asset: str, ticker: str, loopback_function: str):
        """
        This function will connect to IB and start the stream of incoming tick data.

        :param asset: forex or stock
        :param ticker: Ticker of the asset that will be traded.
        :param loopback_function: Name of the function that will be used to process incoming ticks.
        """
        if asset == 'forex':
            self.ticker = Forex(ticker)
        elif asset == 'stock':
            self.ticker = Stock(ticker, 'CHIXCH', 'CHF')
            
        self.ib.qualifyContracts(self.ticker)
        self.ib.reqMktData(self.ticker)
        self.ib.pendingTickersEvent += loopback_function
        
        while self.ib.waitOnUpdate():
            self.ib.sleep(1)
    

    def order_filled(self, trade):
        """ Routine to report that a trade is executed """
        print('Trade Executed')
        self.open_order = False
        

    def create_marketorder(self, action: str, amount: int):
        """
        Create a market order and return the order id or false if not 
        enough money is available.

        :param action: Buy or Sell.
        :param amount: amount of shares to trade.
        :return: orderId
        """
        if self.balance_check(amount):
            marketOrder = MarketOrder(action = action, totalQuantity= amount)
            order = self.ib.placeOrder(self.ticker, marketOrder) 
            order.filledEvent += self.order_filled
            return order.order
        else:
            print('Not enough money left')
            return False
   

    def create_limitorder(self, action: str, amount: int, limit: float):
        """
        Create a limit order and save the order id.
        
        :param action: Buy or sell.
        :param amount: amount of shares to trade.
        :param limit: Limit price at which the trade will be entered.
        :return: orderID.
        """
        limitOrder = LimitOrder(action = action, totalQuantity= amount, lmtPrice = round(limit, 5))
        order = self.ib.placeOrder(self.ticker, limitOrder)
        order.filledEvent += self.order_filled

        if order.orderStatus.status == 'Submitted':
            print('Limit{} order submitted @ {}'.format(action, round(limit, 5)))

        return order.order

        """
        if self.balance_check(amount):
            limitOrder = LimitOrder(action = action, totalQuantity= amount, lmtPrice = limit)
            order = self.ib.placeOrder(self.ticker, limitOrder)
            order.filledEvent += self.order_filled

            if order.orderStatus.status == 'Submitted':
                print('Limit{} order submitted @ {}'.format(action, limit))
            
            return order.order
        else:
            print('Not enough money left')
            return False

        """

    def modify_limit_order(self, order, limit: float):
        """
        Modify an existing limit order. Modification implemented is the change 
        of the limit itself. 

        :param order: Order that needs to be updated.
        :param limit: (float) new limit that needs to be set for the existing order.
        """
        order.lmtPrice = round(limit, 5)

        new_order = self.ib.placeOrder(self.ticker, order)
        new_order.filledEvent += self.order_filled

        if new_order.orderStatus.status == 'Submitted':
            print('Limit order modified @ {}'.format(limit))
        
        return new_order.order

    def cancel_order(self, id_):
        """
        cancel orders.

        :param id: orderID that needs to be canceled. 
        """
        self.ib.cancelOrder(id_)


    def check_order_status(self, id_):
        """
        This function will check the status of an order.
        If the order is still open, it will wait for 5 seconds 
        and check again if it is executed. 
        
        :param id_: orderID.
        """
        status = id_.orderStatus.status
        while id_.isDone():
            print('pending')
            self.ib.sleep(5)


    def balance_check(self, amount: int) -> bool:
        """
        This function checks if there is enough money left in the account 
        to execute the current trade.

        :param amount: (int) number of shares that will be traded.
        :return: (bool) True if enough is available, false otherwise.
        """
        available = self.available_balance()
        if float(available) >= amount: return True
        else: return False


    def available_balance(self) -> float:
        """
        Fetch the current available balance on our account.

        :return (int): available balance.
        """
        account = self.ib.accountSummary()
        available = account[10].value
        return available


    def open_orders(self) -> bool:
        """
        This function checks for open orders and returns True if there are open orders
        and False otherwise.
        """
        lst = self.ib.openTrades()
        if len(lst) == 0:
            return False
        return True


    def sleep(self, time: float) -> None:
        """
        Wait for 'time' seconds while everything keeps processing in the background.
        
        :param time: amount of time to sleep
        """
        self.ib.sleep(time)
