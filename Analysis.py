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
            "Net Income": stockInfo["netIncomeToCommon"],
            "Total Debt": stockInfo["totalDebt"],
            "Current Price": stockInfo["currentPrice"],
            "52 Week Range": stockInfo["fiftyTwoWeekRange"],
            "52 Week High Change": stockInfo["fiftyTwoWeekHighChange"],
            "Return on Equity": stockInfo["returnOnEquity"],
            "Held by Institutions": stockInfo["heldPercentInstitutions"] * 100,
            "Held by Insiders": stockInfo["heldPercentInsiders"] * 100,
            "Forward P/E": stockInfo["forwardPE"],
        }
        return stockData
    except Exception as e:
        print(f"Error: {e}")


def plotData(stockDf, passedVal):
    stockDf = stockDf.dropna(subset=[passedVal])
    
    # Plot Market Cap
    plt.figure(figsize=(12, 6))
    stockDf[passedVal].plot(kind="bar", color="skyblue", edgecolor="black")
    plt.title(passedVal +  " of Selected Stocks")
    plt.xlabel("Stock")
    plt.ylabel(passedVal + " (in USD)")
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()  # Added to ensure labels fit properly
    # Save the plot instead of showing it
    plt.savefig(f"Plots/{passedVal.replace('/', '_')}_plot.png")
    plt.close()  # Close the figure to free memory
    
def main():
    # Create a Stock object
    stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "BABA", "BIDU", "NFLX", "SPOT", "TSLA", "F", "RDDT", "SNAP"]
    stockData= {}
    for stock in stocks:
        stockData[stock] = getStockInfo(stock)


    stockDf = pd.DataFrame(stockData).T
    plotData(stockDf, "Market Cap")
    plotData(stockDf, "Free Cash Flow")
    plotData(stockDf, "Net Income")
    plotData(stockDf, "Total Debt")




if __name__ == '__main__':
    main()
