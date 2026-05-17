#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Window UI
النافذة الرئيسية للتطبيق
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QStatusBar, QProgressBar
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt5.QtGui import QIcon, QFont
from pathlib import Path

from ui.widgets.pair_panel import PairPanel
from ui.widgets.analysis_panel import AnalysisPanel
from ui.widgets.results_panel import ResultsPanel
from ui.styles.dark_theme import load_stylesheet
from utils.config import Config


class MainWindow(QMainWindow):
    """
    Main Application Window
    النافذة الرئيسية للتطبيق
    """
    
    def __init__(self, config: Config):
        super().__init__()
        self.config = config
        self.setWindowTitle(f"{config.get('app_name')} v{config.get('version')}")
        self.setGeometry(100, 100, 1400, 900)
        
        # Load dark theme
        self.setStyleSheet(load_stylesheet())
        
        # Initialize UI
        self.init_ui()
        
    def init_ui(self):
        """
        Initialize user interface
        تهيئة واجهة المستخدم
        """
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("🤖 Trading ML System")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        main_layout.addLayout(header_layout)
        
        # Tab Widget
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabBar::tab {
                background-color: #2b2b2b;
                color: #ffffff;
                padding: 8px 20px;
                border: none;
                border-bottom: 2px solid #2b2b2b;
            }
            QTabBar::tab:selected {
                background-color: #0d7377;
                border-bottom: 2px solid #14afc1;
            }
            QTabBar::tab:hover:!selected {
                background-color: #3a3a3a;
            }
        """)
        
        # Create panels
        self.pair_panel = PairPanel(self.config)
        self.analysis_panel = AnalysisPanel(self.config)
        self.results_panel = ResultsPanel(self.config)
        
        # Add tabs
        tabs.addTab(self.pair_panel, "📊 الأزواج")
        tabs.addTab(self.analysis_panel, "🔍 التحليل")
        tabs.addTab(self.results_panel, "📈 النتائج")
        
        main_layout.addWidget(tabs)
        
        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("جاهز | Ready")
        
        # Progress bar in status bar
        self.progress = QProgressBar()
        self.progress.setMaximumWidth(300)
        self.progress.setVisible(False)
        self.statusBar.addPermanentWidget(self.progress)
        
        central_widget.setLayout(main_layout)
        
        # Connect signals
        self.connect_signals()
    
    def connect_signals(self):
        """
        Connect signals between panels
        ربط الإشارات بين اللوحات
        """
        # Connect pair panel to analysis panel
        self.pair_panel.pair_selected.connect(self.on_pair_selected)
        
        # Connect analysis panel to results panel
        self.analysis_panel.analysis_completed.connect(self.on_analysis_completed)
        self.analysis_panel.progress_updated.connect(self.update_progress)
    
    def on_pair_selected(self, pair_info: dict):
        """
        Handle pair selection
        معالجة اختيار الزوج
        """
        self.analysis_panel.set_pair(pair_info)
        self.statusBar.showMessage(f"تم اختيار الزوج: {pair_info.get('symbol')}")
    
    def on_analysis_completed(self, results: dict):
        """
        Handle analysis completion
        معالجة انتهاء التحليل
        """
        self.results_panel.display_results(results)
        self.statusBar.showMessage("✅ اكتمل التحليل بنجاح")
        self.progress.setVisible(False)
    
    def update_progress(self, value: int):
        """
        Update progress bar
        تحديث شريط التقدم
        """
        self.progress.setVisible(True)
        self.progress.setValue(value)
        if value >= 100:
            self.progress.setVisible(False)
    
    def closeEvent(self, event):
        """
        Handle window close event
        معالجة إغلاق النافذة
        """
        event.accept()
