import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

def getStockInfo(ticker):
    stock = yf.Ticker(ticker)   
    stockInfo = stock.info

    try:
        stockData = {
            "Market Cap": stockInfo["marketCap"],
            "Free Cash Flow": stockInfo["freeCashflow"],    
            "Total Revenue": stockInfo["totalRevenue"],
            "Current Price": stockInfo["currentPrice"],
            "52 Week Range": stockInfo["fiftyTwoWeekRange"],
            "52 Week High Change": stockInfo["fiftyTwoWeekHighChange"],
            "Held by Institutions": stockInfo["heldPercentInstitutions"],
            "Held by Insiders": stockInfo["heldPercentInsiders"],
            "Forward P/E": stockInfo["forwardPE"],
        }
        return stockData
    except Exception as e:
        print(f"Error: {e}")


def plotStockData(stockData, passedVal):
    stockDf = pd.DataFrame(stockData)
    stockDf[passedVal] = stockDf[passedVal].astype(float)
    
    plt.figure(figsize=(10, 6))
    stockDf['Market Cap'].plot(kind='bar')
    plt.title('Market Cap of Selected Stocks')
    plt.xlabel('Stock Ticker')
    plt.ylabel('Market Cap (in billions)')
    plt.xticks(rotation=45)
    plt.show()


    
def main():
    # Create a Stock object
    stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "BABA", "BIDU", "NFLX", "SPOT", "TSLA", "F", "RDDT", "SNAP"]
    stockData= {}
    for stock in stocks:
        stockData[stock] = getStockInfo(stock)

    plotStockData(stockData, "Market Cap")

if __name__ == '__main__':
    main()
