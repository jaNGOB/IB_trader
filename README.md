# IB_trader

The goal of this will be to have a IB trader up and running.

## Goal
This is a simple implementation of a trading strategy which uses tick data to perform trades.

## Installation
1. Download this repository locally
2. Navigate to the repository in your terminal
2. Install dependencies by running
```
pip install -r requirements.txt
```

## Usage
1. Open a paper account on IB
2. Download TWS and open the application
3. Design a strategy by downloading data in the tests.ipynb and then translating it to a fully fledged strategy.py file. An example is given as the test_strategy.py which is a simple market making algorithm that waits on the bid and corrects its current level to a certain spread. This, of course, will not make any money so if you are not in the business of losing as much money as possible we would recommend designing a new strategy.
4. Start the Algorithm
```
python strategy.py
```

Have fun! :)
