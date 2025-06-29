# -*- coding: utf-8 -*-
"""
应用程序设置配置
"""

import os
import json
from typing import Dict, Any
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class AppSettings:
    """应用程序设置管理类"""
    
    def __init__(self):
        self.config_dir = os.path.join(os.path.dirname(__file__))
        self.data_dir = os.path.join(os.path.dirname(self.config_dir), 'data')
        self.assets_dir = os.path.join(os.path.dirname(self.config_dir), 'assets')
        
        # 默认设置
        self.default_settings = {
            "window": {
                "width": 1000,
                "height": 700,
                "min_width": 800,
                "min_height": 600
            },
            "ai": {
                "default_personality": "friendly",
                "max_memory_items": 100,
                "response_timeout": 30
            },
            "ui": {
                "theme": "dark",
                "font_size": 12,
                "chat_bubble_style": "modern"
            },
            "data": {
                "auto_save": True,
                "backup_enabled": True,
                "max_chat_history": 1000
            }
        }
        
        self.settings = self.load_settings()
    
    def load_settings(self) -> Dict[str, Any]:
        """加载设置"""
        settings_file = os.path.join(self.config_dir, 'app_settings.json')
        
        if os.path.exists(settings_file):
            try:
                with open(settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载设置失败: {e}")
                return self.default_settings.copy()
        else:
            return self.default_settings.copy()
    
    def save_settings(self):
        """保存设置"""
        settings_file = os.path.join(self.config_dir, 'app_settings.json')
        
        try:
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存设置失败: {e}")
    
    def get(self, key: str, default=None):
        """获取设置值"""
        keys = key.split('.')
        value = self.settings
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """设置值"""
        keys = key.split('.')
        setting = self.settings
        
        for k in keys[:-1]:
            if k not in setting:
                setting[k] = {}
            setting = setting[k]
        
        setting[keys[-1]] = value
        self.save_settings()
    
    def get_openai_config(self) -> Dict[str, str]:
        """获取OpenAI配置"""
        return {
            "api_key": os.getenv("OPENAI_API_KEY", ""),
            "base_url": os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            "model": os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            "http_proxy": os.getenv("HTTP_PROXY", ""),
            "https_proxy": os.getenv("HTTPS_PROXY", "")
        }
    
    def is_openai_configured(self) -> bool:
        """检查OpenAI是否已配置"""
        return bool(os.getenv("OPENAI_API_KEY"))

    def get_debug_mode(self) -> bool:
        """获取调试模式"""
        return os.getenv("APP_DEBUG", "False").lower() == "true"
    
    def get_log_level(self) -> str:
        """获取日志级别"""
        return os.getenv("LOG_LEVEL", "INFO")
