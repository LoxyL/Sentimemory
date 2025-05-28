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


class MemoryItem:
    """记忆项"""
    
    def __init__(self, content: str, category: str = "general", 
                 importance: int = 1, timestamp: str = None):
        self.content = content
        self.category = category
        self.importance = importance  # 1-5, 5最重要
        self.timestamp = timestamp or datetime.now().isoformat()
        self.id = None
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'id': self.id,
            'content': self.content,
            'category': self.category,
            'importance': self.importance,
            'timestamp': self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'MemoryItem':
        """从字典创建记忆项"""
        item = cls(
            content=data['content'],
            category=data.get('category', 'general'),
            importance=data.get('importance', 1),
            timestamp=data.get('timestamp')
        )
        item.id = data.get('id')
        return item


class MemoryManager:
    """记忆管理器"""
    
    def __init__(self, data_dir: str = None):
        if data_dir is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_dir = os.path.join(current_dir, '..', '..', 'data', 'memories')
        
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        
        # 初始化数据库
        self.db_path = os.path.join(self.data_dir, 'memories.db')
        self.init_database()
    
    def init_database(self):
        """初始化数据库"""
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
    
    def add_memory(self, personality_id: str, memory_item: MemoryItem) -> bool:
        """添加记忆"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO memories (personality_id, content, category, importance, timestamp)
                VALUES (?, ?, ?, ?, ?)
            ''', (personality_id, memory_item.content, memory_item.category, 
                  memory_item.importance, memory_item.timestamp))
            
            memory_item.id = cursor.lastrowid
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"添加记忆失败: {e}")
            return False
    
    def get_memories(self, personality_id: str, limit: int = 50) -> List[MemoryItem]:
        """获取记忆列表"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, content, category, importance, timestamp
                FROM memories 
                WHERE personality_id = ?
                ORDER BY importance DESC, timestamp DESC
                LIMIT ?
            ''', (personality_id, limit))
            
            memories = []
            for row in cursor.fetchall():
                memory = MemoryItem(
                    content=row[1],
                    category=row[2],
                    importance=row[3],
                    timestamp=row[4]
                )
                memory.id = row[0]
                memories.append(memory)
            
            conn.close()
            return memories
        except Exception as e:
            print(f"获取记忆失败: {e}")
            return []
    
    def update_memory(self, memory_id: int, content: str = None, 
                     category: str = None, importance: int = None) -> bool:
        """更新记忆"""
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
            
            if not updates:
                return False
            
            params.append(memory_id)
            query = f"UPDATE memories SET {', '.join(updates)} WHERE id = ?"
            
            cursor.execute(query, params)
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"更新记忆失败: {e}")
            return False
    
    def delete_memory(self, memory_id: int) -> bool:
        """删除记忆"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"删除记忆失败: {e}")
            return False
    
    def search_memories(self, personality_id: str, keyword: str) -> List[MemoryItem]:
        """搜索记忆"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, content, category, importance, timestamp
                FROM memories 
                WHERE personality_id = ? AND content LIKE ?
                ORDER BY importance DESC, timestamp DESC
            ''', (personality_id, f'%{keyword}%'))
            
            memories = []
            for row in cursor.fetchall():
                memory = MemoryItem(
                    content=row[1],
                    category=row[2],
                    importance=row[3],
                    timestamp=row[4]
                )
                memory.id = row[0]
                memories.append(memory)
            
            conn.close()
            return memories
        except Exception as e:
            print(f"搜索记忆失败: {e}")
            return []
    
    def extract_key_info(self, text: str, focus_areas: List[str] = None) -> List[MemoryItem]:
        """从文本中提取关键信息"""
        memories = []
        
        # 简单的关键信息提取规则
        patterns = {
            "个人信息": [
                r"我叫(.+?)(?:[，。]|$)",
                r"我是(.+?)(?:[，。]|$)",
                r"我的(.+?)是(.+?)(?:[，。]|$)"
            ],
            "喜好": [
                r"我喜欢(.+?)(?:[，。]|$)",
                r"我爱(.+?)(?:[，。]|$)",
                r"我最喜欢(.+?)(?:[，。]|$)"
            ],
            "情感": [
                r"我感到(.+?)(?:[，。]|$)",
                r"我觉得(.+?)(?:[，。]|$)",
                r"我很(.+?)(?:[，。]|$)"
            ],
            "重要事件": [
                r"今天(.+?)(?:[，。]|$)",
                r"昨天(.+?)(?:[，。]|$)",
                r"最近(.+?)(?:[，。]|$)"
            ]
        }
        
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
        
        return memories
    
    def get_memory_summary(self, personality_id: str) -> Dict[str, Any]:
        """获取记忆摘要"""
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
            
            return {
                'total_count': total_count,
                'category_stats': category_stats,
                'recent_memories': recent_memories
            }
        except Exception as e:
            print(f"获取记忆摘要失败: {e}")
            return {
                'total_count': 0,
                'category_stats': {},
                'recent_memories': []
            } 