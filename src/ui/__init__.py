# -*- coding: utf-8 -*-
"""
用户界面模块

这个包包含了Sentimemory的所有UI组件：
- MainWindow: 主窗口
- ChatWidget: 聊天界面
- PersonalityWidget: 人格选择界面
- MemoryWidget: 记忆管理界面
"""

# 导入主要的UI组件
from .main_window import MainWindow
from .chat_widget import ChatWidget, ChatBubble
from .personality_widget import PersonalityWidget, PersonalityCard
from .memory_widget import MemoryWidget, MemoryItemWidget

# 定义包的公开接口
__all__ = [
    'MainWindow',
    'ChatWidget',
    'ChatBubble',
    'PersonalityWidget', 
    'PersonalityCard',
    'MemoryWidget',
    'MemoryItemWidget'
] 