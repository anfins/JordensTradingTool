import yfinance as yf
import pandas as pd
import numpy as np


def getStockInfo(ticker):
    stock = yf.Ticker(ticker)   
    stockInfo = stock.info
    #print(stockInfo.keys())

    print(f"Ticker: {ticker}")
    print(f"Current Price: ${stockInfo['currentPrice']:,.2f}")
    print(f"Previous Close: ${stockInfo['previousClose']:,.2f}")
    print(f"Shares Outstanding: {stockInfo['sharesOutstanding']:,.0f}")
    print(f"Shares Short: {stockInfo['sharesShort']:,.0f}")
    print(f"Short Ratio: {stockInfo['shortRatio']:.2f}")
    print(f"Currency: {stockInfo['financialCurrency']}")
    print(f"Earnings Growth: ${stockInfo['earningsGrowth']*100:,.2f}%")
    print(f"52 Week Range: {stockInfo['fiftyTwoWeekRange']}")
    print(f"Held by Institutions: {stockInfo['heldPercentInstitutions'] * 100:.2f}%")
    print(f"Held by Insiders: {stockInfo['heldPercentInsiders'] * 100:.2f}%")
    print(f"Market Cap: ${stockInfo['marketCap']:,.2f}")
    print(f"Forward P/E: {stockInfo['forwardPE']}")
    print(f"Free Cash Flow: ${stockInfo['freeCashflow']:,.2f}")
    print("-----------------------------")

    
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
