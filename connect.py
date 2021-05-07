"""
Connection class


"""
from ib_insync import *

class ib_connect:
    def __init__(self, host='127.0.0.1', port=7497, client_id=1):
        """
        Initial parameters of the IB Connection.
        """
        self.host = host
        self.port = port
        self.client_id = client_id

        self.open_order = False
        self.ticker = None

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

        self.ib.reqMktData(self.ticker)
        self.ib.pendingTickersEvent += loopback_function

        while self.ib.waitOnUpdate():
            self.ib.sleep(1)
    

    def order_filled(self, trade):
        """ Routine to report that a trade is executed """
        self.open_order = False
        

    def create_marketorder(self, action: str, amount: int):
        """

        :param action:
        :param amount:
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


    def cancel_order(self, id_):
        """
        cancel orders.

        :param id: orderID that needs to be canceled. 
        """
        self.ib.cancelOrder(id_)


    def check_order_status(self, id_):
        status = id_.orderStatus.status
        while id_.isDone():
            print('pending')
            self.ib.sleep(5)


    def balance_check(self, amount: int) -> bool:
        """
        This function checks if there is enough money left in the account 
        to execute the current trade.

        :param amount: (int) number of shares that will be traded
        :return: (bool) True if enough is available, false otherwise.
        """
        available = available_balance()
        if available >= amount: return True
        else: return False


    def available_balance(self) -> float:
        """
        Fetch the current available balance on our account.

        :return (int): available balance.
        """
        account = ib.accountSummary()
        available = account[10].value
        return available
