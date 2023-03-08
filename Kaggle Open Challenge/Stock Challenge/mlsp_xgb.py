# -*- coding: utf-8 -*-
"""MLSP XGB.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iZ2gOsrBy1KrgcXRc1fdln-jtV8C-0BB
"""

!pip install yfinance
!pip install statsmodels==0.11.0

import os, contextlib
import pandas as pd
import yfinance as yf

if not os.path.exists("stocks data"):
    os.mkdir("stocks data")
    
url = "https://en.wikipedia.org/wiki/NASDAQ-100#Components"
html = pd.read_html(url, header=0)
series = html[4]["Ticker"]
symbols = series.to_list()

with open(os.devnull, "w") as devnull:
    with contextlib.redirect_stdout(devnull):
        for i, symbol in enumerate(symbols):
            data = yf.download(symbol, period="max")["Close"]
            data.to_csv("stocks data/{}.csv".format(symbol))

import numpy as np
import pandas as pd
import matplotlib as plt
import yfinance as yf
import plotly.express as px
from datetime import datetime
from statsmodels.tsa.stattools import acf , pacf
from statsmodels.graphics.tsaplots import plot_acf
import matplotlib.pyplot as plt
import xgboost as xgb

final_forecasts = {}
p = 2
q = 1
prediction_length = 5
d = {}
valid_size = 0.15

for symbol in symbols:
    stock = yf.download(symbol, period="MAX", Interval="1d", verbose=False)
    # closing_prices = stock.Close.dropna()
    # original_cp = closing_prices
    # assert closing_prices.isnull().sum() == 0
    # d_counter = 0
    # while not stationarity_test(closing_prices):
    #     closing_prices = closing_prices.diff(1).bfill()
    #     d_counter += 1
    # d[symbol] = d_counter

    df = stock
    valid_split_idx = int(df.shape[0] * (1-(valid_size)))

    train_df  = df[:valid_split_idx].copy()
    valid_df  = df[valid_split_idx:-5].copy()
    test_df   = df[-5:].copy()
    y_train = train_df['Close'][5:].copy()
    X_train = train_df.drop(['Close'], 1)[:-5]

    y_valid = valid_df['Close'].copy()
    X_valid = valid_df.drop(['Close'], 1)

    y_test  = test_df['Close'].copy()
    X_test  = test_df.drop(['Close'], 1)
    eval_set = [(X_train, y_train), (X_valid, y_valid)]

    # train_closing_prices = original_cp[:-prediction_length]
    # test_closing_prices = original_cp[-prediction_length:]
    # model = ARIMA(train_closing_prices, order=(2, 1, 1))
    xgb_params = {'gamma': 0.001, 'learning_rate': 0.05, 'max_depth': 12, 'n_estimators': 300, 'random_state': 42}
    model = xgb.XGBRegressor(**xgb_params, objective='reg:squarederror')
    model.fit(X_train, y_train, eval_set=eval_set, verbose=False)

    # try:
    #     model_fit = model.fit(disp=0)
    # except Exception as e:
    #     print(f"An exception occurred")
    #     continue

    forecast = model.predict(X_test)[:5]
    final_forecasts[symbol] = forecast



import numpy as np
np.save('forecasts_companies.npy', final_forecasts)

forecast

