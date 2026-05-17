#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pair Management Panel
لوحة إدارة الأزواج
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QHeaderView
)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QColor
from utils.config import Config


class PairPanel(QWidget):
    """
    Pair Management Panel
    لوحة إدارة الأزواج
    """
    
    # Signals
    pair_selected = pyqtSignal(dict)
    
    def __init__(self, config: Config):
        super().__init__()
        self.config = config
        self.pairs = []
        self.init_ui()
    
    def init_ui(self):
        """
        Initialize UI
        تهيئة الواجهة
        """
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Title
        title = QLabel("إدارة الأزواج")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Input section
        input_layout = QHBoxLayout()
        
        # Symbol input
        input_layout.addWidget(QLabel("رمز الزوج:"))
        self.symbol_input = QLineEdit()
        self.symbol_input.setPlaceholderText("EURUSD, GBPUSD, ...")
        self.symbol_input.setMaximumWidth(150)
        input_layout.addWidget(self.symbol_input)
        
        # Timeframe selection
        input_layout.addWidget(QLabel("الإطار الزمني:"))
        self.timeframe_combo = QComboBox()
        self.timeframe_combo.addItems(['M5', 'M15', 'M30', 'H1', 'H4', 'D1'])
        self.timeframe_combo.setMaximumWidth(100)
        input_layout.addWidget(self.timeframe_combo)
        
        # Add button
        add_btn = QPushButton("➕ إضافة الزوج")
        add_btn.setMaximumWidth(150)
        add_btn.clicked.connect(self.add_pair)
        add_btn.setStyleSheet("""
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
        input_layout.addWidget(add_btn)
        input_layout.addStretch()
        
        layout.addLayout(input_layout)
        
        # Pairs table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['الزوج', 'الإطار الزمني', 'الحالة', 'الإجراء'])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e1e;
                gridline-color: #3a3a3a;
                color: #ffffff;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #2b2b2b;
                color: #ffffff;
                padding: 5px;
                border: none;
                border-bottom: 1px solid #3a3a3a;
            }
        """)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def add_pair(self):
        """
        Add new pair
        إضافة زوج جديد
        """
        symbol = self.symbol_input.text().strip().upper()
        timeframe = self.timeframe_combo.currentText()
        
        if not symbol:
            QMessageBox.warning(self, "تنبيه", "الرجاء إدخال رمز الزوج")
            return
        
        # Check if pair already exists
        for pair in self.pairs:
            if pair['symbol'] == symbol and pair['timeframe'] == timeframe:
                QMessageBox.warning(self, "تنبيه", "هذا الزوج موجود بالفعل")
                return
        
        # Add pair
        pair_info = {
            'symbol': symbol,
            'timeframe': timeframe,
            'status': '⏳ انتظار'
        }
        self.pairs.append(pair_info)
        
        # Update table
        self.update_table()
        
        # Clear inputs
        self.symbol_input.clear()
        
        # Emit signal
        self.pair_selected.emit(pair_info)
    
    def update_table(self):
        """
        Update pairs table
        تحديث جدول الأزواج
        """
        self.table.setRowCount(len(self.pairs))
        
        for row, pair in enumerate(self.pairs):
            # Symbol
            symbol_item = QTableWidgetItem(pair['symbol'])
            symbol_item.setForeground(QColor(20, 175, 193))
            self.table.setItem(row, 0, symbol_item)
            
            # Timeframe
            tf_item = QTableWidgetItem(pair['timeframe'])
            self.table.setItem(row, 1, tf_item)
            
            # Status
            status_item = QTableWidgetItem(pair['status'])
            self.table.setItem(row, 2, status_item)
            
            # Action button
            delete_btn = QPushButton("🗑️ حذف")
            delete_btn.clicked.connect(lambda checked, r=row: self.remove_pair(r))
            delete_btn.setMaximumWidth(80)
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #c44536;
                    color: white;
                    border: none;
                    border-radius: 3px;
                    padding: 4px;
                }
                QPushButton:hover {
                    background-color: #a3372f;
                }
            """)
            self.table.setCellWidget(row, 3, delete_btn)
    
    def remove_pair(self, row: int):
        """
        Remove pair
        حذف زوج
        """
        if 0 <= row < len(self.pairs):
            self.pairs.pop(row)
            self.update_table()
    
    def set_pair_status(self, symbol: str, status: str):
        """
        Update pair status
        تحديث حالة الزوج
        """
        for pair in self.pairs:
            if pair['symbol'] == symbol:
                pair['status'] = status
        self.update_table()
