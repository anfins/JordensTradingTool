import streamlit as st
import matplotlib.pyplot as plt
import os
import yfinance as yf
import pandas as pd
import numpy as np


def getStockInfo(ticker):
    stock = yf.Ticker(ticker)   
    
    stockInfo = stock.info

    try:
        is_chinese = False
        if stockInfo.get("country") == "China":
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
            "Currency": "USD (Converted)" if is_chinese else "USD",
            "Description": stockInfo.get("longBusinessSummary", "No description available.")
        }
        return stockData
    except Exception as e:
        st.error(f"Error: {e}")
        return {}


def main():
    
    # Enter stock ticker
    ticker = st.text_input("Enter a stock ticker (e.g., AAPL, MSFT, GOOGL):", "AAPL")

    if ticker or st.button("Get Stock Info"):
        with st.spinner("Fetching Data"):
            stock_data = getStockInfo(ticker)
            
            if not stock_data:
                st.warning(f"Could not retrieve data for {ticker}")
                return
                
            # Current price and market metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Current Price", f"${stock_data.get('Current Price', 0):.2f}")
            with col2:
                st.metric("Market Cap", f"${stock_data.get('Market Cap', 0):,}")
            with col3:
                st.metric("Forward P/E", f"{stock_data.get('Forward P/E', 0):.2f}")
            
            # Financial metrics
            st.subheader("Financial Metrics")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Free Cash Flow", f"${stock_data.get('Free Cash Flow', 0):,}")
                st.metric("Net Income", f"${stock_data.get('Net Income', 0):,}")
                st.metric("Return on Equity", f"{stock_data.get('Return on Equity', 0)*100:.2f}%")
            
            with col2:
                st.metric("Total Debt", f"${stock_data.get('Total Debt', 0):,}")
                st.metric("Free Cash Flow to Debt", f"{stock_data.get('Free Cash Flow to Debt', 0):.2f}")
                
            # Ownership info
            st.subheader("Ownership")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Institutional Ownership", f"{stock_data.get('Held by Institutions', 0):.2f}%")
            with col2:
                st.metric("Insider Ownership", f"{stock_data.get('Held by Insiders', 0):.2f}%")
            
            # Company description
            st.subheader("Company Description")
            st.write(stock_data.get("Description", "No description available."))


if __name__ == "__main__":
    main()