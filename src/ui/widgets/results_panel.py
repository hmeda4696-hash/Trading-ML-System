#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Results Display Panel
لوحة عرض النتائج
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QPushButton, QTabWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from utils.config import Config


class ResultsPanel(QWidget):
    """
    Results Display Panel
    لوحة عرض النتائج
    """
    
    def __init__(self, config: Config):
        super().__init__()
        self.config = config
        self.init_ui()
    
    def init_ui(self):
        """
        Initialize UI
        تهيئة الواجهة
        """
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Title
        title = QLabel("النتائج والإحصائيات")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Create tabs for different result views
        tabs = QTabWidget()
        
        # Statistics tab
        self.stats_table = QTableWidget()
        self.stats_table.setColumnCount(2)
        self.stats_table.setHorizontalHeaderLabels(['المؤشر', 'القيمة'])
        self.stats_table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e1e;
                gridline-color: #3a3a3a;
                color: #ffffff;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #2b2b2b;
                color: #ffffff;
                padding: 8px;
                border: none;
                border-bottom: 1px solid #3a3a3a;
            }
        """)
        tabs.addTab(self.stats_table, "📊 الإحصائيات")
        
        # Signals tab
        self.signals_table = QTableWidget()
        self.signals_table.setColumnCount(4)
        self.signals_table.setHorizontalHeaderLabels(['الوقت', 'نوع الإشارة', 'السعر', 'الثقة'])
        self.signals_table.setStyleSheet(self.stats_table.styleSheet())
        tabs.addTab(self.signals_table, "🔔 الإشارات")
        
        layout.addWidget(tabs)
        
        # Export button
        button_layout = QHBoxLayout()
        export_btn = QPushButton("💾 تصدير النتائج")
        export_btn.setMaximumWidth(150)
        export_btn.setStyleSheet("""
            QPushButton {
                background-color: #14afc1;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0d7377;
            }
        """)
        button_layout.addWidget(export_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def display_results(self, results: dict):
        """
        Display analysis results
        عرض نتائج التحليل
        """
        # Clear previous results
        self.stats_table.setRowCount(0)
        self.signals_table.setRowCount(0)
        
        if 'backtest' not in results:
            return
        
        bt = results['backtest']
        
        # Display statistics
        stats = [
            ('الربح الإجمالي', f"{bt.get('total_profit', 0):.2f} $"),
            ('معدل النجاح', f"{bt.get('win_rate', 0):.1f}%"),
            ('عدد الصفقات', str(bt.get('total_trades', 0))),
            ('الصفقات الرابحة', str(bt.get('winning_trades', 0))),
            ('الصفقات الخاسرة', str(bt.get('losing_trades', 0))),
            ('نسبة الربح للخسارة', f"{bt.get('profit_factor', 0):.2f}"),
            ('أكبر خسارة متتالية', str(bt.get('max_drawdown', 0))),
        ]
        
        for i, (label, value) in enumerate(stats):
            self.stats_table.insertRow(i)
            
            label_item = QTableWidgetItem(label)
            label_item.setFont(QFont('Arial', 10, QFont.Bold))
            self.stats_table.setItem(i, 0, label_item)
            
            value_item = QTableWidgetItem(value)
            if 'profit' in label.lower() or '%' in value:
                value_item.setForeground(QColor(76, 175, 80))  # Green
            value_item.setFont(QFont('Arial', 10))
            self.stats_table.setItem(i, 1, value_item)
        
        # Display signals if available
        if 'signals' in results:
            signals = results['signals']
            for i, signal in enumerate(signals[:50]):  # Show last 50 signals
                self.signals_table.insertRow(i)
                
                self.signals_table.setItem(i, 0, QTableWidgetItem(signal.get('time', 'N/A')))
                
                signal_type = signal.get('type', 'UNKNOWN')
                signal_item = QTableWidgetItem(signal_type)
                color = QColor(76, 175, 80) if signal_type == 'BUY' else QColor(244, 67, 54)
                signal_item.setForeground(color)
                self.signals_table.setItem(i, 1, signal_item)
                
                self.signals_table.setItem(i, 2, QTableWidgetItem(f"{signal.get('price', 0):.5f}"))
                
                confidence = QTableWidgetItem(f"{signal.get('confidence', 0):.1f}%")
                self.signals_table.setItem(i, 3, confidence)
