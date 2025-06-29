#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sentimemory 系统状态检查
"""

import os
import sys

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def check_system_status():
    """检查系统状态"""
    print("=== Sentimemory 系统状态检查 ===\n")
    
    # 1. 检查环境变量
    print("1. 环境变量检查:")
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("OPENAI_API_KEY", "")
        base_url = os.getenv("OPENAI_BASE_URL", "")
        model = os.getenv("OPENAI_MODEL", "")
        
        if api_key:
            print(f"   ✅ OPENAI_API_KEY: {api_key[:10]}...")
        else:
            print("   ❌ OPENAI_API_KEY: 未设置")
            
        print(f"   ✅ OPENAI_BASE_URL: {base_url}")
        print(f"   ✅ OPENAI_MODEL: {model}")
        
    except Exception as e:
        print(f"   ❌ 环境变量加载失败: {e}")
        return False
    
    # 2. 检查配置设置
    print("\n2. 配置设置检查:")
    try:
        from config.settings import AppSettings
        settings = AppSettings()
        
        if settings.is_openai_configured():
            print("   ✅ OpenAI 配置已设置")
            config = settings.get_openai_config()
            print(f"   ✅ Base URL: {config['base_url']}")
            print(f"   ✅ Model: {config['model']}")
        else:
            print("   ❌ OpenAI 配置未设置")
            return False
            
    except Exception as e:
        print(f"   ❌ 配置设置检查失败: {e}")
        return False
    
    # 3. 检查ChatEngine初始化
    print("\n3. ChatEngine 初始化检查:")
    try:
        from ai.chat_engine import ChatEngine
        engine = ChatEngine(settings)
        print("   ✅ ChatEngine 初始化成功")
        
    except Exception as e:
        print(f"   ❌ ChatEngine 初始化失败: {e}")
        return False
    
    # 4. 检查API连接
    print("\n4. API 连接测试:")
    try:
        print("   正在测试API连接...")
        response = engine.send_message("测试连接")
        if response and len(response) > 0:
            print("   ✅ API 连接成功")
            print(f"   回复: {response[:50]}...")
        else:
            print("   ❌ API 连接失败：空响应")
            return False
            
    except Exception as e:
        print(f"   ❌ API 连接失败: {e}")
        return False
    
    # 5. 检查依赖包
    print("\n5. 依赖包检查:")
    required_packages = [
        "PyQt5", "openai", "requests", "json5", 
        "python-dotenv", "typing-extensions"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            if package == "python-dotenv":
                import dotenv
            elif package == "typing-extensions":
                import typing_extensions
            elif package == "PyQt5":
                import PyQt5
            else:
                __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} (未安装)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n   缺少依赖包: {', '.join(missing_packages)}")
        print("   请运行: pip install -r requirements.txt")
        return False
    
    print("\n=== 系统状态检查完成 ===")
    print("✅ 所有检查通过！系统已准备就绪。")
    print("\n可以运行以下命令启动应用:")
    print("   python main.py")
    
    return True

if __name__ == "__main__":
    check_system_status()
