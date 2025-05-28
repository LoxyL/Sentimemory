# -*- coding: utf-8 -*-
"""
AI相关模块

这个包包含了Sentimemory的核心AI功能：
- ChatEngine: 聊天引擎
- PersonalityManager: 人格管理
- MemoryManager: 记忆管理
- MemoryItem: 记忆项数据结构
"""

# 导入核心类，方便外部使用
from .chat_engine import ChatEngine, ChatMessage
from .personality import PersonalityManager
from .memory import MemoryManager, MemoryItem

# 定义包的公开接口
__all__ = [
    'ChatEngine',
    'ChatMessage', 
    'PersonalityManager',
    'MemoryManager',
    'MemoryItem'
]

# 版本信息
__version__ = '1.0.0' 