# -*- coding: utf-8 -*-
"""
Sentimemory 源代码模块

这是Sentimemory项目的主要源代码包，包含：
- ai: AI相关功能（聊天引擎、人格管理、记忆系统）
- ui: 用户界面组件  
- utils: 工具函数和辅助功能
"""

# 项目信息
__version__ = '1.0.0'
__author__ = '程序设计实习大作业'
__description__ = 'Sentimemory - AI聊天工具'

# 注意：不在包初始化时导入子模块，避免循环依赖
# 各模块应该在需要时单独导入 