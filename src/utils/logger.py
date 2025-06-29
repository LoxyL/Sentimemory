# -*- coding: utf-8 -*-
"""
日志工具模块
"""

import os
import logging
import json
from datetime import datetime
from typing import Any, Dict, Optional
from pathlib import Path


class SentimemoryLogger:
    """Sentimemory专用日志记录器"""
    
    def __init__(self, name: str = "sentimemory", log_level: str = "DEBUG"):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # 创建日志目录
        self.log_dir = Path("./log")
        self.log_dir.mkdir(exist_ok=True)
        
        # 生成日志文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"log_{timestamp}.txt"
        
        # 配置日志格式
        self._setup_handlers()
    
    def _setup_handlers(self):
        """设置日志处理器"""
        # 清除现有的处理器
        self.logger.handlers.clear()
        
        # 文件处理器
        file_handler = logging.FileHandler(
            self.log_file, 
            mode='a', 
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 设置格式
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def debug(self, message: str, extra_data: Optional[Dict] = None):
        """调试级别日志"""
        self._log_with_data(logging.DEBUG, message, extra_data)
    
    def info(self, message: str, extra_data: Optional[Dict] = None):
        """信息级别日志"""
        self._log_with_data(logging.INFO, message, extra_data)
    
    def warning(self, message: str, extra_data: Optional[Dict] = None):
        """警告级别日志"""
        self._log_with_data(logging.WARNING, message, extra_data)
    
    def error(self, message: str, extra_data: Optional[Dict] = None, exc_info: bool = False):
        """错误级别日志"""
        self._log_with_data(logging.ERROR, message, extra_data, exc_info)
    
    def critical(self, message: str, extra_data: Optional[Dict] = None, exc_info: bool = False):
        """严重错误级别日志"""
        self._log_with_data(logging.CRITICAL, message, extra_data, exc_info)
    
    def _log_with_data(self, level: int, message: str, extra_data: Optional[Dict] = None, exc_info: bool = False):
        """带额外数据的日志记录"""
        if extra_data:
            try:
                extra_str = json.dumps(extra_data, ensure_ascii=False, indent=2)
                full_message = f"{message}\n额外数据: {extra_str}"
            except Exception:
                full_message = f"{message}\n额外数据: {str(extra_data)}"
        else:
            full_message = message
        
        self.logger.log(level, full_message, exc_info=exc_info)
    
    def log_ai_request(self, model: str, messages: list, **kwargs):
        """记录AI请求"""
        self.debug("AI请求开始", {
            "model": model,
            "messages_count": len(messages),
            "messages": messages,
            "parameters": kwargs
        })
    
    def log_ai_response(self, response_content: str, usage_info: Optional[Dict] = None, duration: Optional[float] = None):
        """记录AI响应"""
        self.debug("AI响应完成", {
            "response_content": response_content,
            "usage_info": usage_info,
            "duration_seconds": duration
        })
    
    def log_memory_operation(self, operation: str, personality_id: str, memory_data: Any = None):
        """记录记忆操作"""
        self.debug(f"记忆操作: {operation}", {
            "personality_id": personality_id,
            "memory_data": memory_data
        })
    
    def log_personality_switch(self, from_personality: str, to_personality: str, success: bool):
        """记录人格切换"""
        self.info("人格切换", {
            "from": from_personality,
            "to": to_personality,
            "success": success
        })
    
    def log_config_load(self, config_type: str, config_data: Dict, success: bool):
        """记录配置加载"""
        self.debug(f"配置加载: {config_type}", {
            "config_data": config_data,
            "success": success
        })
    
    def log_error_with_context(self, error: Exception, context: str, extra_data: Optional[Dict] = None):
        """记录带上下文的错误"""
        error_data = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context
        }
        if extra_data:
            error_data.update(extra_data)
        
        self.error(f"错误发生在 {context}", error_data, exc_info=True)


# 全局日志实例
_logger_instances = {}

def get_logger(name: str = "sentimemory", log_level: str = "DEBUG") -> SentimemoryLogger:
    """获取日志记录器实例"""
    if name not in _logger_instances:
        _logger_instances[name] = SentimemoryLogger(name, log_level)
    return _logger_instances[name]


# AI专用日志记录器
def get_ai_logger() -> SentimemoryLogger:
    """获取AI专用日志记录器"""
    return get_logger("sentimemory.ai", "DEBUG")


# 快捷函数
def debug(message: str, extra_data: Optional[Dict] = None):
    """调试日志快捷函数"""
    get_logger().debug(message, extra_data)

def info(message: str, extra_data: Optional[Dict] = None):
    """信息日志快捷函数"""
    get_logger().info(message, extra_data)

def warning(message: str, extra_data: Optional[Dict] = None):
    """警告日志快捷函数"""
    get_logger().warning(message, extra_data)

def error(message: str, extra_data: Optional[Dict] = None, exc_info: bool = False):
    """错误日志快捷函数"""
    get_logger().error(message, extra_data, exc_info) 