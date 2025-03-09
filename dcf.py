import yfinance as yf
import pandas as pd
import numpy as np


def getStockInfo(ticker):
    stock = yf.Ticker(ticker)   
    stockInfo = stock.info
    #print(stockInfo.keys())

    print(ticker)
    print(f"Current Price: ${stockInfo['currentPrice']:,.2f}")
    print(stockInfo["financialCurrency"])
    print(stockInfo["exchange"])
    print(f"Market Cap: ${stockInfo['marketCap']:,.2f}")
    print(stockInfo["forwardPE"])
    print(f"Free Cash Flow: ${stockInfo['freeCashflow']:,.2f}")


    
def main():
    # Create a Stock object
    getStockInfo("AAPL")
    getStockInfo("MSFT")
    getStockInfo("GOOGL")
    getStockInfo("AMZN")
    getStockInfo("BABA")
    getStockInfo("BIDU")
    getStockInfo("NFLX")
    getStockInfo("TSLA")
    


if __name__ == '__main__':
    main()
