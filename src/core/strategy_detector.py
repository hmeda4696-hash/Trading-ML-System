#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Strategy Detector Module
كاشف الستراتيجية
"""

import numpy as np
import pandas as pd
from typing import Dict
from utils.config import Config
from utils.helpers import log_message


class StrategyDetector:
    """
    Detect optimal strategy for pair
    كشف الستراتيجية المثلى للزوج
    """
    
    def __init__(self, config: Config):
        self.config = config
    
    def detect(self, symbol: str, analysis_result: Dict) -> Dict:
        """
        Detect optimal strategy
        كشف الستراتيجية المثلى
        """
        trend = analysis_result.get('trend', {})
        signals = analysis_result.get('signals', [])
        
        # Analyze characteristics
        volatility = self._analyze_volatility(analysis_result)
        momentum = self._analyze_momentum(analysis_result)
        mean_reversion = self._analyze_mean_reversion(analysis_result)
        breakout = self._analyze_breakout(analysis_result)
        
        # Score each strategy
        scores = {
            'trend_following': self._score_trend_following(trend, volatility, momentum),
            'mean_reversion': mean_reversion,
            'breakout': breakout,
            'scalping': self._score_scalping(volatility),
        }
        
        # Find best strategy
        best_strategy = max(scores, key=scores.get)
        
        return {
            'symbol': symbol,
            'best_strategy': best_strategy,
            'scores': scores,
            'characteristics': {
                'volatility': volatility,
                'momentum': momentum,
            },
            'recommendation': self._get_recommendation(best_strategy, scores),
        }
    
    def _analyze_volatility(self, analysis_result: Dict) -> float:
        """
        Analyze volatility
        تحليل التقلبات
        """
        # Based on ATR and Bollinger Bands width
        return 0.5  # Placeholder
    
    def _analyze_momentum(self, analysis_result: Dict) -> float:
        """
        Analyze momentum
        تحليل الزخم
        """
        # Based on RSI, MACD, ADX
        return 0.5  # Placeholder
    
    def _analyze_mean_reversion(self, analysis_result: Dict) -> float:
        """
        Analyze mean reversion
        تحليل العودة للمتوسط
        """
        return 0.4
    
    def _analyze_breakout(self, analysis_result: Dict) -> float:
        """
        Analyze breakout potential
        تحليل احتمالية الكسر
        """
        return 0.3
    
    def _score_trend_following(self, trend: Dict, volatility: float, momentum: float) -> float:
        """
        Score trend following strategy
        تقييم استراتيجية تتبع الاتجاه
        """
        strength = abs(trend.get('strength', 0))
        if strength > 0:
            return (strength / 3.0) * 100
        return 0
    
    def _score_scalping(self, volatility: float) -> float:
        """
        Score scalping strategy
        تقييم استراتيجية المضاربة
        """
        if volatility < 0.3:
            return 70
        return 30
    
    def _get_recommendation(self, strategy: str, scores: Dict) -> str:
        """
        Get strategy recommendation
        الحصول على توصية الستراتيجية
        """
        recommendations = {
            'trend_following': 'استخدم استراتيجية تتبع الاتجاه - اتبع الاتجاه الحالي',
            'mean_reversion': 'استخدم استراتيجية العودة للمتوسط - اشتر عند الارتفاع الزائد',
            'breakout': 'استخدم استراتيجية الكسر - انتظر كسر المستويات المهمة',
            'scalping': 'استخدم المضاربة - افتح صفقات سريعة قصيرة المدى',
        }
        return recommendations.get(strategy, 'استراتيجية محايدة')
