
import yfinance as yf
import pandas as pd
import numpy as np


class Stock:
    def __init__(self, ticker):
        self.ticker = ticker.upper()
        self.ticker_obj = yf.Ticker(self.ticker)
        self.cashflow = self.get_cashflow()
        self.balance_sheet = self.get_balance_sheet()
        self.income_statement = self.get_income_statement()
        self.allFinancials= pd.concat([self.cashflow, self.balance_sheet, self.income_statement], axis=1).sort_index()
    def get_cashflow(self):
        return pd.DataFrame(self.ticker_obj.cashflow).replace({np.nan: np.NaN})

    def get_balance_sheet(self):
        return pd.DataFrame(self.ticker_obj.balance_sheet).replace({np.nan: np.NaN})
    
    def get_income_statement(self):
        return pd.DataFrame(self.ticker_obj.financials).replace({np.nan: np.NaN})
