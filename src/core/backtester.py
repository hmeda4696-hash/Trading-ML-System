#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BackTester Module
نظام الاختبار التاريخي
"""

import numpy as np
import pandas as pd
from typing import Dict, List
from utils.config import Config
from utils.helpers import log_message
from core.data_fetcher import DataFetcher


class BackTester:
    """
    Backtesting Engine
    محرك الاختبار التاريخي
    """
    
    def __init__(self, config: Config):
        self.config = config
        self.data_fetcher = DataFetcher(config)
    
    def run(self, symbol: str, analysis_result: Dict) -> Dict:
        """
        Run backtest
        تشغيل الاختبار التاريخي
        """
        log_message(f"Starting backtest for {symbol}")
        
        # Fetch historical data
        timeframe = 'D1'  # Daily
        bars = 252 * 2  # 2 years
        df = self.data_fetcher.get_candles(symbol, timeframe, bars)
        
        if df is None or len(df) < 100:
            return {'error': 'Insufficient data for backtest'}
        
        # Generate trading signals based on analysis
        signals = self._generate_signals(df, analysis_result)
        
        # Run trades
        trades = self._run_trades(df, signals)
        
        # Calculate statistics
        stats = self._calculate_statistics(df, trades)
        
        log_message(f"Backtest complete - Total Profit: {stats['total_profit']:.2f}")
        
        return {
            'symbol': symbol,
            'trades': trades,
            'total_trades': len(trades),
            'winning_trades': len([t for t in trades if t['profit'] > 0]),
            'losing_trades': len([t for t in trades if t['profit'] < 0]),
            'total_profit': stats['total_profit'],
            'win_rate': stats['win_rate'],
            'profit_factor': stats['profit_factor'],
            'max_drawdown': stats['max_drawdown'],
            'equity_curve': stats['equity_curve'].tolist(),
        }
    
    def _generate_signals(self, df: pd.DataFrame, analysis_result: Dict) -> List[Dict]:
        """
        Generate trading signals
        توليد إشارات التداول
        """
        signals = []
        
        close = df['close'].values
        sma_20 = self._calculate_sma(close, 20)
        sma_50 = self._calculate_sma(close, 50)
        
        for i in range(50, len(df) - 5):
            signal = None
            
            # Crossover signals
            if sma_20[i-1] <= sma_50[i-1] and sma_20[i] > sma_50[i]:
                signal = 'BUY'
            elif sma_20[i-1] >= sma_50[i-1] and sma_20[i] < sma_50[i]:
                signal = 'SELL'
            
            if signal:
                signals.append({
                    'time': i,
                    'type': signal,
                    'price': float(close[i]),
                })
        
        return signals
    
    def _run_trades(self, df: pd.DataFrame, signals: List[Dict]) -> List[Dict]:
        """
        Run trades based on signals
        تشغيل الصفقات بناءً على الإشارات
        """
        trades = []
        buy_price = None
        buy_time = None
        
        close = df['close'].values
        
        for signal in signals:
            time = signal['time']
            signal_type = signal['type']
            price = close[time]
            
            if signal_type == 'BUY' and buy_price is None:
                buy_price = price
                buy_time = time
            
            elif signal_type == 'SELL' and buy_price is not None:
                profit = price - buy_price
                profit_pips = profit * 10000  # For major pairs
                
                trades.append({
                    'buy_time': int(buy_time),
                    'sell_time': int(time),
                    'buy_price': float(buy_price),
                    'sell_price': float(price),
                    'profit': float(profit),
                    'profit_pips': float(profit_pips),
                })
                
                buy_price = None
                buy_time = None
        
        return trades
    
    def _calculate_sma(self, data: np.ndarray, period: int) -> np.ndarray:
        """
        Calculate Simple Moving Average
        حساب المتوسط المتحرك البسيط
        """
        return pd.Series(data).rolling(window=period).mean().values
    
    def _calculate_statistics(self, df: pd.DataFrame, trades: List[Dict]) -> Dict:
        """
        Calculate backtest statistics
        حساب إحصائيات الاختبار
        """
        if not trades:
            return {
                'total_profit': 0,
                'win_rate': 0,
                'profit_factor': 0,
                'max_drawdown': 0,
                'equity_curve': np.array([self.config.get('backtesting.initial_capital', 10000)]),
            }
        
        initial_capital = self.config.get('backtesting.initial_capital', 10000)
        equity = initial_capital
        equity_curve = [equity]
        
        gross_profit = 0
        gross_loss = 0
        winning_trades = 0
        losing_trades = 0
        
        for trade in trades:
            profit = trade['profit']
            equity += profit
            equity_curve.append(equity)
            
            if profit > 0:
                gross_profit += profit
                winning_trades += 1
            else:
                gross_loss += abs(profit)
                losing_trades += 1
        
        total_profit = equity - initial_capital
        win_rate = (winning_trades / len(trades) * 100) if trades else 0
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else 0
        max_drawdown = self._calculate_max_drawdown(np.array(equity_curve))
        
        return {
            'total_profit': total_profit,
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'max_drawdown': max_drawdown,
            'equity_curve': np.array(equity_curve),
        }
    
    def _calculate_max_drawdown(self, equity: np.ndarray) -> float:
        """
        Calculate maximum drawdown
        حساب أقصى خسارة متتالية
        """
        running_max = np.maximum.accumulate(equity)
        drawdown = (equity - running_max) / running_max
        return float(np.min(drawdown) * 100)
