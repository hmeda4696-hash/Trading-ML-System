#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trading ML System - Main Application
نظام تحليل وتعلم آلي للأزواج الفوركس

Author: hmeda4696-hash
Date: 2026-05-17
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ui.main_window import MainWindow
from utils.config import Config


def main():
    """
    Application entry point
    نقطة الدخول الرئيسية للتطبيق
    """
    # Load configuration
    config = Config()
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Trading ML System")
    app.setApplicationVersion("1.0.0")
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = MainWindow(config)
    window.show()
    
    # Run application
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
