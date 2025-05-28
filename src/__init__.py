# -*- coding: utf-8 -*-
"""
Sentimemory 源代码模块

这是Sentimemory项目的主要源代码包，包含：
- ai: AI相关功能（聊天引擎、人格管理、记忆系统）
- ui: 用户界面组件
- utils: 工具函数和辅助功能
"""

# 导入主要模块
from . import ai
from . import ui
from . import utils

# 导入核心类，提供顶级访问
from .ai import ChatEngine, PersonalityManager, MemoryManager
from .ui import MainWindow

# 定义包的公开接口
__all__ = [
    'ai',
    'ui', 
    'utils',
    'ChatEngine',
    'PersonalityManager',
    'MemoryManager',
    'MainWindow'
]

# 项目信息
__version__ = '1.0.0'
__author__ = '程序设计实习大作业'
__description__ = 'Sentimemory - AI聊天工具' 