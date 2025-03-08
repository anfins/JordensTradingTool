import yfinance as yf
import pandas as pd
import numpy as np

import Stock as st
def main():
    # Create a Stock object
    goog = st.Stock("GOOG")
    print(goog.income_statement)
    incomeStatement = goog.income_statement
    incomeStatement = incomeStatement.dropna()
    print(incomeStatement)


if __name__ == '__main__':
    main()
