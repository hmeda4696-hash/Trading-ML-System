#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helper Functions Module
دوال مساعدة
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any
import pandas as pd
import numpy as np


def log_message(message: str, level: str = 'INFO') -> None:
    """
    Log a message with timestamp
    تسجيل رسالة مع الوقت
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] [{level}] {message}")


def save_json(data: Dict[str, Any], filepath: str) -> bool:
    """
    Save data to JSON file
    حفظ البيانات في ملف JSON
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        log_message(f"Data saved to {filepath}")
        return True
    except Exception as e:
        log_message(f"Error saving JSON: {e}", 'ERROR')
        return False


def load_json(filepath: str) -> Dict[str, Any]:
    """
    Load data from JSON file
    تحميل البيانات من ملف JSON
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        log_message(f"Error loading JSON: {e}", 'ERROR')
        return {}


def format_number(value: float, decimals: int = 2) -> str:
    """
    Format number with decimals
    تنسيق رقم برقم عشري
    """
    return f"{value:,.{decimals}f}"


def calculate_statistics(data: np.ndarray) -> Dict[str, float]:
    """
    Calculate statistics for array
    حساب الإحصائيات
    """
    return {
        'mean': float(np.mean(data)),
        'median': float(np.median(data)),
        'std': float(np.std(data)),
        'min': float(np.min(data)),
        'max': float(np.max(data)),
    }


def normalize_data(data: np.ndarray) -> np.ndarray:
    """
    Normalize data to [0, 1]
    تطبيع البيانات
    """
    min_val = np.min(data)
    max_val = np.max(data)
    return (data - min_val) / (max_val - min_val + 1e-8)


def get_timeframe_minutes(timeframe: str) -> int:
    """
    Convert timeframe string to minutes
    تحويل الإطار الزمني إلى دقائق
    """
    timeframe_map = {
        'M1': 1,
        'M5': 5,
        'M15': 15,
        'M30': 30,
        'H1': 60,
        'H4': 240,
        'D1': 1440,
        'W1': 10080,
        'MN1': 43200,
    }
    return timeframe_map.get(timeframe, 60)
