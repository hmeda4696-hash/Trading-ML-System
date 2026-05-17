#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Fetcher Module
جلب بيانات الأزواج من MT5
"""

import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from utils.config import Config
from utils.helpers import log_message


class DataFetcher:
    """
    Fetch data from MetaTrader5
    جلب البيانات من MetaTrader5
    """
    
    def __init__(self, config: Config):
        self.config = config
        self.is_connected = False
        self.connect()
    
    def connect(self) -> bool:
        """
        Connect to MT5
        الاتصال بـ MT5
        """
        try:
            if not mt5.initialize():
                log_message("Failed to initialize MT5", "ERROR")
                return False
            self.is_connected = True
            log_message("Connected to MT5 successfully")
            return True
        except Exception as e:
            log_message(f"MT5 Connection Error: {e}", "ERROR")
            return False
    
    def disconnect(self):
        """
        Disconnect from MT5
        قطع الاتصال بـ MT5
        """
        mt5.shutdown()
        self.is_connected = False
        log_message("Disconnected from MT5")
    
    def get_candles(self, symbol: str, timeframe: str, bars: int = 500) -> Optional[pd.DataFrame]:
        """
        Get candle data from MT5
        جلب بيانات الشموع من MT5
        """
        if not self.is_connected:
            if not self.connect():
                return None
        
        try:
            # Convert timeframe string to MT5 timeframe constant
            tf_map = {
                'M1': mt5.TIMEFRAME_M1,
                'M5': mt5.TIMEFRAME_M5,
                'M15': mt5.TIMEFRAME_M15,
                'M30': mt5.TIMEFRAME_M30,
                'H1': mt5.TIMEFRAME_H1,
                'H4': mt5.TIMEFRAME_H4,
                'D1': mt5.TIMEFRAME_D1,
                'W1': mt5.TIMEFRAME_W1,
            }
            
            mt5_timeframe = tf_map.get(timeframe, mt5.TIMEFRAME_H1)
            
            # Get rates
            rates = mt5.copy_rates_from_pos(symbol, mt5_timeframe, 0, bars)
            
            if rates is None or len(rates) == 0:
                log_message(f"No data for {symbol} {timeframe}", "WARNING")
                return None
            
            # Convert to DataFrame
            df = pd.DataFrame(rates)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            df.columns = ['open_time', 'open', 'high', 'low', 'close', 'tick_volume', 'spread', 'real_volume']
            
            log_message(f"Fetched {len(df)} candles for {symbol} {timeframe}")
            return df
        
        except Exception as e:
            log_message(f"Error fetching candles: {e}", "ERROR")
            return None
    
    def get_account_info(self) -> Optional[Dict]:
        """
        Get account information
        الحصول على معلومات الحساب
        """
        try:
            account_info = mt5.account_info()
            if account_info is None:
                return None
            
            return {
                'balance': account_info.balance,
                'equity': account_info.equity,
                'margin': account_info.margin,
                'margin_free': account_info.margin_free,
                'leverage': account_info.leverage,
            }
        except Exception as e:
            log_message(f"Error getting account info: {e}", "ERROR")
            return None
    
    def get_symbol_info(self, symbol: str) -> Optional[Dict]:
        """
        Get symbol information
        الحصول على معلومات الرمز
        """
        try:
            info = mt5.symbol_info(symbol)
            if info is None:
                return None
            
            return {
                'symbol': symbol,
                'bid': info.bid,
                'ask': info.ask,
                'point': info.point,
                'digits': info.digits,
                'spread': info.spread,
                'tick_value': info.tick_value,
            }
        except Exception as e:
            log_message(f"Error getting symbol info: {e}", "ERROR")
            return None
