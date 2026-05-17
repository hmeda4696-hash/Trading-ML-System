#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Indicator Generator Module
مولد المؤشرات MQL5
"""

import os
from pathlib import Path
from typing import Dict
from utils.config import Config
from utils.helpers import log_message
from datetime import datetime


class IndicatorGenerator:
    """
    Generate MQL5 Indicators
    مولد مؤشرات MQL5
    """
    
    def __init__(self, config: Config):
        self.config = config
        self.indicators_dir = config.indicators_dir
    
    def generate(self, symbol: str, analysis_result: Dict) -> bool:
        """
        Generate MQL5 indicator
        توليد مؤشر MQL5
        """
        try:
            # Generate indicator code
            indicator_code = self._generate_indicator_code(symbol, analysis_result)
            
            # Save to file
            filename = f"AI_SmartIndicator_{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mq5"
            filepath = self.indicators_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(indicator_code)
            
            log_message(f"Indicator generated: {filepath}")
            return True
        
        except Exception as e:
            log_message(f"Error generating indicator: {e}", "ERROR")
            return False
    
    def _generate_indicator_code(self, symbol: str, analysis_result: Dict) -> str:
        """
        Generate MQL5 code
        توليد كود MQL5
        """
        trend = analysis_result.get('trend', {})
        sr = analysis_result.get('support_resistance', {})
        signals = analysis_result.get('signals', [])
        
        code = f'''//+------------------------------------------------------------------+
//|                    AI Smart Trading Indicator                      |
//|                 تحليل ذكي للفوركس - نظام ML                      |
//|                       {datetime.now().strftime('%Y-%m-%d')}                            |
//+------------------------------------------------------------------+
#property copyright "Trading ML System"
#property link      "https://github.com/hmeda4696-hash/Trading-ML-System"
#property version   "1.00"
#property strict
#property indicator_chart_window
#property indicator_buffers 5
#property indicator_plots   3

// Indicator buffers
double TrendBuffer[];
double BuySignalBuffer[];
double SellSignalBuffer[];
double SupportBuffer[];
double ResistanceBuffer[];

int OnInit()
{{
    SetIndexBuffer(0, TrendBuffer, INDICATOR_DATA);
    SetIndexBuffer(1, BuySignalBuffer, INDICATOR_DATA);
    SetIndexBuffer(2, SellSignalBuffer, INDICATOR_DATA);
    SetIndexBuffer(3, SupportBuffer, INDICATOR_DATA);
    SetIndexBuffer(4, ResistanceBuffer, INDICATOR_DATA);
    
    // Set plot properties
    PlotIndexSetInteger(0, PLOT_TYPE, PLOT_LINE);
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, 1);
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 0, clrBlue);
    PlotIndexSetInteger(0, PLOT_LINE_WIDTH, 2);
    
    PlotIndexSetInteger(1, PLOT_TYPE, PLOT_ARROW);
    PlotIndexSetInteger(1, PLOT_ARROW, 233);
    PlotIndexSetInteger(1, PLOT_COLOR_INDEXES, 1);
    PlotIndexSetInteger(1, PLOT_LINE_COLOR, 0, clrGreen);
    
    PlotIndexSetInteger(2, PLOT_TYPE, PLOT_ARROW);
    PlotIndexSetInteger(2, PLOT_ARROW, 234);
    PlotIndexSetInteger(2, PLOT_COLOR_INDEXES, 1);
    PlotIndexSetInteger(2, PLOT_LINE_COLOR, 0, clrRed);
    
    IndicatorSetString(INDICATOR_SHORTNAME, "AI Smart Indicator ({symbol})");
    IndicatorSetInteger(INDICATOR_DIGITS, _Digits);
    
    return(INIT_SUCCEEDED);
}}

int OnCalculate(const int rates_total,
                const int prev_calculated,
                const datetime &time[],
                const double &open[],
                const double &high[],
                const double &low[],
                const double &close[],
                const long &tick_volume[],
                const long &volume[],
                const int &spread[])
{{
    // Current trend: {trend.get('direction', 'NEUTRAL')}
    // Trend strength: {trend.get('strength', 0)}
    // Support: {sr.get('support', 0):.5f}
    // Resistance: {sr.get('resistance', 0):.5f}
    
    for(int i = prev_calculated; i < rates_total; i++)
    {{
        // Set support and resistance levels
        SupportBuffer[i] = {sr.get('support', 0):.5f};
        ResistanceBuffer[i] = {sr.get('resistance', 0):.5f};
        
        // Draw trend line
        if(close[i] > {sr.get('pivot', 0):.5f})
        {{
            TrendBuffer[i] = {sr.get('support', 0):.5f};
        }}
        else
        {{
            TrendBuffer[i] = {sr.get('resistance', 0):.5f};
        }}
'''
        
        # Add signals
        if signals:
            code += "\n        // AI Generated Signals\n"
            for signal in signals[-5:]:  # Last 5 signals
                if signal['type'] == 'BUY':
                    code += f"        BuySignalBuffer[i] = {signal['price']:.5f}; // Confidence: {signal['confidence']:.1f}%\n"
                else:
                    code += f"        SellSignalBuffer[i] = {signal['price']:.5f}; // Confidence: {signal['confidence']:.1f}%\n"
        
        code += """    }
    
    return(rates_total);
}

//+------------------------------------------------------------------+
//| Custom function to display indicator info                        |
//+------------------------------------------------------------------+
void OnChartEvent(const int id, const long &lparam, const double &dparam, const string &sparam)
{
    // Display trend information on chart
    Comment("AI Trading System Active\\n",
            "Trend: """ + f"{trend.get('direction', 'NEUTRAL')}" + "\\n",
            "Price: " + DoubleToString(Close[0], _Digits));
}

//+------------------------------------------------------------------+
"""        
        return code
