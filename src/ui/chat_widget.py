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
    
    def __init__(self, message: str, sender: str = "user", timestamp: str = None):
        super().__init__()
        self.message = message
        self.sender = sender
        self.timestamp = timestamp or datetime.now().strftime("%H:%M")
        
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
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
                border-radius: 15px;
                margin-left: 50px;
                margin-right: 10px;
            }
            QLabel {
                background-color: transparent;
                color: white;
            }
            """
        elif self.sender == "ai":
            # AI消息 - 灰色，左对齐
            style = """
            QFrame {
                background-color: #f0f0f0;
                color: black;
                border-radius: 15px;
                margin-left: 10px;
                margin-right: 50px;
            }
            QLabel {
                background-color: transparent;
                color: black;
            }
            """
        else:
            # 系统消息 - 居中
            style = """
            QFrame {
                background-color: #ffffcc;
                color: #666;
                border-radius: 10px;
                margin-left: 100px;
                margin-right: 100px;
            }
            QLabel {
                background-color: transparent;
                color: #666;
                text-align: center;
            }
            """
        
        self.setStyleSheet(style)


class ChatWidget(QWidget):
    """聊天界面组件"""
    
    message_sent = pyqtSignal(str)
    
    def __init__(self, chat_engine):
        super().__init__()
        self.chat_engine = chat_engine
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
        style = """
        QScrollArea {
            border: none;
            background-color: white;
        }
        QFrame {
            background-color: #f8f9fa;
            border-top: 1px solid #e0e0e0;
        }
        QLineEdit {
            border: 2px solid #e0e0e0;
            border-radius: 20px;
            padding: 8px 15px;
            font-size: 12px;
            background-color: white;
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
        }
        """
        self.setStyleSheet(style)
    
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
        """添加消息到聊天区域"""
        bubble = ChatBubble(message, sender)
        
        # 在弹性空间之前插入消息气泡
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, bubble)
        
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