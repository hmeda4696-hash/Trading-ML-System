#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PainX 800 AI Model - Advanced Neural Network
نموذج ذكاء اصطناعي متقدم متخصص لزوج PainX 800
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import talib
from typing import Dict, Tuple, Optional
import joblib
from pathlib import Path
from utils.config import Config
from utils.helpers import log_message


class PainX800AIModel:
    """
    Advanced AI Model for PainX 800
    نموذج ذكاء اصطناعي متقدم لـ PainX 800
    """
    
    def __init__(self, config: Config):
        self.config = config
        self.scaler = StandardScaler()
        self.price_scaler = MinMaxScaler()
        
        # Multiple models ensemble
        self.rf_model = None  # Random Forest
        self.gb_model = None  # Gradient Boosting
        self.nn_model = None  # Neural Network
        self.svm_model = None # Support Vector Machine
        
        self.is_trained = False
        self.model_dir = Path(config.base_dir) / 'models'
        self.model_dir.mkdir(exist_ok=True)
    
    def train(self, df: pd.DataFrame, lookback: int = 50) -> Dict:
        """
        Train AI models with ensemble approach
        تدريب نماذج الذكاء الاصطناعي بطريقة العصابة
        """
        log_message(f"Training AI Models for PainX 800 with {len(df)} candles")
        
        # Calculate advanced indicators
        df = self._calculate_advanced_indicators(df)
        
        # Generate features and labels
        X, y = self._generate_training_data(df, lookback)
        
        if len(X) < 100:
            log_message("Insufficient data for training", "WARNING")
            return {'error': 'Insufficient data'}
        
        # Normalize features
        X_scaled = self.scaler.fit_transform(X)
        
        # Split data
        split_idx = int(len(X_scaled) * 0.8)
        X_train, X_test = X_scaled[:split_idx], X_scaled[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        # Train ensemble models
        self._train_random_forest(X_train, y_train)
        self._train_gradient_boosting(X_train, y_train)
        self._train_neural_network(X_train, y_train)
        self._train_svm(X_train, y_train)
        
        # Evaluate
        metrics = self._evaluate_models(X_test, y_test)
        
        self.is_trained = True
        self._save_models()
        
        log_message(f"Training Complete - Accuracy: {metrics.get('ensemble_accuracy', 0):.2%}")
        return metrics
    
    def predict(self, df: pd.DataFrame, lookback: int = 50) -> Dict:
        """
        Make predictions using ensemble voting
        توقع الأسعار باستخدام نظام التصويت العصابي
        """
        if not self.is_trained:
            return {'error': 'Model not trained'}
        
        df = self._calculate_advanced_indicators(df)
        X = self._extract_features(df.tail(lookback).copy())
        
        if len(X) == 0:
            return {'error': 'Insufficient data'}
        
        X_scaled = self.scaler.transform(X)
        
        # Get predictions from all models
        predictions = self._ensemble_predict(X_scaled)
        
        # Calculate confidence
        confidence = predictions['confidence']
        signal = predictions['signal']  # 'BUY' or 'SELL'
        probability = predictions['probability']
        
        return {
            'signal': signal,
            'confidence': confidence,
            'probability': probability,
            'rf_vote': predictions['rf_vote'],
            'gb_vote': predictions['gb_vote'],
            'nn_vote': predictions['nn_vote'],
            'svm_vote': predictions['svm_vote'],
        }
    
    def _calculate_advanced_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate advanced technical indicators
        حساب مؤشرات فنية متقدمة
        """
        close = df['close'].values
        high = df['high'].values
        low = df['low'].values
        volume = df.get('tick_volume', np.ones(len(close))).values
        
        # Momentum Indicators
        df['rsi_14'] = talib.RSI(close, timeperiod=14)
        df['rsi_21'] = talib.RSI(close, timeperiod=21)
        df['stoch_k'], df['stoch_d'] = talib.STOCH(high, low, close)
        df['mom'] = talib.MOM(close, timeperiod=10)
        df['roc'] = talib.ROC(close, timeperiod=10)
        
        # Trend Indicators
        df['sma_10'] = talib.SMA(close, timeperiod=10)
        df['sma_20'] = talib.SMA(close, timeperiod=20)
        df['sma_50'] = talib.SMA(close, timeperiod=50)
        df['ema_12'] = talib.EMA(close, timeperiod=12)
        df['ema_26'] = talib.EMA(close, timeperiod=26)
        df['adx'] = talib.ADX(high, low, close, timeperiod=14)
        df['dx'] = talib.DX(high, low, close, timeperiod=14)
        
        # MACD
        df['macd'], df['macd_signal'], df['macd_hist'] = talib.MACD(close)
        
        # Bollinger Bands
        df['bb_upper'], df['bb_mid'], df['bb_lower'] = talib.BBANDS(close, timeperiod=20)
        df['bb_width'] = df['bb_upper'] - df['bb_lower']
        df['bb_position'] = (close - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'] + 1e-8)
        
        # ATR
        df['atr'] = talib.ATR(high, low, close, timeperiod=14)
        df['atr_sma'] = talib.SMA(df['atr'], timeperiod=14)
        
        # Volatility
        df['natr'] = talib.NATR(high, low, close, timeperiod=14)
        returns = np.diff(np.log(close))
        df['volatility'] = pd.Series(returns).rolling(20).std().values
        
        # Volume indicators
        df['obv'] = talib.OBV(close, volume)
        df['ad'] = talib.AD(high, low, close, volume)
        
        # CCI
        df['cci'] = talib.CCI(high, low, close, timeperiod=14)
        
        # Ichimoku
        df['tenkan'] = self._ichimoku_tenkan(high, low)
        df['kijun'] = self._ichimoku_kijun(high, low)
        
        # Price patterns
        df['high_low_diff'] = high - low
        df['close_open_diff'] = close - df['open']
        df['price_momentum'] = np.gradient(close, axis=0)
        
        # Fill NaN values
        df = df.fillna(method='bfill').fillna(method='ffill')
        
        return df
    
    def _ichimoku_tenkan(self, high: np.ndarray, low: np.ndarray, period: int = 9) -> np.ndarray:
        """Calculate Ichimoku Tenkan"""
        tenkan = []
        for i in range(len(high)):
            if i < period - 1:
                tenkan.append(0)
            else:
                period_high = np.max(high[i-period+1:i+1])
                period_low = np.min(low[i-period+1:i+1])
                tenkan.append((period_high + period_low) / 2)
        return np.array(tenkan)
    
    def _ichimoku_kijun(self, high: np.ndarray, low: np.ndarray, period: int = 26) -> np.ndarray:
        """Calculate Ichimoku Kijun"""
        kijun = []
        for i in range(len(high)):
            if i < period - 1:
                kijun.append(0)
            else:
                period_high = np.max(high[i-period+1:i+1])
                period_low = np.min(low[i-period+1:i+1])
                kijun.append((period_high + period_low) / 2)
        return np.array(kijun)
    
    def _generate_training_data(self, df: pd.DataFrame, lookback: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate training features and labels
        توليد بيانات التدريب
        """
        X = []
        y = []
        
        close = df['close'].values
        
        for i in range(lookback, len(df) - 5):
            # Extract features from lookback period
            features = self._extract_features(df.iloc[i-lookback:i].copy())
            if len(features) > 0:
                X.append(features[0])
                
                # Label: 1 if price goes up in next 5 candles, 0 otherwise
                future_return = (close[i+5] - close[i]) / close[i]
                label = 1 if future_return > 0.001 else 0
                y.append(label)
        
        return np.array(X), np.array(y)
    
    def _extract_features(self, df: pd.DataFrame) -> np.ndarray:
        """
        Extract features from dataframe
        استخراج الميزات من البيانات
        """
        features = []
        
        feature_cols = [
            'rsi_14', 'rsi_21', 'stoch_k', 'stoch_d', 'mom', 'roc',
            'sma_10', 'sma_20', 'sma_50', 'ema_12', 'ema_26', 'adx', 'dx',
            'macd', 'macd_signal', 'macd_hist',
            'bb_upper', 'bb_mid', 'bb_lower', 'bb_width', 'bb_position',
            'atr', 'atr_sma', 'natr', 'volatility',
            'obv', 'ad', 'cci', 'tenkan', 'kijun',
            'high_low_diff', 'close_open_diff', 'price_momentum'
        ]
        
        for col in feature_cols:
            if col in df.columns:
                features.append(df[col].values)
        
        if not features:
            return np.array([])
        
        # Stack features and get the last row
        stacked = np.column_stack(features)
        if len(stacked) > 0:
            return stacked[-1:]
        return np.array([])
    
    def _train_random_forest(self, X_train: np.ndarray, y_train: np.ndarray):
        """Train Random Forest"""
        self.rf_model = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        self.rf_model.fit(X_train, y_train)
        log_message(f"Random Forest trained - Accuracy: {self.rf_model.score(X_train, y_train):.2%}")
    
    def _train_gradient_boosting(self, X_train: np.ndarray, y_train: np.ndarray):
        """Train Gradient Boosting"""
        self.gb_model = GradientBoostingClassifier(
            n_estimators=200,
            learning_rate=0.05,
            max_depth=5,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
        self.gb_model.fit(X_train, y_train)
        log_message(f"Gradient Boosting trained - Accuracy: {self.gb_model.score(X_train, y_train):.2%}")
    
    def _train_neural_network(self, X_train: np.ndarray, y_train: np.ndarray):
        """Train Neural Network"""
        self.nn_model = MLPClassifier(
            hidden_layer_sizes=(256, 128, 64),
            activation='relu',
            solver='adam',
            learning_rate='adaptive',
            max_iter=1000,
            early_stopping=True,
            validation_fraction=0.1,
            random_state=42
        )
        self.nn_model.fit(X_train, y_train)
        log_message(f"Neural Network trained - Accuracy: {self.nn_model.score(X_train, y_train):.2%}")
    
    def _train_svm(self, X_train: np.ndarray, y_train: np.ndarray):
        """Train Support Vector Machine"""
        self.svm_model = SVC(
            kernel='rbf',
            C=1.0,
            gamma='scale',
            probability=True,
            random_state=42
        )
        self.svm_model.fit(X_train, y_train)
        log_message(f"SVM trained - Accuracy: {self.svm_model.score(X_train, y_train):.2%}")
    
    def _ensemble_predict(self, X_scaled: np.ndarray) -> Dict:
        """
        Predict using ensemble voting
        التنبؤ باستخدام نظام التصويت
        """
        rf_pred = self.rf_model.predict(X_scaled)[0]
        gb_pred = self.gb_model.predict(X_scaled)[0]
        nn_pred = self.nn_model.predict(X_scaled)[0]
        svm_pred = self.svm_model.predict(X_scaled)[0]
        
        # Get probabilities
        rf_proba = self.rf_model.predict_proba(X_scaled)[0][1]
        gb_proba = self.gb_model.predict_proba(X_scaled)[0][1]
        nn_proba = self.nn_model.predict_proba(X_scaled)[0][1]
        svm_proba = self.svm_model.predict_proba(X_scaled)[0][1]
        
        # Ensemble voting
        votes = rf_pred + gb_pred + nn_pred + svm_pred
        avg_probability = (rf_proba + gb_proba + nn_proba + svm_proba) / 4
        
        signal = 'BUY' if votes >= 2 else 'SELL'
        confidence = max(avg_probability, 1 - avg_probability) * 100
        
        return {
            'signal': signal,
            'confidence': confidence,
            'probability': avg_probability * 100,
            'rf_vote': int(rf_pred),
            'gb_vote': int(gb_pred),
            'nn_vote': int(nn_pred),
            'svm_vote': int(svm_pred),
        }
    
    def _evaluate_models(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict:
        """
        Evaluate all models
        تقييم جميع النماذج
        """
        rf_acc = accuracy_score(y_test, self.rf_model.predict(X_test))
        gb_acc = accuracy_score(y_test, self.gb_model.predict(X_test))
        nn_acc = accuracy_score(y_test, self.nn_model.predict(X_test))
        svm_acc = accuracy_score(y_test, self.svm_model.predict(X_test))
        
        # Ensemble accuracy
        ensemble_pred = []
        for i in range(len(X_test)):
            votes = (self.rf_model.predict([X_test[i]])[0] +
                    self.gb_model.predict([X_test[i]])[0] +
                    self.nn_model.predict([X_test[i]])[0] +
                    self.svm_model.predict([X_test[i]])[0])
            ensemble_pred.append(1 if votes >= 2 else 0)
        
        ensemble_acc = accuracy_score(y_test, ensemble_pred)
        
        return {
            'rf_accuracy': rf_acc,
            'gb_accuracy': gb_acc,
            'nn_accuracy': nn_acc,
            'svm_accuracy': svm_acc,
            'ensemble_accuracy': ensemble_acc,
        }
    
    def _save_models(self):
        """Save trained models"""
        joblib.dump(self.rf_model, self.model_dir / 'rf_model.pkl')
        joblib.dump(self.gb_model, self.model_dir / 'gb_model.pkl')
        joblib.dump(self.nn_model, self.model_dir / 'nn_model.pkl')
        joblib.dump(self.svm_model, self.model_dir / 'svm_model.pkl')
        joblib.dump(self.scaler, self.model_dir / 'scaler.pkl')
        log_message("Models saved successfully")
    
    def load_models(self):
        """Load trained models"""
        try:
            self.rf_model = joblib.load(self.model_dir / 'rf_model.pkl')
            self.gb_model = joblib.load(self.model_dir / 'gb_model.pkl')
            self.nn_model = joblib.load(self.model_dir / 'nn_model.pkl')
            self.svm_model = joblib.load(self.model_dir / 'svm_model.pkl')
            self.scaler = joblib.load(self.model_dir / 'scaler.pkl')
            self.is_trained = True
            log_message("Models loaded successfully")
            return True
        except Exception as e:
            log_message(f"Error loading models: {e}", "ERROR")
            return False
