# -*- coding: utf-8 -*-
"""
主窗口界面
"""

import sys
import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QSplitter, QTabWidget, QMenuBar, QMenu, QAction,
                             QStatusBar, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QFont
import platform

# 添加src目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..')
sys.path.insert(0, src_dir)

from ai.chat_engine import ChatEngine
from .chat_widget import ChatWidget
from .personality_widget import PersonalityWidget
from .memory_widget import MemoryWidget
from config.settings import AppSettings


class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self):
        super().__init__()
        self.chat_engine = ChatEngine()
        self.settings = AppSettings()
        self.is_dark_theme = self.settings.get('ui.theme', 'light') == 'dark'
        self.init_ui()
        self.setup_connections()
    
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("Sentimemory - AI聊天工具")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(800, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # 创建左侧面板（人格选择和记忆管理）
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # 创建右侧聊天区域
        self.chat_widget = ChatWidget(self.chat_engine)
        # 立即设置主题
        self.chat_widget.set_theme(self.is_dark_theme)
        splitter.addWidget(self.chat_widget)
        
        # 设置分割器比例
        splitter.setSizes([300, 900])
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        
        # 设置左边栏的固定宽度范围
        left_panel.setMinimumWidth(280)
        left_panel.setMaximumWidth(350)
        
        # 设置分割器不允许折叠左边栏
        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建状态栏
        self.create_status_bar()
        
        # 设置样式
        self.set_style()
    
    def create_left_panel(self) -> QWidget:
        """创建左侧面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建标签页
        tab_widget = QTabWidget()
        
        # 人格选择标签页
        self.personality_widget = PersonalityWidget(self.chat_engine)
        # 立即设置主题
        self.personality_widget.set_theme(self.is_dark_theme)
        tab_widget.addTab(self.personality_widget, "人格选择")
        
        # 记忆管理标签页
        self.memory_widget = MemoryWidget(self.chat_engine)
        # 立即设置主题
        self.memory_widget.set_theme(self.is_dark_theme)
        tab_widget.addTab(self.memory_widget, "记忆管理")
        
        layout.addWidget(tab_widget)
        
        return panel
    
    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu('文件(&F)')
        
        # 新建对话
        new_chat_action = QAction('新建对话(&N)', self)
        new_chat_action.setShortcut('Ctrl+N')
        new_chat_action.triggered.connect(self.new_chat)
        file_menu.addAction(new_chat_action)
        
        file_menu.addSeparator()
        
        # 退出
        exit_action = QAction('退出(&X)', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 编辑菜单
        edit_menu = menubar.addMenu('编辑(&E)')
        
        # 清空聊天记录
        clear_action = QAction('清空聊天记录(&C)', self)
        clear_action.triggered.connect(self.clear_chat)
        edit_menu.addAction(clear_action)
        
        # 视图菜单
        view_menu = menubar.addMenu('视图(&V)')
        
        # 切换主题
        theme_action = QAction('切换主题(&T)', self)
        theme_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(theme_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu('帮助(&H)')
        
        # 关于
        about_action = QAction('关于(&A)', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_status_bar(self):
        """创建状态栏"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # 显示当前人格
        self.update_status_bar()
    
    def set_style(self):
        """设置样式"""
        # 设置全局字体 - 使用跨平台兼容的字体
        if platform.system() == "Darwin":  # macOS
            font = QFont("PingFang SC", 10)  # macOS中文字体
        elif platform.system() == "Windows":
            font = QFont("Microsoft YaHei", 10)  # Windows中文字体
        else:  # Linux
            font = QFont("Noto Sans CJK SC", 10)  # Linux中文字体
        
        # 如果指定字体不存在，使用系统默认字体
        if not font.exactMatch():
            font = QFont()  # 使用系统默认字体
            font.setPointSize(10)
        
        self.setFont(font)
        
        # 根据主题设置样式表
        if self.is_dark_theme:
            self.set_dark_theme()
        else:
            self.set_light_theme()
    
    def set_light_theme(self):
        """设置浅色主题"""
        style = """
        QMainWindow {
            background-color: #f5f5f5;
            color: #333333;
        }
        QTabWidget::pane {
            border: 1px solid #c0c0c0;
            background-color: white;
        }
        QTabWidget::tab-bar {
            alignment: center;
        }
        QTabBar::tab {
            background-color: #e0e0e0;
            padding: 8px 16px;
            margin-right: 2px;
            color: #333333;
        }
        QTabBar::tab:selected {
            background-color: white;
            border-bottom: 2px solid #007acc;
        }
        QTabBar::tab:hover {
            background-color: #f0f0f0;
        }
        QMenuBar {
            background-color: #f5f5f5;
            color: #333333;
        }
        QMenuBar::item:selected {
            background-color: #e0e0e0;
        }
        QMenu {
            background-color: white;
            color: #333333;
            border: 1px solid #c0c0c0;
        }
        QMenu::item:selected {
            background-color: #007acc;
            color: white;
        }
        QStatusBar {
            background-color: #f5f5f5;
            color: #333333;
        }
        """
        self.setStyleSheet(style)
    
    def set_dark_theme(self):
        """设置深色主题"""
        style = """
        QMainWindow {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QWidget {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QTabWidget::pane {
            border: 1px solid #404040;
            background-color: #363636;
        }
        QTabWidget::tab-bar {
            alignment: center;
        }
        QTabBar::tab {
            background-color: #404040;
            padding: 8px 16px;
            margin-right: 2px;
            color: #ffffff;
            border: 1px solid #555555;
        }
        QTabBar::tab:selected {
            background-color: #363636;
            border-bottom: 2px solid #007acc;
            border-top: 1px solid #404040;
            border-left: 1px solid #404040;
            border-right: 1px solid #404040;
        }
        QTabBar::tab:hover {
            background-color: #505050;
        }
        QMenuBar {
            background-color: #2b2b2b;
            color: #ffffff;
            border-bottom: 1px solid #404040;
        }
        QMenuBar::item {
            background-color: transparent;
            padding: 4px 8px;
        }
        QMenuBar::item:selected {
            background-color: #404040;
        }
        QMenu {
            background-color: #363636;
            color: #ffffff;
            border: 1px solid #555555;
        }
        QMenu::item {
            padding: 6px 20px;
        }
        QMenu::item:selected {
            background-color: #007acc;
            color: white;
        }
        QMenu::separator {
            height: 1px;
            background-color: #555555;
            margin: 2px 0px;
        }
        QStatusBar {
            background-color: #2b2b2b;
            color: #ffffff;
            border-top: 1px solid #404040;
        }
        QSplitter::handle {
            background-color: #404040;
        }
        QSplitter::handle:horizontal {
            width: 3px;
        }
        /* 滚动条样式 */
        QScrollBar:vertical {
            background-color: #2b2b2b;
            width: 12px;
            border: none;
        }
        QScrollBar::handle:vertical {
            background-color: #555555;
            border-radius: 6px;
            min-height: 20px;
        }
        QScrollBar::handle:vertical:hover {
            background-color: #666666;
        }
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            height: 0px;
        }
        QScrollBar::add-page:vertical,
        QScrollBar::sub-page:vertical {
            background-color: transparent;
        }
        QScrollBar:horizontal {
            background-color: #2b2b2b;
            height: 12px;
            border: none;
        }
        QScrollBar::handle:horizontal {
            background-color: #555555;
            border-radius: 6px;
            min-width: 20px;
        }
        QScrollBar::handle:horizontal:hover {
            background-color: #666666;
        }
        QScrollBar::add-line:horizontal,
        QScrollBar::sub-line:horizontal {
            width: 0px;
        }
        QScrollBar::add-page:horizontal,
        QScrollBar::sub-page:horizontal {
            background-color: transparent;
        }
        /* 工具提示 */
        QToolTip {
            background-color: #363636;
            color: #ffffff;
            border: 1px solid #555555;
            padding: 4px;
        }
        /* 消息框 */
        QMessageBox {
            background-color: #363636;
            color: #ffffff;
        }
        QMessageBox QPushButton {
            background-color: #505050;
            border: 1px solid #666666;
            padding: 6px 12px;
            border-radius: 3px;
            color: #ffffff;
            min-width: 60px;
        }
        QMessageBox QPushButton:hover {
            background-color: #606060;
        }
        QMessageBox QPushButton:default {
            background-color: #007acc;
        }
        QMessageBox QPushButton:default:hover {
            background-color: #005a9e;
        }
        """
        self.setStyleSheet(style)
    
    def setup_connections(self):
        """设置信号连接"""
        # 人格切换信号
        self.personality_widget.personality_changed.connect(self.on_personality_changed)
        
        # 记忆更新信号
        self.memory_widget.memory_updated.connect(self.on_memory_updated)
    
    def on_personality_changed(self, personality_id: str):
        """人格切换处理"""
        self.chat_widget.on_personality_changed()
        self.memory_widget.refresh_memories()
        self.update_status_bar()
    
    def on_memory_updated(self):
        """记忆更新处理"""
        self.memory_widget.refresh_memories()
    
    def update_status_bar(self):
        """更新状态栏"""
        personality = self.chat_engine.get_current_personality_info()
        if personality:
            status_text = f"当前人格: {personality['name']}"
            memory_summary = self.chat_engine.get_memory_summary()
            status_text += f" | 记忆数量: {memory_summary['total_count']}"
            self.status_bar.showMessage(status_text)
    
    def new_chat(self):
        """新建对话"""
        reply = QMessageBox.question(
            self, '新建对话', 
            '确定要开始新的对话吗？当前对话记录将被清空。',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.clear_chat()
    
    def clear_chat(self):
        """清空聊天记录"""
        self.chat_engine.clear_chat_history()
        self.chat_widget.clear_chat()
        self.status_bar.showMessage("聊天记录已清空", 2000)
    
    def toggle_theme(self):
        """切换主题"""
        self.is_dark_theme = not self.is_dark_theme
        theme_name = 'dark' if self.is_dark_theme else 'light'
        
        # 保存主题设置
        self.settings.set('ui.theme', theme_name)
        
        # 更新样式
        self.set_style()
        
        # 通知子组件更新主题
        self.chat_widget.set_theme(self.is_dark_theme)
        self.personality_widget.set_theme(self.is_dark_theme)
        self.memory_widget.set_theme(self.is_dark_theme)
        
        # 显示切换提示
        theme_text = "深色主题" if self.is_dark_theme else "浅色主题"
        self.status_bar.showMessage(f"已切换到{theme_text}", 2000)
    
    def show_about(self):
        """显示关于对话框"""
        about_text = """
        <h3>Sentimemory</h3>
        <p>版本: 1.0.0</p>
        <p>一款基于Python开发的AI聊天工具</p>
        <p>具有情感化互动和记忆功能</p>
        <br>
        <p>开发者: 程序设计实习大作业</p>
        """
        QMessageBox.about(self, '关于 Sentimemory', about_text)
    
    def closeEvent(self, event):
        """关闭事件处理"""
        # 首先清除对话
        self.clear_chat()
        
        event.accept() 