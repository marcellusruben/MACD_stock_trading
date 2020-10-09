# -*- coding: utf-8 -*-

import datafeed as DF

class Trader(object):
    
    def __init__(self, df_daily, indicators, stock_add):
        
       
        self.df_daily = df_daily
        self.indicators = indicators
        self.stock_add = stock_add
    
    def state_check(self, value, indicators):
    
            
        check = lambda x, y: 1 if x > y else 0
        self.state = check(value[0], value[1])
        
        return self.state
        
    def trading_rules(self, ohlc_value, indicator_value_daily, indicators, stock_left, max_stock_amt, stock_amt, profit, transaction):
        
            
        self.buy_condition = ((indicator_value_daily[0] > indicator_value_daily[1]) and stock_left != 0)
        self.sell_condition = ((indicator_value_daily[0] < indicator_value_daily[1]) and stock_amt != 0)
        
        if self.buy_condition == True:
            
            
                stock_amt += self.stock_add
                profit = profit - (self.stock_add * ohlc_value[4])
                self.transaction.append([ohlc_value[0], ohlc_value[4], 1, profit, stock_amt])
                            
        
        if self.sell_condition == True:
            

                profit = profit + (self.stock_add * ohlc_value[4])
                stock_amt -= self.stock_add
                self.transaction.append([ohlc_value[0], ohlc_value[4], 0, profit, stock_amt])

           
        return self.transaction, profit, stock_amt
    
        
    def trading_decision(self):
        
        self.ohlc_daily_hist = []
        self.transaction = []
        
        max_stock_amt = 1
    
        stock_amt = 0
        profit = 0
        
        self.df_daily.reset_index(inplace=True)
        self.prev_state_daily = 0

        for i in range (len(self.df_daily)):
            
            self.ohlc_daily = DF.DataFeed(self.df_daily.iloc[i], self.ohlc_daily_hist, self.indicators).get_values()
            self.indicator_daily = DF.DataFeed(self.df_daily.iloc[i], self.ohlc_daily_hist, self.indicators).get_indicators()
            
            self.current_state_daily = self.state_check(self.indicator_daily, self.indicators)
            
            
            stock_left = max_stock_amt - stock_amt
            
            if self.current_state_daily != self.prev_state_daily:
                
                self.transaction, profit, stock_amt = self.trading_rules(self.ohlc_daily, self.indicator_daily, self.indicators, stock_left, max_stock_amt, stock_amt, profit, self.transaction)
                
            if i == (len(self.df_daily)-1):
                
                if stock_amt != 0:
            
                    profit = profit + (stock_amt * self.ohlc_daily[4])
                    stock_amt = 0
                    self.transaction.append([self.ohlc_daily[0], self.ohlc_daily[4], 0, profit, stock_amt])
            
            self.prev_state_daily =  self.current_state_daily
        
           
        profit = self.transaction[-1][3]
        
        return profit, self.transaction
