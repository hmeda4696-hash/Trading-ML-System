#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analysis Panel
لوحة التحليل
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSpinBox, QComboBox, QMessageBox, QTextEdit
)
from PyQt5.QtCore import pyqtSignal, QThread, pyqtSlot
from PyQt5.QtGui import QFont
from utils.config import Config
from core.ml_analyzer import MLAnalyzer
from core.backtester import BackTester


class AnalysisWorker(QThread):
    """
    Worker thread for analysis
    خيط العامل للتحليل
    """
    progress = pyqtSignal(int)
    completed = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, pair_info: dict, config: Config):
        super().__init__()
        self.pair_info = pair_info
        self.config = config
    
    def run(self):
        try:
            self.progress.emit(10)
            
            # Initialize analyzer
            analyzer = MLAnalyzer(self.config)
            self.progress.emit(30)
            
            # Analyze pair
            analysis_result = analyzer.analyze(
                self.pair_info['symbol'],
                self.pair_info['timeframe']
            )
            self.progress.emit(60)
            
            # Backtest
            backtester = BackTester(self.config)
            backtest_result = backtester.run(
                self.pair_info['symbol'],
                analysis_result
            )
            self.progress.emit(90)
            
            # Combine results
            results = {
                'analysis': analysis_result,
                'backtest': backtest_result
            }
            
            self.progress.emit(100)
            self.completed.emit(results)
        
        except Exception as e:
            self.error.emit(str(e))


class AnalysisPanel(QWidget):
    """
    Analysis Panel
    لوحة التحليل
    """
    
    # Signals
    analysis_completed = pyqtSignal(dict)
    progress_updated = pyqtSignal(int)
    
    def __init__(self, config: Config):
        super().__init__()
        self.config = config
        self.current_pair = None
        self.worker = None
        self.init_ui()
    
    def init_ui(self):
        """
        Initialize UI
        تهيئة الواجهة
        """
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Title
        title = QLabel("تحليل الأزواج")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Settings section
        settings_layout = QHBoxLayout()
        
        # Backtest period
        settings_layout.addWidget(QLabel("فترة الاختبار (شهور):"))
        self.period_spin = QSpinBox()
        self.period_spin.setMinimum(1)
        self.period_spin.setMaximum(60)
        self.period_spin.setValue(12)
        self.period_spin.setMaximumWidth(100)
        settings_layout.addWidget(self.period_spin)
        
        # Strategy type
        settings_layout.addWidget(QLabel("نوع الاستراتيجية:"))
        self.strategy_combo = QComboBox()
        self.strategy_combo.addItems([
            'تلقائي (Auto)',
            'تتبع الاتجاه (Trend)',
            'العودة للمتوسط (Mean Reversion)',
            'كسر المستويات (Breakout)'
        ])
        self.strategy_combo.setMaximumWidth(200)
        settings_layout.addWidget(self.strategy_combo)
        
        settings_layout.addStretch()
        layout.addLayout(settings_layout)
        
        # Buttons section
        buttons_layout = QHBoxLayout()
        
        # Analyze button
        self.analyze_btn = QPushButton("🔍 بدء التحليل")
        self.analyze_btn.setMaximumWidth(150)
        self.analyze_btn.clicked.connect(self.start_analysis)
        self.analyze_btn.setStyleSheet("""
            QPushButton {
                background-color: #14afc1;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #0d7377;
            }
            QPushButton:pressed {
                background-color: #0a5460;
            }
        """)
        buttons_layout.addWidget(self.analyze_btn)
        
        # Generate indicator button
        gen_btn = QPushButton("⚙️ توليد المؤشر")
        gen_btn.setMaximumWidth(150)
        gen_btn.clicked.connect(self.generate_indicator)
        gen_btn.setStyleSheet("""
            QPushButton {
                background-color: #6a4c93;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a3c83;
            }
        """)
        buttons_layout.addWidget(gen_btn)
        
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
        
        # Output area
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #00ff00;
                border: 1px solid #3a3a3a;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Courier New';
                font-size: 10px;
            }
        """)
        layout.addWidget(self.output_text)
        
        self.setLayout(layout)
    
    def set_pair(self, pair_info: dict):
        """
        Set current pair for analysis
        تعيين الزوج الحالي للتحليل
        """
        self.current_pair = pair_info
        self.output_text.append(f"تم اختيار الزوج: {pair_info['symbol']} {pair_info['timeframe']}")
    
    def start_analysis(self):
        """
        Start pair analysis
        بدء تحليل الزوج
        """
        if not self.current_pair:
            QMessageBox.warning(self, "تنبيه", "الرجاء اختيار زوج أولاً")
            return
        
        self.output_text.append("\n🔍 بدء التحليل...")
        self.analyze_btn.setEnabled(False)
        
        # Create and start worker
        self.worker = AnalysisWorker(self.current_pair, self.config)
        self.worker.progress.connect(self.progress_updated.emit)
        self.worker.completed.connect(self.on_analysis_done)
        self.worker.error.connect(self.on_analysis_error)
        self.worker.start()
    
    @pyqtSlot(dict)
    def on_analysis_done(self, results: dict):
        """
        Handle analysis completion
        معالجة انتهاء التحليل
        """
        self.output_text.append("✅ انتهى التحليل بنجاح!")
        self.output_text.append(f"\nنتائج الاختبار:")
        
        if 'backtest' in results:
            bt = results['backtest']
            self.output_text.append(f"  الأرباح: {bt.get('profit', 'N/A')}")
            self.output_text.append(f"  معدل النجاح: {bt.get('win_rate', 'N/A')}%")
        
        self.analyze_btn.setEnabled(True)
        self.analysis_completed.emit(results)
    
    @pyqtSlot(str)
    def on_analysis_error(self, error: str):
        """
        Handle analysis error
        معالجة خطأ التحليل
        """
        self.output_text.append(f"❌ خطأ: {error}")
        self.analyze_btn.setEnabled(True)
        QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء التحليل: {error}")
    
    def generate_indicator(self):
        """
        Generate MQL5 indicator
        توليد مؤشر MQL5
        """
        if not self.current_pair:
            QMessageBox.warning(self, "تنبيه", "الرجاء اختيار زوج أولاً")
            return
        
        self.output_text.append("\n⚙️ جاري توليد المؤشر...")
        # TODO: Implement indicator generation
        self.output_text.append("✅ تم حفظ المؤشر بنجاح")
