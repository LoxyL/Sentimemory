# -*- coding: utf-8 -*-
"""
AI聊天引擎模块
"""

import json
import time
from openai import OpenAI
from typing import List, Dict, Optional, Callable
from datetime import datetime

from .personality import PersonalityManager
from .memory import MemoryManager, MemoryItem
from config.settings import AppSettings
from utils.logger import get_ai_logger


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
    
    def __init__(self, app_settings: AppSettings = None):
        self.logger = get_ai_logger()
        self.logger.info("ChatEngine初始化开始")
        
        self.personality_manager = PersonalityManager()
        self.memory_manager = MemoryManager()
        self.chat_history: List[ChatMessage] = []
        self.response_callback: Optional[Callable] = None
        
        # 对话历史管理配置
        self.max_chat_history = 30  # 最多保留30轮对话
        self.memory_extract_count = 10  # 达到上限时提取最早10轮的记忆
        
        # 使用传入的AppSettings或创建新实例
        self.app_settings = app_settings or AppSettings()
        self.logger.debug("AppSettings已加载", {
            "settings_type": "传入实例" if app_settings else "新创建实例"
        })
        
        self._setup_openai_client()
        self.logger.info("ChatEngine初始化完成", {
            "max_chat_history": self.max_chat_history,
            "memory_extract_count": self.memory_extract_count
        })
    
    def _setup_openai_client(self):
        """设置OpenAI客户端"""
        self.logger.debug("开始设置OpenAI客户端")
        
        try:
            # 从AppSettings获取AI配置
            api_key = self.app_settings.get('ai.api_key', '')
            base_url = self.app_settings.get('ai.base_url', 'https://api.openai.com/v1')
            
            # 记录配置信息（隐藏敏感信息）
            config_info = {
                "api_key_length": len(api_key) if api_key else 0,
                "api_key_masked": f"{api_key[:8]}..." if len(api_key) > 8 else "未设置",
                "base_url": base_url,
                "model": self.app_settings.get('ai.model', 'gpt-4o-mini'),
                "timeout": self.app_settings.get('ai.response_timeout', 30)
            }
            
            self.client = OpenAI(
                api_key=api_key,
                base_url=base_url
            )
            self.model = self.app_settings.get('ai.model', 'gpt-4o-mini')
            self.timeout = self.app_settings.get('ai.response_timeout', 30)
            
            self.logger.log_config_load("OpenAI配置", config_info, True)
            self.logger.info("OpenAI客户端设置成功")
            
        except Exception as e:
            self.logger.log_error_with_context(e, "OpenAI客户端设置", {"config_info": config_info})
            self.client = None
    
    def set_response_callback(self, callback: Callable):
        """设置回复回调函数"""
        self.logger.debug("设置回复回调函数", {
            "callback_type": str(type(callback))
        })
        self.response_callback = callback
    
    def send_message(self, content: str) -> str:
        """发送消息并获取AI回复"""
        start_time = time.time()
        self.logger.info("开始处理用户消息", {
            "content_length": len(content),
            "content_preview": content[:100] + "..." if len(content) > 100 else content,
            "chat_history_length": len(self.chat_history)
        })
        
        # 管理对话历史：在添加新消息前检查是否需要记忆提取
        self._manage_chat_history_before_add()
        
        # 添加用户消息到历史
        user_message = ChatMessage(content, "user")
        self.chat_history.append(user_message)
        self.logger.debug("用户消息已添加到聊天历史")
        
        # 生成AI回复
        ai_response = self._generate_response(content)
        
        # 添加AI回复到历史
        ai_message = ChatMessage(ai_response, "ai")
        self.chat_history.append(ai_message)
        
        processing_time = time.time() - start_time
        self.logger.info("消息处理完成", {
            "processing_time_seconds": processing_time,
            "response_length": len(ai_response),
            "response_preview": ai_response[:100] + "..." if len(ai_response) > 100 else ai_response,
            "final_chat_history_length": len(self.chat_history)
        })
        
        return ai_response
    
    def _manage_chat_history_before_add(self):
        """在添加新消息前管理对话历史"""
        current_count = len(self.chat_history)
        
        self.logger.debug("检查对话历史长度", {
            "current_count": current_count,
            "max_limit": self.max_chat_history
        })
        
        # 如果当前对话数量达到上限，需要进行记忆提取和清理
        if current_count >= self.max_chat_history:
            self.logger.info("对话历史达到上限，开始提取早期对话记忆", {
                "current_count": current_count,
                "extract_count": self.memory_extract_count
            })
            
            # 提取最早的对话进行记忆处理
            early_conversations = self.chat_history[:self.memory_extract_count]
            self._extract_memories_from_conversations(early_conversations)
            
            # 移除已处理的早期对话
            self.chat_history = self.chat_history[self.memory_extract_count:]
            
            self.logger.info("早期对话记忆提取完成", {
                "extracted_count": len(early_conversations),
                "remaining_count": len(self.chat_history)
            })
    
    def _extract_memories_from_conversations(self, conversations: List[ChatMessage]):
        """从对话片段中提取记忆"""
        if not conversations:
            return
        
        personality_id = self.personality_manager.get_current_personality_id()
        if not personality_id or not self.client:
            self.logger.warning("无法提取对话记忆：缺少人格ID或AI客户端")
            return
        
        self.logger.debug("开始从对话片段提取记忆", {
            "conversation_count": len(conversations),
            "personality_id": personality_id
        })
        
        # 将对话转换为文本
        conversation_text = self._conversations_to_text(conversations)
        
        try:
            # 使用AI从对话片段中提取关键记忆
            system_prompt = """你是一个记忆提取专家。请从这段对话历史中提取重要信息，包括：
1. 用户表达的重要事件和经历
2. 用户的情感状态和变化
3. 用户的个人偏好和兴趣
4. 重要的日期、时间或人物关系
5. 用户的目标、计划或担忧
6. 用户的个人信息（姓名、年龄、职业、居住地等）
7. 用户的学习和工作情况
8. 用户的生活习惯和爱好

请仔细分析整段对话，提取所有有价值的信息。每个记忆项应该是独立且有意义的。

请以JSON格式返回，每个记忆项包含：
- content: 记忆内容描述（要完整且具体）
- category: 分类（personal/event/emotion/preference/date/relationship/goal/habit/work/study）
- importance: 重要性（1-5，5最重要）
- tags: 相关标签列表

尽可能多地提取有价值的信息，不要遗漏重要细节。

示例格式：
[
    {
        "content": "用户名叫张三，今年25岁",
        "category": "personal",
        "importance": 4,
        "tags": ["姓名", "年龄", "基本信息"]
    },
    {
        "content": "用户正在学习Python编程，目标是成为AI工程师",
        "category": "goal",
        "importance": 5,
        "tags": ["学习", "编程", "Python", "AI工程师", "职业目标"]
    },
    {
        "content": "用户每天喝3-4杯咖啡，咖啡是日常生活的重要部分",
        "category": "habit",
        "importance": 3,
        "tags": ["咖啡", "饮食习惯", "日常生活"]
    }
]"""

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"请从以下对话历史中提取关键记忆：\n\n{conversation_text}"}
            ]
            
            self.logger.log_ai_request(
                model=self.model,
                messages=messages,
                timeout=self.timeout,
                purpose="对话记忆提取"
            )

            extract_start_time = time.time()
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                timeout=self.timeout
            )
            
            ai_response = response.choices[0].message.content
            extract_duration = time.time() - extract_start_time
            
            # 记录使用信息
            usage_info = None
            if hasattr(response, 'usage'):
                usage_info = {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            
            self.logger.log_ai_response(
                response_content=ai_response,
                usage_info=usage_info,
                duration=extract_duration
            )
            
            # 解析AI返回的记忆数据
            try:
                # 清理AI返回的内容，移除可能的markdown代码块标记
                cleaned_response = ai_response.strip()
                if cleaned_response.startswith("```json"):
                    cleaned_response = cleaned_response[7:]  # 移除 ```json
                if cleaned_response.endswith("```"):
                    cleaned_response = cleaned_response[:-3]  # 移除结尾的 ```
                cleaned_response = cleaned_response.strip()
                
                memories_data = json.loads(cleaned_response)
                if isinstance(memories_data, list):
                    saved_count = 0
                    for memory_data in memories_data:
                        memory = MemoryItem(
                            content=memory_data.get('content', ''),
                            category=memory_data.get('category', 'general'),
                            importance=memory_data.get('importance', 3),
                            tags=memory_data.get('tags', [])
                        )
                        self.memory_manager.add_memory(personality_id, memory)
                        self.logger.log_memory_operation("添加(对话提取)", personality_id, memory_data)
                        saved_count += 1
                    
                    self.logger.info(f"对话记忆提取成功，从{len(conversations)}轮对话中保存了{saved_count}个记忆项", {
                        "conversation_count": len(conversations),
                        "extracted_memories": saved_count,
                        "memory_categories": list(set(m.get('category', 'unknown') for m in memories_data))
                    })
                    
                else:
                    self.logger.warning("AI返回的对话记忆数据格式不是列表", {
                        "response_type": type(memories_data).__name__,
                        "response_content": cleaned_response
                    })
                    
            except json.JSONDecodeError as e:
                self.logger.warning("AI返回的对话记忆JSON格式无效", {
                    "json_error": str(e),
                    "ai_response": ai_response,
                    "cleaned_response": cleaned_response
                })
                
        except Exception as e:
            self.logger.log_error_with_context(e, "对话记忆提取", {
                "personality_id": personality_id,
                "conversation_count": len(conversations)
            })
    
    def _conversations_to_text(self, conversations: List[ChatMessage]) -> str:
        """将对话列表转换为文本格式"""
        text_parts = []
        for msg in conversations:
            sender_label = "用户" if msg.sender == "user" else "AI"
            text_parts.append(f"{sender_label}: {msg.content}")
        
        return "\n".join(text_parts)
    
    def _extract_and_save_memories(self, user_input: str):
        """使用AI提取并保存用户输入中的关键信息"""
        self.logger.debug("开始提取和保存记忆", {
            "input_length": len(user_input)
        })
        
        personality_id = self.personality_manager.get_current_personality_id()
        if not personality_id:
            self.logger.warning("无法提取记忆：未设置人格ID")
            return
        
        if not self.client:
            self.logger.warning("无法提取记忆：OpenAI客户端未配置")
            return
        
        start_time = time.time()
        
        try:
            # 使用AI提取关键信息
            system_prompt = """你是一个记忆提取专家。请从用户的输入中提取关键信息，包括：
1. 重要事件
2. 情感状态
3. 个人偏好
4. 重要日期或时间
5. 人物关系

请以JSON格式返回，每个记忆项包含以下字段：
- content: 记忆内容描述
- category: 分类（event/emotion/preference/date/relationship）
- importance: 重要性（1-5，5最重要）
- tags: 相关标签列表

示例格式：
[
    {
        "content": "用户喜欢喝咖啡",
        "category": "preference",
        "importance": 3,
        "tags": ["咖啡", "饮品", "偏好"]
    }
]"""

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"请从以下文本中提取关键信息：\n{user_input}"}
            ]
            
            self.logger.log_ai_request(
                model=self.model,
                messages=messages,
                timeout=self.timeout,
                purpose="记忆提取"
            )

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                timeout=self.timeout
            )
            
            ai_response = response.choices[0].message.content
            extract_start_time = time.time()
            
            # 记录使用信息
            usage_info = None
            if hasattr(response, 'usage'):
                usage_info = {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            
            self.logger.log_ai_response(
                response_content=ai_response,
                usage_info=usage_info,
                duration=time.time() - extract_start_time
            )
            
            # 解析AI返回的JSON
            try:
                memories_data = json.loads(ai_response)
                if isinstance(memories_data, list):
                    saved_count = 0
                    for memory_data in memories_data:
                        memory = MemoryItem(
                            content=memory_data.get('content', ''),
                            category=memory_data.get('category', 'general'),
                            importance=memory_data.get('importance', 3),
                            tags=memory_data.get('tags', [])
                        )
                        self.memory_manager.add_memory(personality_id, memory)
                        self.logger.log_memory_operation("添加", personality_id, memory_data)
                        saved_count += 1
                    
                    self.logger.info(f"AI记忆提取成功，保存了{saved_count}个记忆项")
                    
                else:
                    self.logger.warning("AI返回的记忆数据格式不是列表", {
                        "response_type": type(memories_data).__name__,
                        "response_content": ai_response
                    })
                    
            except json.JSONDecodeError as e:
                self.logger.warning("AI返回的JSON格式无效，使用备用方法", {
                    "json_error": str(e),
                    "ai_response": ai_response
                })
                
                # 如果AI返回的不是有效JSON，创建一个简单的记忆项
                memory = MemoryItem(
                    content=user_input[:100],  # 截取前100个字符
                    category='general',
                    importance=3,
                    tags=self._extract_simple_keywords(user_input)
                )
                self.memory_manager.add_memory(personality_id, memory)
                self.logger.log_memory_operation("添加(备用)", personality_id, memory.to_dict())
                
        except Exception as e:
            self.logger.log_error_with_context(e, "AI记忆提取", {
                "personality_id": personality_id,
                "input_preview": user_input[:200]
            })
            
            # 回退到简单的关键词提取
            self.logger.info("回退到简单记忆提取方法")
            focus_areas = self.personality_manager.get_memory_focus()
            memories = self.memory_manager.extract_key_info(user_input, focus_areas)
            for memory in memories:
                self.memory_manager.add_memory(personality_id, memory)
                self.logger.log_memory_operation("添加(简单提取)", personality_id, memory.to_dict())
    
    def _extract_simple_keywords(self, text: str) -> List[str]:
        """简单的关键词提取（备用方法）"""
        self.logger.debug("使用简单关键词提取", {"text_length": len(text)})
        
        import re
        clean_text = re.sub(r'[^\w\s]', '', text)
        words = clean_text.split()
        stop_words = {'我', '你', '他', '她', '它', '的', '了', '在', '是', '有', '和', '与', '或', '但', '因为', '所以'}
        keywords = [word for word in words if word not in stop_words and len(word) > 1]
        
        result = keywords[:5]
        self.logger.debug("关键词提取完成", {"keywords": result})
        return result
    
    def _generate_response(self, user_input: str) -> str:
        """使用真实AI生成回复"""
        self.logger.debug("开始生成AI回复")
        
        personality = self.personality_manager.get_current_personality()
        if not personality:
            self.logger.warning("无法生成回复：未设置人格")
            return "抱歉，我现在无法回复。"
        
        if not self.client:
            self.logger.error("无法生成回复：OpenAI客户端未配置")
            return "抱歉，AI服务未正确配置。"
        
        start_time = time.time()
        
        try:
            # 获取相关记忆
            personality_id = self.personality_manager.get_current_personality_id()
            memories = self.memory_manager.get_memories(personality_id, limit=10)
            
            self.logger.debug("获取相关记忆", {
                "personality_id": personality_id,
                "memory_count": len(memories),
                "memories": [m.to_dict() for m in memories]
            })
            
            # 构建人格和记忆上下文
            context = self._build_ai_context(user_input, memories, personality)
            
            # 构建对话历史
            messages = self._build_conversation_history()
            
            # 添加系统提示
            system_prompt = f"""你是一个AI助手，具有以下人格特征：
{context}

请根据这些信息和对话历史，以符合人格特征的方式回复用户。保持对话的连贯性和个性化。"""

            messages.insert(0, {"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": user_input})
            
            self.logger.log_ai_request(
                model=self.model,
                messages=messages,
                timeout=self.timeout,
                temperature=0.7,
                max_tokens=1000,
                purpose="对话回复"
            )
            
            # 调用OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                timeout=self.timeout,
                temperature=0.7,
                max_tokens=1000
            )
            
            response_content = response.choices[0].message.content
            generation_time = time.time() - start_time
            
            # 记录使用信息
            usage_info = None
            if hasattr(response, 'usage'):
                usage_info = {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            
            self.logger.log_ai_response(
                response_content=response_content,
                usage_info=usage_info,
                duration=generation_time
            )
            
            return response_content
            
        except Exception as e:
            self.logger.log_error_with_context(e, "AI回复生成", {
                "personality_id": personality_id,
                "input_preview": user_input[:200],
                "model": self.model
            })
            return f"抱歉，我现在遇到了一些技术问题，无法正常回复。错误信息: {str(e)}"
    
    def _build_ai_context(self, user_input: str, memories: List[MemoryItem], personality: Dict) -> str:
        """为AI构建上下文信息"""
        self.logger.debug("构建AI上下文", {
            "personality_name": personality.get('name', '未知'),
            "memory_count": len(memories)
        })
        
        context_parts = []
        
        # 添加人格信息
        if personality:
            context_parts.append(f"人格名称: {personality.get('name', '未知')}")
            context_parts.append(f"人格特征: {', '.join(personality.get('personality_traits', []))}")
            context_parts.append(f"回复风格: {personality.get('response_style', '友好')}")
            
            if personality.get('background'):
                context_parts.append(f"背景描述: {personality['background']}")
        
        # 添加相关记忆
        if memories:
            memory_texts = []
            for memory in memories[:8]:  # 限制记忆数量
                memory_texts.append(f"- {memory.content} (类别: {memory.category}, 重要性: {memory.importance})")
            context_parts.append(f"相关记忆:\n{chr(10).join(memory_texts)}")
        
        context = "\n\n".join(context_parts)
        self.logger.debug("AI上下文构建完成", {
            "context_length": len(context),
            "context_preview": context[:300] + "..." if len(context) > 300 else context
        })
        
        return context
    
    def _build_conversation_history(self) -> List[Dict]:
        """构建对话历史"""
        messages = []
        
        # 获取最近的对话历史（最多10轮对话）
        recent_messages = self.chat_history[-20:]  # 20条消息约等于10轮对话
        
        for msg in recent_messages:
            if msg.sender == "user":
                messages.append({"role": "user", "content": msg.content})
            elif msg.sender == "ai":
                messages.append({"role": "assistant", "content": msg.content})
            # 跳过system消息
        
        self.logger.debug("对话历史构建完成", {
            "total_history_count": len(self.chat_history),
            "used_history_count": len(messages)
        })
        
        return messages
    
    def get_chat_history(self) -> List[ChatMessage]:
        """获取聊天历史"""
        return self.chat_history.copy()
    
    def clear_chat_history(self):
        """清空聊天历史"""
        old_count = len(self.chat_history)
        
        self.logger.info("开始清空聊天历史", {
            "current_count": old_count
        })
        
        # 在清空前提取所有对话的记忆
        if old_count > 0:
            self.logger.info("在清空前提取所有对话记忆", {
                "total_conversations": old_count
            })
            self._extract_memories_from_conversations(self.chat_history)
        
        # 清空聊天历史
        self.chat_history.clear()
        
        self.logger.info("聊天历史已清空", {
            "cleared_count": old_count,
            "extracted_memories": old_count > 0
        })
    
    def switch_personality(self, personality_id: str) -> bool:
        """切换人格"""
        current_personality = self.personality_manager.get_current_personality()
        current_name = current_personality.get('name', '未知') if current_personality else '无'
        
        self.logger.info(f"尝试切换人格: {current_name} -> {personality_id}")
        
        success = self.personality_manager.set_personality(personality_id)
        
        if success:
            # 添加系统消息
            personality = self.personality_manager.get_current_personality()
            if personality:
                system_msg = f"已切换到{personality['name']}人格"
                self.chat_history.append(ChatMessage(system_msg, "system"))
                
                self.logger.log_personality_switch(current_name, personality['name'], True)
        else:
            self.logger.log_personality_switch(current_name, personality_id, False)
            
        return success
    
    def get_current_personality_info(self) -> Optional[Dict]:
        """获取当前人格信息"""
        return self.personality_manager.get_current_personality()
    
    def get_memory_summary(self) -> Dict:
        """获取记忆摘要"""
        personality_id = self.personality_manager.get_current_personality_id()
        if personality_id:
            summary = self.memory_manager.get_memory_summary(personality_id)
            self.logger.debug("记忆摘要获取完成", {
                "personality_id": personality_id,
                "summary": summary
            })
            return summary
        return {'total_count': 0, 'category_stats': {}, 'recent_memories': []}