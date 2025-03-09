import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import os


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
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Filter out NaN values
    filtered_df = stockDf.dropna(subset=[passedVal])
    
    if filtered_df.empty:
        st.warning(f"No data available for {passedVal}")
        return
    
    filtered_df[passedVal].plot(kind="bar", color="skyblue", edgecolor="black", ax=ax)
    plt.title(f"{passedVal} of Selected Stocks")
    plt.xlabel("Stock")
    plt.ylabel(f"{passedVal} (in USD)")
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()

    # Return the figure to be displayed in Streamlit
    return fig



def main():
    # Create a Stock object
    stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "BABA", "BIDU", "NFLX", "WBD", "SPOT", "TSLA", "F", "RDDT", "SNAP", "UBER"]
    stockData= {}
    for stock in stocks:
        stockData[stock] = getStockInfo(stock)

    stockDf = pd.DataFrame(stockData).T
    stockDf = stockDf.sort_values(by="Market Cap", ascending=False)

    # Progress bar for data loading
    progress_bar = st.progress(0)


    # Display the raw data
    st.subheader("Stock Financial Data")
    st.dataframe(stockDf)

    # Create metrics to display
    metrics = ["Market Cap", "Free Cash Flow", "Net Income", "Total Debt", "Free Cash Flow to Debt"]
    
    # Add option to select additional metrics
    selected_metric = st.selectbox("Select a metric to visualize:", metrics)
    
    # Plot the selected metric
    st.subheader(f"{selected_metric} Comparison")
    fig = plotData(stockDf, selected_metric)
    if fig:
        st.pyplot(fig)



if __name__ == '__main__':
    main()
