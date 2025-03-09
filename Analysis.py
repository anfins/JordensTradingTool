import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

def getStockInfo(ticker):
    stock = yf.Ticker(ticker)   
    
    stockInfo = stock.info


    try:
        is_chinese = False
        if stockInfo["country"] == "China":
            is_chinese = True

        cny_to_usd = 0.1389
        

        # Convert values if Chinese stock
        multiplier = cny_to_usd if is_chinese else 1
        

        # Apply conversion to financial metrics
        market_cap = int(stockInfo.get("marketCap", 0) * multiplier)
        free_cash_flow = int(stockInfo.get("freeCashflow", 0) * multiplier)
        net_income = int(stockInfo.get("netIncomeToCommon", 0) * multiplier)
        total_debt = int(stockInfo.get("totalDebt", 0) * multiplier)
        
       
        stockData = {
            "Market Cap": market_cap,
            "Free Cash Flow": free_cash_flow,    
            "Free Cash Flow to Debt": free_cash_flow / total_debt if total_debt != 0 else 0,
            "Net Income": net_income,
            "Total Debt": total_debt,
            "Current Price": stockInfo.get("currentPrice", 0),  # Stock price is typically shown in local currency
            "52 Week Range": stockInfo.get("fiftyTwoWeekRange", "N/A"),
            "52 Week High Change": stockInfo.get("fiftyTwoWeekHighChange", 0),
            "Return on Equity": stockInfo.get("returnOnEquity", 0),
            "Held by Institutions": stockInfo.get("heldPercentInstitutions", 0) * 100,
            "Held by Insiders": stockInfo.get("heldPercentInsiders", 0) * 100,
            "Forward P/E": stockInfo.get("forwardPE", 0),
            "Currency": "USD (Converted)" if is_chinese else "USD"

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
    stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "BABA", "BIDU", "NFLX", "WBD", "SPOT", "TSLA", "F", "RDDT", "SNAP", "UBER"]
    stockData= {}
    for stock in stocks:
        stockData[stock] = getStockInfo(stock)


    stockDf = pd.DataFrame(stockData).T
    plotData(stockDf, "Market Cap")
    plotData(stockDf, "Free Cash Flow")
    plotData(stockDf, "Net Income")
    plotData(stockDf, "Total Debt")
    plotData(stockDf, "Free Cash Flow to Debt")

    print(stockDf)




if __name__ == '__main__':
    main()
