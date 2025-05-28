# -*- coding: utf-8 -*-
"""
AI聊天引擎模块
"""

import json
import time
from typing import List, Dict, Optional, Callable
from datetime import datetime

from .personality import PersonalityManager
from .memory import MemoryManager, MemoryItem


class ChatMessage:
    """聊天消息"""
    
    def __init__(self, content: str, sender: str = "user", timestamp: str = None):
        self.content = content
        self.sender = sender  # "user" 或 "ai"
        self.timestamp = timestamp or datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'content': self.content,
            'sender': self.sender,
            'timestamp': self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ChatMessage':
        """从字典创建消息"""
        return cls(
            content=data['content'],
            sender=data.get('sender', 'user'),
            timestamp=data.get('timestamp')
        )


class ChatEngine:
    """聊天引擎"""
    
    def __init__(self):
        self.personality_manager = PersonalityManager()
        self.memory_manager = MemoryManager()
        self.chat_history: List[ChatMessage] = []
        self.response_callback: Optional[Callable] = None
        
        # 模拟AI回复的模板
        self.response_templates = {
            "warm": [
                "我理解你的感受，{content}",
                "听起来{content}，我很关心你",
                "谢谢你和我分享这些，{content}"
            ],
            "playful": [
                "哈哈，{content}！这很有趣呢~",
                "嘿嘿，{content}，你真有意思！",
                "哇，{content}！我喜欢这样的对话😄"
            ],
            "analytical": [
                "根据你说的{content}，我认为...",
                "从分析角度来看，{content}是很有道理的",
                "让我们深入思考一下{content}这个问题"
            ],
            "creative": [
                "哇！{content}让我想到了很多创意想法！",
                "这真是个有趣的话题！{content}激发了我的灵感",
                "你知道吗？{content}让我联想到..."
            ],
            "thoughtful": [
                "这是一个值得深思的问题。{content}",
                "让我仔细考虑一下{content}",
                "从更深层次来看，{content}"
            ]
        }
    
    def set_response_callback(self, callback: Callable):
        """设置回复回调函数"""
        self.response_callback = callback
    
    def send_message(self, content: str) -> str:
        """发送消息并获取AI回复"""
        # 添加用户消息到历史
        user_message = ChatMessage(content, "user")
        self.chat_history.append(user_message)
        
        # 提取并保存关键信息到记忆
        self._extract_and_save_memories(content)
        
        # 生成AI回复
        ai_response = self._generate_response(content)
        
        # 添加AI回复到历史
        ai_message = ChatMessage(ai_response, "ai")
        self.chat_history.append(ai_message)
        
        return ai_response
    
    def _extract_and_save_memories(self, user_input: str):
        """提取并保存用户输入中的关键信息"""
        personality_id = self.personality_manager.get_current_personality_id()
        if not personality_id:
            return
        
        # 提取关键信息
        focus_areas = self.personality_manager.get_memory_focus()
        memories = self.memory_manager.extract_key_info(user_input, focus_areas)
        
        # 保存到记忆库
        for memory in memories:
            self.memory_manager.add_memory(personality_id, memory)
    
    def _generate_response(self, user_input: str) -> str:
        """生成AI回复"""
        personality = self.personality_manager.get_current_personality()
        if not personality:
            return "抱歉，我现在无法回复。"
        
        # 获取回复风格
        response_style = self.personality_manager.get_response_style()
        
        # 获取相关记忆
        personality_id = self.personality_manager.get_current_personality_id()
        memories = self.memory_manager.get_memories(personality_id, limit=10)
        
        # 构建回复上下文
        context = self._build_context(user_input, memories)
        
        # 生成回复（这里使用模板，实际项目中可以接入真实的AI API）
        response = self._generate_template_response(user_input, response_style, context)
        
        return response
    
    def _build_context(self, user_input: str, memories: List[MemoryItem]) -> str:
        """构建对话上下文"""
        context_parts = []
        
        # 添加人格信息
        personality = self.personality_manager.get_current_personality()
        if personality:
            context_parts.append(f"人格特征: {', '.join(personality.get('personality_traits', []))}")
        
        # 添加相关记忆
        if memories:
            memory_texts = [f"- {memory.content}" for memory in memories[:5]]
            context_parts.append(f"相关记忆:\n{chr(10).join(memory_texts)}")
        
        # 添加最近对话历史
        recent_messages = self.chat_history[-6:]  # 最近3轮对话
        if recent_messages:
            history_texts = []
            for msg in recent_messages:
                prefix = "用户" if msg.sender == "user" else "AI"
                history_texts.append(f"{prefix}: {msg.content}")
            context_parts.append(f"对话历史:\n{chr(10).join(history_texts)}")
        
        return "\n\n".join(context_parts)
    
    def _generate_template_response(self, user_input: str, style: str, context: str) -> str:
        """使用模板生成回复"""
        templates = self.response_templates.get(style, self.response_templates["warm"])
        
        # 简单的关键词提取
        keywords = self._extract_keywords(user_input)
        content_summary = ", ".join(keywords[:3]) if keywords else "你说的内容"
        
        # 选择模板
        import random
        template = random.choice(templates)
        
        # 填充模板
        response = template.format(content=content_summary)
        
        # 根据上下文调整回复
        if "记忆" in context and any(keyword in context for keyword in keywords):
            response += " 我记得你之前提到过类似的事情。"
        
        return response
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 简单的关键词提取（实际项目中可以使用更复杂的NLP技术）
        import re
        
        # 移除标点符号
        clean_text = re.sub(r'[^\w\s]', '', text)
        words = clean_text.split()
        
        # 过滤停用词
        stop_words = {'我', '你', '他', '她', '它', '的', '了', '在', '是', '有', '和', '与', '或', '但', '因为', '所以'}
        keywords = [word for word in words if word not in stop_words and len(word) > 1]
        
        return keywords[:10]  # 返回前10个关键词
    
    def get_chat_history(self) -> List[ChatMessage]:
        """获取聊天历史"""
        return self.chat_history.copy()
    
    def clear_chat_history(self):
        """清空聊天历史"""
        self.chat_history.clear()
    
    def switch_personality(self, personality_id: str) -> bool:
        """切换人格"""
        success = self.personality_manager.set_personality(personality_id)
        if success:
            # 添加系统消息
            personality = self.personality_manager.get_current_personality()
            if personality:
                system_msg = f"已切换到{personality['name']}人格"
                self.chat_history.append(ChatMessage(system_msg, "system"))
        return success
    
    def get_current_personality_info(self) -> Optional[Dict]:
        """获取当前人格信息"""
        return self.personality_manager.get_current_personality()
    
    def get_memory_summary(self) -> Dict:
        """获取记忆摘要"""
        personality_id = self.personality_manager.get_current_personality_id()
        if personality_id:
            return self.memory_manager.get_memory_summary(personality_id)
        return {'total_count': 0, 'category_stats': {}, 'recent_memories': []}