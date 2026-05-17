#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PainX 800 Advanced Indicator Generator
مولد المؤشرات المتقدمة لـ PainX 800
"""

from pathlib import Path
from typing import Dict
from utils.config import Config
from utils.helpers import log_message
from datetime import datetime


class PainX800IndicatorGenerator:
    """
    Generate advanced MQL5 indicator for PainX 800
    مولد مؤشرات MQL5 متقدمة لـ PainX 800
    """
    
    def __init__(self, config: Config):
        self.config = config
        self.indicators_dir = config.indicators_dir
    
    def generate(self, analysis_result: Dict) -> bool:
        """
        Generate advanced PainX 800 indicator
        توليد مؤشر PainX 800 متقدم
        """
        try:
            indicator_code = self._generate_indicator_code(analysis_result)
            
            filename = f"PainX800_AI_Indicator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mq5"
            filepath = self.indicators_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(indicator_code)
            
            log_message(f"PainX 800 Indicator generated: {filepath}")
            return True
        
        except Exception as e:
            log_message(f"Error generating indicator: {e}", "ERROR")
            return False
    
    def _generate_indicator_code(self, analysis_result: Dict) -> str:
        """
        Generate MQL5 indicator code
        توليد كود MQL5 للمؤشر
        """
        signal = analysis_result.get('signal', 'NEUTRAL')
        confidence = analysis_result.get('confidence', 0)
        
        code = f'''//+------------------------------------------------------------------+
//|              PainX 800 AI Advanced Trading Indicator              |
//|                    نظام تداول ذكي متقدم                          |
//|                      Powered by ML/AI                            |
//+------------------------------------------------------------------+
#property copyright "PainX 800 Trading System"
#property link      "https://github.com/hmeda4696-hash/Trading-ML-System"
#property version   "2.0"
#property strict
#property indicator_chart_window
#property indicator_buffers 8
#property indicator_plots   5

// ==================== INPUT PARAMETERS ====================
input int RsiPeriod = 14;
input int AdxPeriod = 14;
input int MacdFast = 12;
input int MacdSlow = 26;
input int MacdSignal = 9;
input int BollingerPeriod = 20;
input double BollingerDev = 2.0;
input int IchimokuTenkan = 9;
input int IchimokuKijun = 26;
input bool ShowAlerts = true;
input bool ShowClouds = true;

// ==================== INDICATOR BUFFERS ====================
double AISignalBuffer[];
double BuySignalBuffer[];
double SellSignalBuffer[];
double ConfidenceBuffer[];
double SupportBuffer[];
double ResistanceBuffer[];
double TrendBuffer[];
double VolumeBuffer[];

// ==================== GLOBAL VARIABLES ====================
int lastAlertTime = 0;
string lastAlertSignal = "";
color buyColor = clrGreen;
color sellColor = clrRed;
color neutralColor = clrYellow;

// ==================== INITIALIZATION ====================
int OnInit()
{{
    // Set indicator buffers
    SetIndexBuffer(0, AISignalBuffer, INDICATOR_DATA);
    SetIndexBuffer(1, BuySignalBuffer, INDICATOR_DATA);
    SetIndexBuffer(2, SellSignalBuffer, INDICATOR_DATA);
    SetIndexBuffer(3, ConfidenceBuffer, INDICATOR_DATA);
    SetIndexBuffer(4, SupportBuffer, INDICATOR_DATA);
    SetIndexBuffer(5, ResistanceBuffer, INDICATOR_DATA);
    SetIndexBuffer(6, TrendBuffer, INDICATOR_DATA);
    SetIndexBuffer(7, VolumeBuffer, INDICATOR_DATA);
    
    // Configure BUY signals plot
    PlotIndexSetInteger(1, PLOT_TYPE, PLOT_ARROW);
    PlotIndexSetInteger(1, PLOT_ARROW, 233);
    PlotIndexSetInteger(1, PLOT_COLOR_INDEXES, 1);
    PlotIndexSetInteger(1, PLOT_LINE_COLOR, 0, buyColor);
    PlotIndexSetInteger(1, PLOT_LINE_WIDTH, 3);
    PlotIndexSetString(1, PLOT_LABEL, "AI BUY Signal");
    
    // Configure SELL signals plot
    PlotIndexSetInteger(2, PLOT_TYPE, PLOT_ARROW);
    PlotIndexSetInteger(2, PLOT_ARROW, 234);
    PlotIndexSetInteger(2, PLOT_COLOR_INDEXES, 1);
    PlotIndexSetInteger(2, PLOT_LINE_COLOR, 0, sellColor);
    PlotIndexSetInteger(2, PLOT_LINE_WIDTH, 3);
    PlotIndexSetString(2, PLOT_LABEL, "AI SELL Signal");
    
    // Configure Support/Resistance
    PlotIndexSetInteger(4, PLOT_TYPE, PLOT_LINE);
    PlotIndexSetInteger(4, PLOT_COLOR_INDEXES, 1);
    PlotIndexSetInteger(4, PLOT_LINE_COLOR, 0, clrBlue);
    PlotIndexSetInteger(4, PLOT_LINE_WIDTH, 1);
    PlotIndexSetString(4, PLOT_LABEL, "Support");
    
    PlotIndexSetInteger(5, PLOT_TYPE, PLOT_LINE);
    PlotIndexSetInteger(5, PLOT_COLOR_INDEXES, 1);
    PlotIndexSetInteger(5, PLOT_LINE_COLOR, 0, clrMagenta);
    PlotIndexSetInteger(5, PLOT_LINE_WIDTH, 1);
    PlotIndexSetString(5, PLOT_LABEL, "Resistance");
    
    // Configure Trend
    PlotIndexSetInteger(6, PLOT_TYPE, PLOT_LINE);
    PlotIndexSetInteger(6, PLOT_COLOR_INDEXES, 2);
    PlotIndexSetInteger(6, PLOT_LINE_COLOR, 0, buyColor);
    PlotIndexSetInteger(6, PLOT_LINE_COLOR, 1, sellColor);
    PlotIndexSetInteger(6, PLOT_LINE_WIDTH, 2);
    PlotIndexSetString(6, PLOT_LABEL, "Trend");
    
    IndicatorSetString(INDICATOR_SHORTNAME, "PainX 800 AI Indicator v2.0");
    IndicatorSetInteger(INDICATOR_DIGITS, _Digits);
    
    return(INIT_SUCCEEDED);
}}

// ==================== MAIN CALCULATION ====================
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
    if(rates_total < 100) return 0;
    
    int start = prev_calculated > 0 ? prev_calculated - 1 : 0;
    
    for(int i = start; i < rates_total; i++)
    {{
        // Calculate RSI
        double rsi = iRSI(Symbol(), PERIOD_CURRENT, RsiPeriod, PRICE_CLOSE, i);
        
        // Calculate MACD
        double macd = iMACD(Symbol(), PERIOD_CURRENT, MacdFast, MacdSlow, MacdSignal, PRICE_CLOSE, MODE_MAIN, i);
        double macdsignal = iMACD(Symbol(), PERIOD_CURRENT, MacdFast, MacdSlow, MacdSignal, PRICE_CLOSE, MODE_SIGNAL, i);
        
        // Calculate ADX
        double adx = iADX(Symbol(), PERIOD_CURRENT, AdxPeriod, MODE_MAIN, i);
        double plusdi = iADX(Symbol(), PERIOD_CURRENT, AdxPeriod, MODE_PLUSDI, i);
        double minusdi = iADX(Symbol(), PERIOD_CURRENT, AdxPeriod, MODE_MINUSDI, i);
        
        // Calculate Bollinger Bands
        double bbUpper = iBands(Symbol(), PERIOD_CURRENT, BollingerPeriod, BollingerDev, 0, PRICE_CLOSE, MODE_UPPER, i);
        double bbLower = iBands(Symbol(), PERIOD_CURRENT, BollingerPeriod, BollingerDev, 0, PRICE_CLOSE, MODE_LOWER, i);
        double bbMiddle = iBands(Symbol(), PERIOD_CURRENT, BollingerPeriod, BollingerDev, 0, PRICE_CLOSE, MODE_MAIN, i);
        
        // Calculate Moving Averages
        double ma20 = iMA(Symbol(), PERIOD_CURRENT, 20, 0, MODE_SMA, PRICE_CLOSE, i);
        double ma50 = iMA(Symbol(), PERIOD_CURRENT, 50, 0, MODE_SMA, PRICE_CLOSE, i);
        double ma200 = iMA(Symbol(), PERIOD_CURRENT, 200, 0, MODE_SMA, PRICE_CLOSE, i);
        
        // AI Signal Generation
        // Based on model prediction: {signal}
        // Confidence Level: {confidence:.1f}%
        
        double confidence = {confidence:.1f};
        string currentSignal = "{signal}";
        
        // Initialize values
        AISignalBuffer[i] = close[i];
        ConfidenceBuffer[i] = confidence;
        SupportBuffer[i] = bbLower;
        ResistanceBuffer[i] = bbUpper;
        TrendBuffer[i] = ma50;
        VolumeBuffer[i] = (double)volume[i];
        
        // Generate Buy Signals
        bool buySignal = false;
        if(StringCompare(currentSignal, "BUY", false) == 0 && confidence >= 70)
        {{
            if(rsi < 70 && macd > macdsignal && close[i] > ma20)
            {{
                buySignal = true;
                BuySignalBuffer[i] = low[i] - (high[i] - low[i]) * 0.5;
            }}
        }}
        
        // Generate Sell Signals
        bool sellSignal = false;
        if(StringCompare(currentSignal, "SELL", false) == 0 && confidence >= 70)
        {{
            if(rsi > 30 && macd < macdsignal && close[i] < ma20)
            {{
                sellSignal = true;
                SellSignalBuffer[i] = high[i] + (high[i] - low[i]) * 0.5;
            }}
        }}
        
        // Generate Alerts
        if(ShowAlerts && (buySignal || sellSignal))
        {{
            if(time[i] != lastAlertTime)
            {{
                string alertText = StringCompare(currentSignal, "BUY", false) == 0 ? 
                    "🚀 BUY SIGNAL - Confidence: " + DoubleToString(confidence, 1) + "%" :
                    "⛔ SELL SIGNAL - Confidence: " + DoubleToString(confidence, 1) + "%";
                
                Alert("PainX 800 AI Indicator: " + alertText);
                SendNotification("PainX 800 Alert: " + alertText);
                
                lastAlertTime = time[i];
                lastAlertSignal = currentSignal;
            }}
        }}
    }}
    
    return(rates_total);
}}

// ==================== DEINIT ====================
void OnDeinit(const int reason)
{{
    ObjectsDeleteAll(0, "PainX800_");
}}

// ==================== CUSTOM FUNCTIONS ====================
void DrawTrendCloud(int index, bool isBullish, double upper, double lower)
{{
    if(!ShowClouds) return;
    
    color cloudColor = isBullish ? clrGreen : clrRed;
    // Cloud drawing logic here
}}

string GetSignalDescription(string signal, double confidence)
{{
    if(confidence >= 85) return signal + " - VERY STRONG";
    if(confidence >= 75) return signal + " - STRONG";
    if(confidence >= 65) return signal + " - MODERATE";
    return signal + " - WEAK";
}}
//+------------------------------------------------------------------+
'''
        return code
