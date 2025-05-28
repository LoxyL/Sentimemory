# -*- coding: utf-8 -*-
"""
AI人格管理模块
"""

import json
import os
from typing import Dict, List, Optional


class PersonalityManager:
    """AI人格管理器"""
    
    def __init__(self, config_path: str = None):
        if config_path is None:
            # 默认配置文件路径
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(current_dir, '..', '..', 'config', 'personalities.json')
        
        self.config_path = config_path
        self.personalities = self.load_personalities()
        self.current_personality = None
        
        # 设置默认人格
        default_id = self.personalities.get('default_personality', 'friendly')
        self.set_personality(default_id)
    
    def load_personalities(self) -> Dict:
        """加载人格配置"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载人格配置失败: {e}")
            return self._get_default_personalities()
    
    def _get_default_personalities(self) -> Dict:
        """获取默认人格配置"""
        return {
            "personalities": {
                "friendly": {
                    "name": "友善型",
                    "description": "温和友善，善于倾听和安慰",
                    "system_prompt": "你是一个温和友善的AI助手。",
                    "personality_traits": ["温和", "善解人意"],
                    "response_style": "warm",
                    "emoji_usage": "moderate",
                    "memory_focus": ["情感状态", "个人喜好"]
                }
            },
            "default_personality": "friendly"
        }
    
    def get_personalities(self) -> Dict[str, Dict]:
        """获取所有人格"""
        return self.personalities.get('personalities', {})
    
    def get_personality_list(self) -> List[Dict]:
        """获取人格列表"""
        personalities = self.get_personalities()
        return [
            {
                'id': pid,
                'name': pdata.get('name', pid),
                'description': pdata.get('description', ''),
                'traits': pdata.get('personality_traits', [])
            }
            for pid, pdata in personalities.items()
        ]
    
    def set_personality(self, personality_id: str) -> bool:
        """设置当前人格"""
        personalities = self.get_personalities()
        if personality_id in personalities:
            self.current_personality = personality_id
            return True
        return False
    
    def get_current_personality(self) -> Optional[Dict]:
        """获取当前人格信息"""
        if self.current_personality:
            personalities = self.get_personalities()
            return personalities.get(self.current_personality)
        return None
    
    def get_current_personality_id(self) -> Optional[str]:
        """获取当前人格ID"""
        return self.current_personality
    
    def get_system_prompt(self) -> str:
        """获取当前人格的系统提示"""
        personality = self.get_current_personality()
        if personality:
            return personality.get('system_prompt', '')
        return ''
    
    def get_memory_focus(self) -> List[str]:
        """获取当前人格的记忆关注点"""
        personality = self.get_current_personality()
        if personality:
            return personality.get('memory_focus', [])
        return []
    
    def get_response_style(self) -> str:
        """获取当前人格的回应风格"""
        personality = self.get_current_personality()
        if personality:
            return personality.get('response_style', 'neutral')
        return 'neutral' 