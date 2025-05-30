# -*- coding: utf-8 -*-
"""
AI记忆系统模块
"""

import json
import os
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Any
import re
from utils.logger import get_logger


class MemoryItem:
    """记忆项"""
    
    def __init__(self, content: str, category: str = "general", 
                 importance: int = 1, timestamp: str = None, tags: List[str] = None):
        self.content = content
        self.category = category
        self.importance = importance  # 1-5, 5最重要
        self.timestamp = timestamp or datetime.now().isoformat()
        self.tags = tags or []
        self.id = None
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'id': self.id,
            'content': self.content,
            'category': self.category,
            'importance': self.importance,
            'timestamp': self.timestamp,
            'tags': self.tags
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'MemoryItem':
        """从字典创建记忆项"""
        item = cls(
            content=data['content'],
            category=data.get('category', 'general'),
            importance=data.get('importance', 1),
            timestamp=data.get('timestamp'),
            tags=data.get('tags', [])
        )
        item.id = data.get('id')
        return item


class MemoryManager:
    """记忆管理器"""
    
    def __init__(self, data_dir: str = None):
        self.logger = get_logger("sentimemory.memory")
        self.logger.info("MemoryManager初始化开始")
        
        if data_dir is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_dir = os.path.join(current_dir, '..', '..', 'data', 'memories')
        
        self.data_dir = data_dir
        self.logger.debug("记忆数据目录", {"data_dir": data_dir})
        
        os.makedirs(self.data_dir, exist_ok=True)
        
        # 初始化数据库
        self.db_path = os.path.join(self.data_dir, 'memories.db')
        self.logger.debug("记忆数据库路径", {"db_path": self.db_path})
        
        self.init_database()
        self.logger.info("MemoryManager初始化完成")
    
    def init_database(self):
        """初始化数据库"""
        self.logger.debug("开始初始化记忆数据库")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 创建记忆表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    personality_id TEXT NOT NULL,
                    content TEXT NOT NULL,
                    category TEXT DEFAULT 'general',
                    importance INTEGER DEFAULT 1,
                    timestamp TEXT NOT NULL,
                    tags TEXT DEFAULT '[]',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建索引
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_personality_id 
                ON memories(personality_id)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_category 
                ON memories(category)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_importance 
                ON memories(importance)
            ''')
            
            conn.commit()
            conn.close()
            
            self.logger.info("记忆数据库初始化成功")
            
        except Exception as e:
            self.logger.log_error_with_context(e, "记忆数据库初始化", {
                "db_path": self.db_path
            })
    
    def add_memory(self, personality_id: str, memory_item: MemoryItem) -> bool:
        """添加记忆"""
        self.logger.debug("开始添加记忆", {
            "personality_id": personality_id,
            "content_length": len(memory_item.content),
            "category": memory_item.category,
            "importance": memory_item.importance,
            "tags": memory_item.tags
        })
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            tags_json = json.dumps(memory_item.tags, ensure_ascii=False)
            
            cursor.execute('''
                INSERT INTO memories (personality_id, content, category, importance, timestamp, tags)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (personality_id, memory_item.content, memory_item.category, 
                  memory_item.importance, memory_item.timestamp, tags_json))
            
            memory_item.id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            self.logger.info("记忆添加成功", {
                "memory_id": memory_item.id,
                "personality_id": personality_id,
                "content_preview": memory_item.content[:50] + "..." if len(memory_item.content) > 50 else memory_item.content
            })
            
            return True
            
        except Exception as e:
            self.logger.log_error_with_context(e, "添加记忆", {
                "personality_id": personality_id,
                "memory_data": memory_item.to_dict()
            })
            return False
    
    def get_memories(self, personality_id: str, limit: int = 50) -> List[MemoryItem]:
        """获取记忆列表"""
        self.logger.debug("开始获取记忆列表", {
            "personality_id": personality_id,
            "limit": limit
        })
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, content, category, importance, timestamp, tags
                FROM memories 
                WHERE personality_id = ?
                ORDER BY importance DESC, timestamp DESC
                LIMIT ?
            ''', (personality_id, limit))
            
            memories = []
            for row in cursor.fetchall():
                try:
                    tags = json.loads(row[5]) if row[5] else []
                except:
                    tags = []
                
                memory = MemoryItem(
                    content=row[1],
                    category=row[2],
                    importance=row[3],
                    timestamp=row[4],
                    tags=tags
                )
                memory.id = row[0]
                memories.append(memory)
            
            conn.close()
            
            self.logger.info("记忆列表获取成功", {
                "personality_id": personality_id,
                "returned_count": len(memories),
                "requested_limit": limit
            })
            
            return memories
            
        except Exception as e:
            self.logger.log_error_with_context(e, "获取记忆列表", {
                "personality_id": personality_id,
                "limit": limit
            })
            return []
    
    def update_memory(self, memory_id: int, content: str = None, 
                     category: str = None, importance: int = None, tags: List[str] = None) -> bool:
        """更新记忆"""
        self.logger.debug("开始更新记忆", {
            "memory_id": memory_id,
            "update_content": content is not None,
            "update_category": category is not None,
            "update_importance": importance is not None,
            "update_tags": tags is not None
        })
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            updates = []
            params = []
            
            if content is not None:
                updates.append("content = ?")
                params.append(content)
            if category is not None:
                updates.append("category = ?")
                params.append(category)
            if importance is not None:
                updates.append("importance = ?")
                params.append(importance)
            if tags is not None:
                updates.append("tags = ?")
                params.append(json.dumps(tags, ensure_ascii=False))
            
            if not updates:
                self.logger.warning("更新记忆失败：没有提供更新字段", {"memory_id": memory_id})
                return False
            
            params.append(memory_id)
            query = f"UPDATE memories SET {', '.join(updates)} WHERE id = ?"
            
            cursor.execute(query, params)
            affected_rows = cursor.rowcount
            conn.commit()
            conn.close()
            
            if affected_rows > 0:
                self.logger.info("记忆更新成功", {
                    "memory_id": memory_id,
                    "updated_fields": updates,
                    "affected_rows": affected_rows
                })
                return True
            else:
                self.logger.warning("记忆更新失败：记忆不存在", {"memory_id": memory_id})
                return False
                
        except Exception as e:
            self.logger.log_error_with_context(e, "更新记忆", {
                "memory_id": memory_id,
                "update_params": {
                    "content": content,
                    "category": category,
                    "importance": importance,
                    "tags": tags
                }
            })
            return False
    
    def delete_memory(self, memory_id: int) -> bool:
        """删除记忆"""
        self.logger.debug("开始删除记忆", {"memory_id": memory_id})
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
            affected_rows = cursor.rowcount
            conn.commit()
            conn.close()
            
            if affected_rows > 0:
                self.logger.info("记忆删除成功", {
                    "memory_id": memory_id,
                    "affected_rows": affected_rows
                })
                return True
            else:
                self.logger.warning("记忆删除失败：记忆不存在", {"memory_id": memory_id})
                return False
                
        except Exception as e:
            self.logger.log_error_with_context(e, "删除记忆", {"memory_id": memory_id})
            return False
    
    def search_memories(self, personality_id: str, keyword: str) -> List[MemoryItem]:
        """搜索记忆"""
        self.logger.debug("开始搜索记忆", {
            "personality_id": personality_id,
            "keyword": keyword
        })
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, content, category, importance, timestamp, tags
                FROM memories 
                WHERE personality_id = ? AND content LIKE ?
                ORDER BY importance DESC, timestamp DESC
            ''', (personality_id, f'%{keyword}%'))
            
            memories = []
            for row in cursor.fetchall():
                try:
                    tags = json.loads(row[5]) if row[5] else []
                except:
                    tags = []
                
                memory = MemoryItem(
                    content=row[1],
                    category=row[2],
                    importance=row[3],
                    timestamp=row[4],
                    tags=tags
                )
                memory.id = row[0]
                memories.append(memory)
            
            conn.close()
            
            self.logger.info("记忆搜索完成", {
                "personality_id": personality_id,
                "keyword": keyword,
                "found_count": len(memories)
            })
            
            return memories
            
        except Exception as e:
            self.logger.log_error_with_context(e, "搜索记忆", {
                "personality_id": personality_id,
                "keyword": keyword
            })
            return []
    
    def extract_key_info(self, text: str, focus_areas: List[str] = None) -> List[MemoryItem]:
        """从文本中提取关键信息"""
        self.logger.debug("开始提取关键信息", {
            "text_length": len(text),
            "focus_areas": focus_areas
        })
        
        memories = []
        
        # 简单的关键信息提取规则
        patterns = {
            "personal": [
                r"我叫(.+?)(?:[，。]|$)",
                r"我是(.+?)(?:[，。]|$)",
                r"我的(.+?)是(.+?)(?:[，。]|$)"
            ],
            "preference": [
                r"我喜欢(.+?)(?:[，。]|$)",
                r"我爱(.+?)(?:[，。]|$)",
                r"我最喜欢(.+?)(?:[，。]|$)"
            ],
            "emotion": [
                r"我感到(.+?)(?:[，。]|$)",
                r"我觉得(.+?)(?:[，。]|$)",
                r"我很(.+?)(?:[，。]|$)"
            ],
            "event": [
                r"今天(.+?)(?:[，。]|$)",
                r"昨天(.+?)(?:[，。]|$)",
                r"最近(.+?)(?:[，。]|$)"
            ]
        }
        
        extracted_count = 0
        for category, pattern_list in patterns.items():
            for pattern in pattern_list:
                matches = re.findall(pattern, text)
                for match in matches:
                    if isinstance(match, tuple):
                        content = " ".join(match)
                    else:
                        content = match
                    
                    if content.strip():
                        memory = MemoryItem(
                            content=content.strip(),
                            category=category,
                            importance=2  # 默认重要性
                        )
                        memories.append(memory)
                        extracted_count += 1
        
        self.logger.info("关键信息提取完成", {
            "text_length": len(text),
            "extracted_count": extracted_count,
            "categories": list(set(m.category for m in memories))
        })
        
        return memories
    
    def get_memory_summary(self, personality_id: str) -> Dict[str, Any]:
        """获取记忆摘要"""
        self.logger.debug("开始获取记忆摘要", {"personality_id": personality_id})
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 总记忆数
            cursor.execute(
                "SELECT COUNT(*) FROM memories WHERE personality_id = ?",
                (personality_id,)
            )
            total_count = cursor.fetchone()[0]
            
            # 按类别统计
            cursor.execute('''
                SELECT category, COUNT(*) 
                FROM memories 
                WHERE personality_id = ?
                GROUP BY category
            ''', (personality_id,))
            category_stats = dict(cursor.fetchall())
            
            # 最近记忆
            cursor.execute('''
                SELECT content, timestamp
                FROM memories 
                WHERE personality_id = ?
                ORDER BY timestamp DESC
                LIMIT 5
            ''', (personality_id,))
            recent_memories = cursor.fetchall()
            
            conn.close()
            
            summary = {
                'total_count': total_count,
                'category_stats': category_stats,
                'recent_memories': recent_memories
            }
            
            self.logger.info("记忆摘要获取成功", {
                "personality_id": personality_id,
                "total_count": total_count,
                "categories": list(category_stats.keys()),
                "recent_count": len(recent_memories)
            })
            
            return summary
            
        except Exception as e:
            self.logger.log_error_with_context(e, "获取记忆摘要", {
                "personality_id": personality_id
            })
            return {
                'total_count': 0,
                'category_stats': {},
                'recent_memories': []
            } 