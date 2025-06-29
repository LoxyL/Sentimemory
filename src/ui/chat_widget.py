# -*- coding: utf-8 -*-
"""
聊天界面组件
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
                             QLineEdit, QPushButton, QScrollArea, QLabel,
                             QFrame, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QTimer
from PyQt5.QtGui import QFont, QTextCursor, QPalette
from datetime import datetime


class ChatBubble(QFrame):
    """聊天气泡"""
    
    def __init__(self, message: str, sender: str = "user", timestamp: str = None, is_dark_theme: bool = False):
        super().__init__()
        self.message = message
        self.sender = sender
        self.timestamp = timestamp or datetime.now().strftime("%H:%M")
        self.is_dark_theme = is_dark_theme
        
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        # 设置框架样式，确保没有边框
        self.setFrameStyle(QFrame.NoFrame)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        
        # 消息内容
        message_label = QLabel(self.message)
        message_label.setWordWrap(True)
        message_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        
        # 时间戳
        time_label = QLabel(self.timestamp)
        time_label.setAlignment(Qt.AlignRight if self.sender == "user" else Qt.AlignLeft)
        time_label.setStyleSheet("color: #888; font-size: 10px;")
        
        layout.addWidget(message_label)
        layout.addWidget(time_label)
        
        # 设置样式
        self.set_bubble_style()
    
    def set_bubble_style(self):
        """设置气泡样式"""
        if self.sender == "user":
            # 用户消息 - 蓝色，右对齐
            style = """
            QFrame {
                background-color: #007acc;
                color: white;
                border: none;
                border-radius: 15px;
                margin-left: 50px;
                margin-right: 10px;
            }
            QLabel {
                background-color: transparent;
                color: white;
                border: none;
            }
            """
        elif self.sender == "ai":
            # AI消息 - 根据主题调整颜色
            if self.is_dark_theme:
                bg_color = "#404040"
                text_color = "#ffffff"
            else:
                bg_color = "#f0f0f0"
                text_color = "#333333"
            
            style = f"""
            QFrame {{
                background-color: {bg_color};
                color: {text_color};
                border: none;
                border-radius: 15px;
                margin-left: 10px;
                margin-right: 50px;
            }}
            QLabel {{
                background-color: transparent;
                color: {text_color};
                border: none;
            }}
            """
        else:
            # 系统消息 - 根据主题调整颜色
            if self.is_dark_theme:
                bg_color = "#555555"
                text_color = "#cccccc"
            else:
                bg_color = "#ffffcc"
                text_color = "#666666"
            
            style = f"""
            QFrame {{
                background-color: {bg_color};
                color: {text_color};
                border: none;
                border-radius: 10px;
                margin-left: 100px;
                margin-right: 100px;
            }}
            QLabel {{
                background-color: transparent;
                color: {text_color};
                border: none;
                text-align: center;
            }}
            """
        
        self.setStyleSheet(style)
    
    def set_theme(self, is_dark_theme: bool):
        """设置主题"""
        self.is_dark_theme = is_dark_theme
        self.set_bubble_style()


class ChatWidget(QWidget):
    """聊天界面组件"""
    
    message_sent = pyqtSignal(str)
    
    def __init__(self, chat_engine):
        super().__init__()
        self.chat_engine = chat_engine
        self.is_dark_theme = False
        self.init_ui()
        self.setup_connections()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 聊天显示区域
        self.create_chat_display()
        layout.addWidget(self.chat_scroll_area)
        
        # 输入区域
        self.create_input_area()
        layout.addWidget(self.input_frame)
        
        # 设置样式
        self.set_style()
    
    def create_chat_display(self):
        """创建聊天显示区域"""
        # 滚动区域
        self.chat_scroll_area = QScrollArea()
        self.chat_scroll_area.setWidgetResizable(True)
        self.chat_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.chat_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # 聊天内容容器
        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setContentsMargins(10, 10, 10, 10)
        self.chat_layout.setSpacing(10)
        self.chat_layout.addStretch()  # 添加弹性空间，使消息从底部开始
        
        self.chat_scroll_area.setWidget(self.chat_container)
        
        # 添加欢迎消息
        self.add_welcome_message()
    
    def create_input_area(self):
        """创建输入区域"""
        self.input_frame = QFrame()
        self.input_frame.setFrameStyle(QFrame.NoFrame)  # 确保没有边框
        self.input_frame.setFixedHeight(80)
        
        layout = QHBoxLayout(self.input_frame)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # 输入框
        self.input_edit = QLineEdit()
        self.input_edit.setPlaceholderText("请输入您的消息...")
        self.input_edit.setFixedHeight(40)
        
        # 发送按钮
        self.send_button = QPushButton("发送")
        self.send_button.setFixedSize(80, 40)
        self.send_button.setDefault(True)
        
        layout.addWidget(self.input_edit)
        layout.addWidget(self.send_button)
    
    def set_style(self):
        """设置样式"""
        if self.is_dark_theme:
            self.set_dark_style()
        else:
            self.set_light_style()
    
    def set_light_style(self):
        """设置浅色样式"""
        style = """
        QScrollArea {
            border: none;
            background-color: white;
        }
        QFrame {
            background-color: #f8f9fa;
            border: none;
        }
        QLineEdit {
            border: 2px solid #e0e0e0;
            border-radius: 20px;
            padding: 8px 15px;
            font-size: 12px;
            background-color: white;
            color: #333333;
        }
        QLineEdit:focus {
            border-color: #007acc;
        }
        QPushButton {
            background-color: #007acc;
            color: white;
            border: none;
            border-radius: 20px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #005a9e;
        }
        QPushButton:pressed {
            background-color: #004080;
        }
        QPushButton:disabled {
            background-color: #cccccc;
            color: #888888;
        }
        """
        self.setStyleSheet(style)
    
    def set_dark_style(self):
        """设置深色样式"""
        style = """
        QScrollArea {
            border: none;
            background-color: #2b2b2b;
        }
        QFrame {
            background-color: #1e1e1e;
            border: none;
        }
        QLineEdit {
            border: 2px solid #555555;
            border-radius: 20px;
            padding: 8px 15px;
            font-size: 12px;
            background-color: #363636;
            color: #ffffff;
        }
        QLineEdit:focus {
            border-color: #007acc;
        }
        QPushButton {
            background-color: #007acc;
            color: white;
            border: none;
            border-radius: 20px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #005a9e;
        }
        QPushButton:pressed {
            background-color: #004080;
        }
        QPushButton:disabled {
            background-color: #555555;
            color: #888888;
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
        """
        self.setStyleSheet(style)
    
    def set_theme(self, is_dark_theme: bool):
        """设置主题"""
        self.is_dark_theme = is_dark_theme
        self.set_style()
        
        # 更新所有聊天气泡的主题
        for i in range(self.chat_layout.count()):
            item = self.chat_layout.itemAt(i)
            if item and item.widget() and isinstance(item.widget(), ChatBubble):
                item.widget().set_theme(is_dark_theme)
    
    def setup_connections(self):
        """设置信号连接"""
        self.send_button.clicked.connect(self.send_message)
        self.input_edit.returnPressed.connect(self.send_message)
    
    def add_welcome_message(self):
        """添加欢迎消息"""
        personality = self.chat_engine.get_current_personality_info()
        if personality:
            welcome_text = f"你好！我是{personality['name']}，{personality['description']}。有什么我可以帮助你的吗？"
        else:
            welcome_text = "你好！欢迎使用Sentimemory AI聊天工具！"
        
        self.add_message(welcome_text, "ai")
    
    def add_message(self, message: str, sender: str = "user"):
        """添加消息"""
        # 移除弹性空间
        if self.chat_layout.count() > 0:
            last_item = self.chat_layout.itemAt(self.chat_layout.count() - 1)
            if last_item.spacerItem():
                self.chat_layout.removeItem(last_item)
        
        # 创建消息气泡
        bubble = ChatBubble(message, sender, is_dark_theme=self.is_dark_theme)
        self.chat_layout.addWidget(bubble)
        
        # 重新添加弹性空间
        self.chat_layout.addStretch()
        
        # 滚动到底部
        QTimer.singleShot(100, self.scroll_to_bottom)
    
    def scroll_to_bottom(self):
        """滚动到底部"""
        scrollbar = self.chat_scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def send_message(self):
        """发送消息"""
        message = self.input_edit.text().strip()
        if not message:
            return
        
        # 清空输入框
        self.input_edit.clear()
        
        # 禁用发送按钮
        self.send_button.setEnabled(False)
        self.send_button.setText("发送中...")
        
        # 添加用户消息
        self.add_message(message, "user")
        
        # 模拟AI思考延迟
        QTimer.singleShot(1000, lambda: self.get_ai_response(message))
    
    def get_ai_response(self, user_message: str):
        """获取AI回复"""
        try:
            # 获取AI回复
            ai_response = self.chat_engine.send_message(user_message)
            
            # 添加AI回复
            self.add_message(ai_response, "ai")
            
        except Exception as e:
            # 错误处理
            error_message = f"抱歉，我遇到了一些问题：{str(e)}"
            self.add_message(error_message, "ai")
        
        finally:
            # 重新启用发送按钮
            self.send_button.setEnabled(True)
            self.send_button.setText("发送")
            self.input_edit.setFocus()
    
    def clear_chat(self):
        """清空聊天记录"""
        # 清除所有消息气泡
        while self.chat_layout.count() > 1:  # 保留最后的弹性空间
            item = self.chat_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # 重新添加欢迎消息
        self.add_welcome_message()
    
    def on_personality_changed(self):
        """人格切换处理"""
        # 添加系统消息
        personality = self.chat_engine.get_current_personality_info()
        if personality:
            system_message = f"已切换到{personality['name']}人格"
            self.add_message(system_message, "system")
            
            # 添加新的欢迎消息
            welcome_text = f"你好！我现在是{personality['name']}，{personality['description']}。"
            self.add_message(welcome_text, "ai") 