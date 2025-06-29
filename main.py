#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sentimemory - AI聊天工具主程序
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ui.main_window import MainWindow
from config.settings import AppSettings


def main():
    """主函数"""
    # 在创建QApplication之前设置高DPI属性
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # 创建应用程序
    app = QApplication(sys.argv)
    app.setApplicationName("Sentimemory")
    app.setApplicationVersion("1.0.0")
    
    # 加载应用设置
    settings = AppSettings()
    
    # 创建主窗口
    main_window = MainWindow()
    main_window.show()
    
    # 运行应用程序
    sys.exit(app.exec_())


if __name__ == "__main__":
    main() 