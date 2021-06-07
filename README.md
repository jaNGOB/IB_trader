# IB_trader

The goal of this will be to have a IB trader up and running.

## Goal
This is a simple implementation of a trading strategy which uses tick data to perform trades.

## Installation
1. Install this repository locally
2. Install dependencies by running
```
pip install -r requirements.txt
```
Dependencies needed:
- ib_insync
- nest_asyncio
- tableprint
- datetime
- numpy

## Usage
1. Open a paper account on IB
2. Download TWS and run it in the background
3. Design a strategy by downloading data in the tests.ipynb and then translating it to a fully fledged strategy.py file. An example is given as the test_strategy.py which is a simple market making algorithm that waits on the bid and corrects its current level to a certain spread.
4. ???
5. Profit :)
