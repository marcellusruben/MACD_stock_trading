# -*- coding: utf-8 -*-

class DataFeed(object):
    
    def __init__(self, df, history, indicators):
        
        self.df = df
        self.indicators = indicators
        self.history = history
   
        
    def get_values(self):
        
        self.date = self.df['date']
        self.open = self.df['open']
        self.high = self.df['high']
        self.low = self.df['low']
        self.close = self.df['close']
        self.volume = self.df['volume']
        
        self.values = [self.date, self.open, self.high, self.low, self.close, self.volume]
        
        return self.values

    def get_indicators(self):
        
            self.macd = self.df['macd']
            self.macds = self.df['macds']
            
            self.macd_all = [self.macd, self.macds]
            
            return self.macd_all