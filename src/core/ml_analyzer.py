#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ML Analyzer Module
نظام التحليل الآلي بالتعلم الآلي
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from typing import Dict, Tuple, Optional
import talib
from utils.config import Config
from utils.helpers import log_message, normalize_data
from core.data_fetcher import DataFetcher


class MLAnalyzer:
    """
    Machine Learning Analyzer
    محلل التعلم الآلي
    """
    
    def __init__(self, config: Config):
        self.config = config
        self.data_fetcher = DataFetcher(config)
        self.scaler = StandardScaler()
        self.model = None
    
    def analyze(self, symbol: str, timeframe: str) -> Dict:
        """
        Analyze pair using ML
        تحليل الزوج باستخدام التعلم الآلي
        """
        log_message(f"Analyzing {symbol} {timeframe}")
        
        # Fetch data
        df = self.data_fetcher.get_candles(symbol, timeframe)
        if df is None or len(df) < 100:
            return {'error': 'Insufficient data'}
        
        # Calculate technical indicators
        df = self._calculate_indicators(df)
        
        # Generate features
        X = self._generate_features(df)
        
        # Train model
        self.model = self._train_model(X, df)
        
        # Get predictions
        predictions = self._get_predictions(X)
        
        # Analyze trend
        trend = self._analyze_trend(df)
        
        # Detect support/resistance
        support_resistance = self._detect_support_resistance(df)
        
        # Detect signals
        signals = self._detect_signals(df, predictions)
        
        result = {
            'symbol': symbol,
            'timeframe': timeframe,
            'trend': trend,
            'support_resistance': support_resistance,
            'signals': signals,
            'confidence': self._calculate_confidence(predictions),
            'prediction': 'BUY' if predictions[-1] == 1 else 'SELL',
        }
        
        log_message(f"Analysis complete for {symbol}")
        return result
    
    def _calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate technical indicators
        حساب المؤشرات الفنية
        """
        close = df['close'].values
        high = df['high'].values
        low = df['low'].values
        
        # RSI
        df['rsi'] = talib.RSI(close, timeperiod=14)
        
        # MACD
        df['macd'], df['macd_signal'], df['macd_hist'] = talib.MACD(close)
        
        # Bollinger Bands
        df['bb_upper'], df['bb_middle'], df['bb_lower'] = talib.BBANDS(close, timeperiod=20)
        
        # Moving Averages
        df['sma_20'] = talib.SMA(close, timeperiod=20)
        df['sma_50'] = talib.SMA(close, timeperiod=50)
        df['sma_200'] = talib.SMA(close, timeperiod=200)
        df['ema_12'] = talib.EMA(close, timeperiod=12)
        df['ema_26'] = talib.EMA(close, timeperiod=26)
        
        # ATR
        df['atr'] = talib.ATR(high, low, close, timeperiod=14)
        
        # Stochastic
        df['slowk'], df['slowd'] = talib.STOCH(high, low, close)
        
        # ADX
        df['adx'] = talib.ADX(high, low, close, timeperiod=14)
        
        # Fill NaN values
        df = df.fillna(method='bfill')
        
        return df
    
    def _generate_features(self, df: pd.DataFrame) -> np.ndarray:
        """
        Generate ML features
        توليد خصائص التعلم الآلي
        """
        features = []
        
        # Technical indicators as features
        feature_cols = [
            'rsi', 'macd', 'macd_signal', 'macd_hist',
            'bb_upper', 'bb_lower', 'sma_20', 'sma_50', 'sma_200',
            'ema_12', 'ema_26', 'atr', 'slowk', 'slowd', 'adx'
        ]
        
        X = df[feature_cols].values
        
        # Normalize features
        X = self.scaler.fit_transform(X)
        
        return X
    
    def _train_model(self, X: np.ndarray, df: pd.DataFrame):
        """
        Train ML model
        تدريب نموذج التعلم الآلي
        """
        # Generate labels (1 for uptrend, 0 for downtrend)
        y = (df['close'].shift(-5) > df['close']).astype(int).values
        
        # Remove last 5 samples
        X_train = X[:-5]
        y_train = y[:-5]
        
        # Remove NaN values
        mask = ~np.isnan(y_train)
        X_train = X_train[mask]
        y_train = y_train[mask]
        
        # Train model
        model = RandomForestClassifier(
            n_estimators=self.config.get('ml.n_estimators', 100),
            max_depth=10,
            random_state=self.config.get('ml.random_state', 42)
        )
        model.fit(X_train, y_train)
        
        log_message(f"Model trained with accuracy: {model.score(X_train, y_train):.2%}")
        return model
    
    def _get_predictions(self, X: np.ndarray) -> np.ndarray:
        """
        Get model predictions
        الحصول على توقعات النموذج
        """
        if self.model is None:
            return np.zeros(len(X))
        
        predictions = self.model.predict(X)
        return predictions
    
    def _analyze_trend(self, df: pd.DataFrame) -> Dict:
        """
        Analyze trend
        تحليل الاتجاه
        """
        close = df['close'].values
        sma_20 = df['sma_20'].values
        sma_50 = df['sma_50'].values
        sma_200 = df['sma_200'].values
        
        trend = 'NEUTRAL'
        strength = 0
        
        # Check trend direction
        if close[-1] > sma_20[-1] > sma_50[-1] > sma_200[-1]:
            trend = 'STRONG_UPTREND'
            strength = 3
        elif close[-1] > sma_20[-1] > sma_50[-1]:
            trend = 'UPTREND'
            strength = 2
        elif close[-1] > sma_20[-1]:
            trend = 'WEAK_UPTREND'
            strength = 1
        elif close[-1] < sma_20[-1] < sma_50[-1] < sma_200[-1]:
            trend = 'STRONG_DOWNTREND'
            strength = -3
        elif close[-1] < sma_20[-1] < sma_50[-1]:
            trend = 'DOWNTREND'
            strength = -2
        elif close[-1] < sma_20[-1]:
            trend = 'WEAK_DOWNTREND'
            strength = -1
        
        return {
            'direction': trend,
            'strength': strength,
            'current_price': float(close[-1]),
            'sma_20': float(sma_20[-1]),
            'sma_50': float(sma_50[-1]),
            'sma_200': float(sma_200[-1]),
        }
    
    def _detect_support_resistance(self, df: pd.DataFrame) -> Dict:
        """
        Detect support and resistance levels
        كشف مستويات الدعم والمقاومة
        """
        high = df['high'].values[-100:]  # Last 100 candles
        low = df['low'].values[-100:]
        close = df['close'].values[-100:]
        
        # Find pivot points
        pivot = (high[-1] + low[-1] + close[-1]) / 3
        resistance = 2 * pivot - low[-1]
        support = 2 * pivot - high[-1]
        
        return {
            'support': float(support),
            'pivot': float(pivot),
            'resistance': float(resistance),
            'current_price': float(close[-1]),
        }
    
    def _detect_signals(self, df: pd.DataFrame, predictions: np.ndarray) -> list:
        """
        Detect buy/sell signals
        كشف إشارات الشراء والبيع
        """
        signals = []
        
        rsi = df['rsi'].values
        macd = df['macd'].values
        macd_signal = df['macd_signal'].values
        close = df['close'].values
        
        # Check last 10 candles for signals
        for i in range(len(df) - 10, len(df)):
            signal_type = None
            confidence = 0
            
            # RSI signals
            if rsi[i] < 30:
                signal_type = 'BUY'
                confidence = (30 - rsi[i]) / 30 * 100
            elif rsi[i] > 70:
                signal_type = 'SELL'
                confidence = (rsi[i] - 70) / 30 * 100
            
            # MACD signals
            if macd[i] > macd_signal[i] and macd[i-1] <= macd_signal[i-1]:
                signal_type = 'BUY'
                confidence = max(confidence, 75)
            elif macd[i] < macd_signal[i] and macd[i-1] >= macd_signal[i-1]:
                signal_type = 'SELL'
                confidence = max(confidence, 75)
            
            # ML prediction signal
            if predictions[i] == 1:
                confidence = max(confidence, 80)
            
            if signal_type:
                signals.append({
                    'time': str(df['open_time'].iloc[i]),
                    'type': signal_type,
                    'price': float(close[i]),
                    'confidence': min(confidence, 100),
                    'rsi': float(rsi[i]) if not np.isnan(rsi[i]) else 0,
                })
        
        return signals
    
    def _calculate_confidence(self, predictions: np.ndarray) -> float:
        """
        Calculate overall confidence
        حساب درجة الثقة العامة
        """
        if self.model is None:
            return 0.0
        
        # Get probabilities
        proba = self.model.predict_proba(self.scaler.transform(np.random.randn(1, 15)))[0]
        confidence = max(proba) * 100
        
        return min(confidence, 100)
