#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration Module
إدارة إعدادات النظام
"""

import os
import json
from pathlib import Path
from typing import Dict, Any


class Config:
    """
    Configuration Manager
    مدير الإعدادات
    """
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent.parent
        self.src_dir = self.base_dir / 'src'
        self.data_dir = self.base_dir / 'data'
        self.output_dir = self.base_dir / 'output'
        self.indicators_dir = self.base_dir / 'mql5_indicators'
        
        # Create directories if they don't exist
        self.data_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        self.indicators_dir.mkdir(exist_ok=True)
        
        # Default configuration
        self.config = {
            'app_name': 'Trading ML System',
            'version': '1.0.0',
            'language': 'ar',  # Arabic
            'theme': 'dark',
            
            # MT5 Settings
            'mt5': {
                'enabled': True,
                'timeout': 5000,
            },
            
            # Analysis Settings
            'analysis': {
                'default_timeframe': 'H1',
                'lookback_periods': 500,
                'min_signals': 3,
            },
            
            # Backtesting Settings
            'backtesting': {
                'default_period': 12,  # months
                'initial_capital': 10000,
                'leverage': 1,
            },
            
            # ML Settings
            'ml': {
                'test_size': 0.2,
                'random_state': 42,
                'n_estimators': 100,
            },
        }
    
    def get(self, key: str, default=None) -> Any:
        """
        Get configuration value
        الحصول على قيمة من الإعدادات
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value
        تعيين قيمة في الإعدادات
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def load_from_file(self, filepath: str) -> bool:
        """
        Load configuration from file
        تحميل الإعدادات من ملف
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.config.update(data)
            return True
        except Exception as e:
            print(f"Error loading config: {e}")
            return False
    
    def save_to_file(self, filepath: str) -> bool:
        """
        Save configuration to file
        حفظ الإعدادات في ملف
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
