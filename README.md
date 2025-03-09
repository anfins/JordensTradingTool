# JordensTradingTool

I created this project to have my own custom site to use to evaluating stocks. It is primarily built via using the yfinance package to access financial data, so a huge shout out to the team that has provided the capability to do so. To use the RAG capability implemented in the repo, I suggest aquiring your own ChatGPT API key, creating your own env file, and adding it there.

## Repo Roadmap

**Requirements.txt** The packages that need to be installed in order for this repo to function as intended (use pip install -r requirements.txt) to bulk install all the needed packages

**Main.py**: implements a streamlit app that allows a user to query for stock info

**AnalyzeER.py** Scrapes inputted earnings reports and summarizes the information using a RAG

