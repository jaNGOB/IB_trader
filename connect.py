"""
Connection class


"""
from ib_insync import *
import asyncio

class ib_connect:
    def __init__(self, host='127.0.0.1', port=7497, client_id=1):
        self.host = host
        self.port = port
        self.client_id = client_id
        self.ticker = None

        self.ib = IB()

    def open_connection(self):
        """ open the connection to IB """
        self.ib.connect(self.host, self.port, clientId=self.client_id)

    def close_connection(self):
        """ close the connection to IB """
        self.ib.disconnect()

    def start_stream(self, ticker, loopback_function):
        """

        :param ticker: 
        :param loopback_function: 
        """

        self.ticker = Forex(ticker)

        self.ib.reqMktData(self.ticker)
        self.ib.pendingTickersEvent += loopback_function

        while self.ib.waitOnUpdate():
            self.ib.sleep(1)
    
    def create_marketorder(self, action, amount):
        marketOrder = MarketOrder(action = action, totalQuantity= amount)
        trade = self.ib.placeOrder(self.ticker, marketOrder) 
    
    def create_limitorder(self, ticker, amount, limit):
        pass

    def cancel_order(self, id):
        pass

    def check_order_status(self, id):
        pass

