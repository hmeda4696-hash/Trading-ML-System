#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dark Theme Loader
محمل المظهر الداكن
"""

from pathlib import Path


def load_stylesheet() -> str:
    """
    Load dark theme stylesheet
    تحميل ورقة أنماط المظهر الداكن
    """
    stylesheet = """
    QWidget {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    
    QMainWindow {
        background-color: #1a1a1a;
    }
    
    QMenuBar {
        background-color: #2b2b2b;
        color: #ffffff;
        border-bottom: 1px solid #3a3a3a;
    }
    
    QMenuBar::item:selected {
        background-color: #0d7377;
    }
    
    QMenu {
        background-color: #2b2b2b;
        color: #ffffff;
        border: 1px solid #3a3a3a;
    }
    
    QMenu::item:selected {
        background-color: #0d7377;
    }
    
    QPushButton {
        background-color: #0d7377;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 8px 16px;
        font-weight: bold;
    }
    
    QPushButton:hover {
        background-color: #14afc1;
    }
    
    QPushButton:pressed {
        background-color: #0a5460;
    }
    
    QLineEdit, QTextEdit, QComboBox {
        background-color: #2b2b2b;
        color: #ffffff;
        border: 1px solid #3a3a3a;
        border-radius: 4px;
        padding: 8px;
        selection-background-color: #0d7377;
    }
    
    QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
        border: 1px solid #14afc1;
        outline: none;
    }
    
    QTableWidget {
        background-color: #1e1e1e;
        gridline-color: #3a3a3a;
        border: none;
    }
    
    QTableWidget::item {
        padding: 8px;
        border: none;
    }
    
    QTableWidget::item:selected {
        background-color: #0d7377;
    }
    
    QHeaderView::section {
        background-color: #2b2b2b;
        color: #ffffff;
        padding: 8px;
        border: none;
        border-right: 1px solid #3a3a3a;
        border-bottom: 1px solid #3a3a3a;
    }
    
    QTabWidget::pane {
        border: none;
    }
    
    QTabBar::tab {
        background-color: #2b2b2b;
        color: #ffffff;
        padding: 8px 20px;
        border: none;
        border-right: 1px solid #3a3a3a;
    }
    
    QTabBar::tab:selected {
        background-color: #0d7377;
    }
    
    QScrollBar:vertical {
        background-color: #2b2b2b;
        width: 12px;
        margin: 0px;
    }
    
    QScrollBar::handle:vertical {
        background-color: #3a3a3a;
        border-radius: 6px;
        min-height: 20px;
    }
    
    QScrollBar::handle:vertical:hover {
        background-color: #0d7377;
    }
    
    QLabel {
        color: #ffffff;
    }
    
    QSpinBox, QDoubleSpinBox {
        background-color: #2b2b2b;
        color: #ffffff;
        border: 1px solid #3a3a3a;
        border-radius: 4px;
        padding: 4px;
    }
    
    QStatusBar {
        background-color: #2b2b2b;
        color: #ffffff;
        border-top: 1px solid #3a3a3a;
    }
    
    QProgressBar {
        background-color: #2b2b2b;
        border: 1px solid #3a3a3a;
        border-radius: 4px;
        text-align: center;
        color: #ffffff;
    }
    
    QProgressBar::chunk {
        background-color: #14afc1;
    }
    """
    return stylesheet
