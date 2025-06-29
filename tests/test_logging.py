#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志系统测试脚本
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.utils.logger import get_ai_logger, get_logger
from src.ai.chat_engine import ChatEngine
from config.settings import AppSettings


def test_basic_logging():
    """测试基本日志功能"""
    logger = get_logger("test")
    
    logger.info("开始测试基本日志功能")
    logger.debug("这是一个调试信息", {"test_data": "hello world"})
    logger.warning("这是一个警告", {"warning_type": "test"})
    
    try:
        raise ValueError("这是一个测试错误")
    except Exception as e:
        logger.log_error_with_context(e, "测试错误处理", {"context": "basic_test"})
    
    logger.info("基本日志功能测试完成")


def test_ai_logging():
    """测试AI相关的日志功能"""
    ai_logger = get_ai_logger()
    
    ai_logger.info("开始测试AI日志功能")
    
    # 测试AI请求记录
    ai_logger.log_ai_request(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "你是一个AI助手"},
            {"role": "user", "content": "你好"}
        ],
        temperature=0.7,
        max_tokens=100
    )
    
    # 测试AI响应记录
    ai_logger.log_ai_response(
        response_content="你好！我是AI助手，很高兴为你服务。",
        usage_info={
            "prompt_tokens": 20,
            "completion_tokens": 15,
            "total_tokens": 35
        },
        duration=1.5
    )
    
    # 测试记忆操作记录
    ai_logger.log_memory_operation(
        operation="添加",
        personality_id="friendly",
        memory_data={
            "content": "用户喜欢喝咖啡",
            "category": "preference",
            "importance": 3
        }
    )
    
    # 测试人格切换记录
    ai_logger.log_personality_switch("friendly", "creative", True)
    
    ai_logger.info("AI日志功能测试完成")


def test_chat_engine_logging():
    """测试聊天引擎的日志功能"""
    logger = get_logger("test.chat_engine")
    logger.info("开始测试ChatEngine日志功能")
    
    try:
        # 创建AppSettings和ChatEngine实例
        app_settings = AppSettings()
        chat_engine = ChatEngine(app_settings)
        
        # 测试消息处理（这会触发大量日志）
        response = chat_engine.send_message("你好，我喜欢喝咖啡")
        logger.info("ChatEngine测试消息发送成功", {"response_preview": response[:100]})
        
        # 测试人格切换
        success = chat_engine.switch_personality("friendly")
        logger.info("ChatEngine人格切换测试", {"success": success})
        
        # 测试获取记忆摘要
        summary = chat_engine.get_memory_summary()
        logger.info("ChatEngine记忆摘要获取测试", {"summary": summary})
        
    except Exception as e:
        logger.log_error_with_context(e, "ChatEngine测试", {"test_phase": "chat_engine_test"})
    
    logger.info("ChatEngine日志功能测试完成")


if __name__ == "__main__":
    print("开始日志系统测试...")
    
    print("\n1. 测试基本日志功能")
    test_basic_logging()
    
    print("\n2. 测试AI日志功能")
    test_ai_logging()
    
    print("\n3. 测试ChatEngine日志功能")
    test_chat_engine_logging()
    
    print("\n日志系统测试完成！")
    print("请检查 ./log/ 目录下的日志文件") 