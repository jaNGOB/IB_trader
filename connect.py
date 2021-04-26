"""
Connection class


"""
from ib_insync import *

class ib_connect(Object):
    def __init__(self, host='127.0.0.1', port=7497, client_id=1):
        self.host = host
        self.port = port
        self.client_id = client_id

        self.ib = IB()

    def open_connection(self):
        """ open the connection to IB """
        self.ib.connect(self.host, self.port, clientId=self.client_id)

    def close_connection(self):
        """ close the connection to IB """
        self.ib.disconnect()

    def start_stream(self, ticker):
        pass

    def new_tick(self, tickers):
        for t in tickers:
            
    
    def create_marketorder(self, ticker, amount):
        pass
    
    def create_limitorder(self, ticker, amount, limit):
        pass

    def cancel_order(self, id):
        pass

    def check_order_status(self, id):
        pass

