# -*- coding: utf-8 -*-

import yfinance as yf
from stockstats import StockDataFrame as sdf
import trader as T
import visualization as viz

tickerSymbol = 'AAPL'

tickerData = yf.Ticker(tickerSymbol)

tickerDf = tickerData.history(period='1d', start='2020-1-1', end='2020-6-1')

tickerDf.reset_index(inplace=True)

df_daily = sdf.retype(tickerDf)
df_daily.get('macd')

stock_add = 1
indicator = 'macd'

df_daily.reset_index(inplace=True)
profit, net = T.Trader(df_daily, indicator, stock_add).trading_decision()
profit_regular = (stock_add*df_daily['close'].iloc[-1]) - (stock_add*df_daily['close'].iloc[0])

print('Profit MACD: '+str(profit))
print('Profit keep and sell: '+str(profit_regular))

fig = viz.viz_candlestick(df_daily)
fig.update_layout(title={
        'text': "Candlestick Chart",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show()

fig_macd = viz.viz_macd(df_daily)
fig_macd.update_layout(title={
        'text': "MACD Indicator",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
fig_macd.show()

fig_decision = viz.viz_trade_decision(df_daily, net, indicator)
fig_decision.update_layout(title={
        'text': "Trade Decision",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
fig_decision.show()
