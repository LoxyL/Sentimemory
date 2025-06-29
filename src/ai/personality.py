# -*- coding: utf-8 -*-
"""
AI人格管理模块
"""

import json
import os
from typing import Dict, List, Optional
from utils.logger import get_logger


class PersonalityManager:
    """AI人格管理器"""
    
    def __init__(self, config_path: str = None):
        self.logger = get_logger("sentimemory.personality")
        self.logger.info("PersonalityManager初始化开始")
        
        if config_path is None:
            # 默认配置文件路径
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(current_dir, '..', '..', 'config', 'personalities.json')
        
        self.config_path = config_path
        self.logger.debug("人格配置文件路径", {"config_path": config_path})
        
        self.personalities = self.load_personalities()
        self.current_personality = None
        
        # 设置默认人格
        default_id = self.personalities.get('default_personality', 'friendly')
        self.logger.debug("设置默认人格", {"default_personality": default_id})
        self.set_personality(default_id)
        
        self.logger.info("PersonalityManager初始化完成", {
            "total_personalities": len(self.get_personalities()),
            "current_personality": self.current_personality
        })
    
    def load_personalities(self) -> Dict:
        """加载人格配置"""
        self.logger.debug("开始加载人格配置")
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                personalities = json.load(f)
                
            self.logger.log_config_load("人格配置", {
                "config_path": self.config_path,
                "personalities_count": len(personalities.get('personalities', {})),
                "default_personality": personalities.get('default_personality')
            }, True)
            
            return personalities
            
        except Exception as e:
            self.logger.log_error_with_context(e, "加载人格配置", {
                "config_path": self.config_path
            })
            
            default_config = self._get_default_personalities()
            self.logger.warning("使用默认人格配置", {
                "personalities_count": len(default_config.get('personalities', {}))
            })
            return default_config
    
    def _get_default_personalities(self) -> Dict:
        """获取默认人格配置"""
        self.logger.debug("生成默认人格配置")
        
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
        personality_list = [
            {
                'id': pid,
                'name': pdata.get('name', pid),
                'description': pdata.get('description', ''),
                'traits': pdata.get('personality_traits', [])
            }
            for pid, pdata in personalities.items()
        ]
        
        self.logger.debug("获取人格列表", {
            "count": len(personality_list),
            "personalities": [p['id'] for p in personality_list]
        })
        
        return personality_list
    
    def set_personality(self, personality_id: str) -> bool:
        """设置当前人格"""
        old_personality = self.current_personality
        
        self.logger.debug("尝试设置人格", {
            "from_personality": old_personality,
            "to_personality": personality_id
        })
        
        personalities = self.get_personalities()
        if personality_id in personalities:
            self.current_personality = personality_id
            
            personality_info = personalities[personality_id]
            self.logger.info("人格设置成功", {
                "personality_id": personality_id,
                "personality_name": personality_info.get('name', '未知'),
                "personality_traits": personality_info.get('personality_traits', []),
                "response_style": personality_info.get('response_style', '未知')
            })
            
            return True
        else:
            self.logger.warning("人格设置失败：人格不存在", {
                "personality_id": personality_id,
                "available_personalities": list(personalities.keys())
            })
            return False
    
    def get_current_personality(self) -> Optional[Dict]:
        """获取当前人格信息"""
        if self.current_personality:
            personalities = self.get_personalities()
            personality_info = personalities.get(self.current_personality)
            
            self.logger.debug("获取当前人格信息", {
                "personality_id": self.current_personality,
                "has_info": personality_info is not None
            })
            
            return personality_info
        
        self.logger.warning("当前无人格设置")
        return None
    
    def get_current_personality_id(self) -> Optional[str]:
        """获取当前人格ID"""
        self.logger.debug("获取当前人格ID", {"personality_id": self.current_personality})
        return self.current_personality
    
    def get_system_prompt(self) -> str:
        """获取当前人格的系统提示"""
        personality = self.get_current_personality()
        if personality:
            system_prompt = personality.get('system_prompt', '')
            self.logger.debug("获取系统提示", {
                "personality_id": self.current_personality,
                "prompt_length": len(system_prompt)
            })
            return system_prompt
        
        self.logger.warning("无法获取系统提示：未设置人格")
        return ''
    
    def get_memory_focus(self) -> List[str]:
        """获取当前人格的记忆关注点"""
        personality = self.get_current_personality()
        if personality:
            memory_focus = personality.get('memory_focus', [])
            self.logger.debug("获取记忆关注点", {
                "personality_id": self.current_personality,
                "focus_areas": memory_focus
            })
            return memory_focus
        
        self.logger.warning("无法获取记忆关注点：未设置人格")
        return []
    
    def get_response_style(self) -> str:
        """获取当前人格的回应风格"""
        personality = self.get_current_personality()
        if personality:
            response_style = personality.get('response_style', 'neutral')
            self.logger.debug("获取回应风格", {
                "personality_id": self.current_personality,
                "response_style": response_style
            })
            return response_style
        
        self.logger.warning("无法获取回应风格：未设置人格")
        return 'neutral' 