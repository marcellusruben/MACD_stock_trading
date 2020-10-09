# -*- coding: utf-8 -*-

import plotly.graph_objs as go
import plotly.io as pio
pio.renderers.default = "browser"
import pandas as pd
import numpy as np

def viz_candlestick(df):
    
    fig = go.Figure(data = [go.Candlestick(x = df['date'],
                open = df['open'],
                high = df['high'],
                low = df['low'],
                close = df['close'],
                name = 'OHLC')])

    
    return fig

def viz_macd(df):
    
    macd = go.Scatter(x = df['date'], y = df['macd'], name = 'MACD Line')
    macd_s = go.Scatter(x = df['date'], y = df['macds'], name = 'MACD Signal')
    macd_h = go.Bar(x = df['date'], y = df['macdh'], name = 'MACD Histogram')
    data = [macd, macd_s, macd_h]
    fig_macd = go.Figure(data = data)
   
    return fig_macd

def viz_trade_decision(df, net, indicators):
    
    net_df = pd.DataFrame(np.array(net), columns = ['date', 'close', 'status', 'profit', 'stock'])

    net_df['date'] = pd.to_datetime(net_df['date'])
    

    def SetColor(x):
    
        if(x == 1):
            return "red"
        elif(x == 0):
            return "green"

    color = list(map(SetColor, net_df['status']))
    
    net_df['color'] = color
    
    net_df_buy = net_df[net_df['status'] == 1]
    net_df_sell = net_df[net_df['status'] == 0]

    data_points = go.Scatter(
                    x = df['date'], 
                    y = df['close'],
                    name = 'Close Price',
                    mode = 'lines'
                    )
    
    buy_points = go.Scatter(
                    x = net_df_buy['date'], 
                    y = net_df_buy['close'],
                    customdata = np.dstack((net_df_buy['stock'], net_df_buy['profit'])),
                    name = 'Buy',
                    mode = 'markers',
                    text = ['Date: %s<br>Stock: %d<br>Profit: $%d'%(d,t,s) for d,t,s in net_df_buy.loc[:,['date','stock','profit']].values],
                    marker = dict(color = net_df_buy['color']) 
                    )  

    sell_points = go.Scatter(
                    x = net_df_sell['date'], 
                    y = net_df_sell['close'],
                    name = 'Sell',
                    mode = 'markers',
                    text = ['Date: %s<br>Stock: %d<br>Profit: $%d'%(d,t,s) for d,t,s in net_df_sell.loc[:,['date','stock','profit']].values],
                    marker = dict(color = net_df_sell['color']))
    
    data = [data_points, buy_points, sell_points]
    
    fig = go.Figure(data = data)
    
    return fig
