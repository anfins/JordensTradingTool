import streamlit as st
import matplotlib.pyplot as plt
import os
import yfinance as yf
import pandas as pd
import numpy as np
import json

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

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


def getStockNews(ticker):
    stock = yf.Ticker(ticker)
    newsData = stock.news

    newsArray = []
    
    for article in newsData:
        if 'content' in article and 'summary' in article['content']:
            summary = article['content']['summary']
            title = article['content']['title']
            sentiment = sid.polarity_scores(summary)["compound"]
            newsArray.append([title, summary, sentiment])
            print([title, summary, sentiment])
    
    return newsArray if newsArray else []


def get_sentiment_color(sentiment_score):
    """Return a color based on sentiment score"""
    if sentiment_score >= 0.5:
        return "#00CC00"  # Strong positive - green
    elif sentiment_score > 0:
        return "#88CC88"  # Weak positive - light green
    elif sentiment_score == 0:
        return "#CCCCCC"  # Neutral - gray
    elif sentiment_score > -0.5:
        return "#CC8888"  # Weak negative - light red
    else:
        return "#CC0000"  # Strong negative - red



def main():
    
    # Enter stock ticker
    ticker = st.text_input("Enter a stock ticker (e.g., AAPL, MSFT, GOOGL):", "AAPL")

    if ticker or st.button("Get Stock Info"):
        with st.spinner("Fetching Data"):
            stock_data = getStockInfo(ticker)
            stock_news = getStockNews(ticker)
            
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

            # Display news if available
            if stock_news:
                st.subheader("Recent News")
                st.markdown("""
                <style>
                .sentiment-circle {
                    height: 15px;
                    width: 15px;
                    border-radius: 50%;
                    display: inline-block;
                    margin-right: 10px;
                }
                </style>
                """, unsafe_allow_html=True)
                
                for row in stock_news:
                    title = row[0]
                    summary = row[1]
                    sentiment = row[2]
                    
                    # Get color based on sentiment
                    color = get_sentiment_color(sentiment)
                    
                    # Display title with sentiment circle
                    st.markdown(f"""
                    <h3>
                      <span class="sentiment-circle" style="background-color: {color};"></span>
                      {title}
                    </h3>
                    """, unsafe_allow_html=True)
                    
                    st.write(summary)
                    
                    # Create a label for the sentiment score
                    sentiment_label = "Very Positive" if sentiment >= 0.5 else "Positive" if sentiment > 0 else "Neutral" if sentiment == 0 else "Negative" if sentiment > -0.5 else "Very Negative"
                    st.write(f"Sentiment: {sentiment:.2f} ({sentiment_label})")
                    st.write("---")
            else:
                st.info("No news articles available for this stock.")
           

           

if __name__ == "__main__":
    main()
