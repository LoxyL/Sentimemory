# -*- coding: utf-8 -*-
"""
记忆系统测试
"""

import unittest
import tempfile
import os
import sys

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ai.memory import MemoryManager, MemoryItem


class TestMemorySystem(unittest.TestCase):
    """记忆系统测试类"""
    
    def setUp(self):
        """测试前准备"""
        # 创建临时目录
        self.temp_dir = tempfile.mkdtemp()
        self.memory_manager = MemoryManager(self.temp_dir)
        self.test_personality_id = "test_personality"
    
    def tearDown(self):
        """测试后清理"""
        # 清理临时文件
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_add_memory(self):
        """测试添加记忆"""
        memory_item = MemoryItem(
            content="测试记忆内容",
            category="测试",
            importance=3
        )
        
        success = self.memory_manager.add_memory(self.test_personality_id, memory_item)
        self.assertTrue(success)
        self.assertIsNotNone(memory_item.id)
    
    def test_get_memories(self):
        """测试获取记忆"""
        # 添加几条记忆
        for i in range(3):
            memory_item = MemoryItem(
                content=f"测试记忆{i}",
                category="测试",
                importance=i + 1
            )
            self.memory_manager.add_memory(self.test_personality_id, memory_item)
        
        # 获取记忆
        memories = self.memory_manager.get_memories(self.test_personality_id)
        self.assertEqual(len(memories), 3)
        
        # 验证按重要性排序
        self.assertEqual(memories[0].importance, 3)
        self.assertEqual(memories[1].importance, 2)
        self.assertEqual(memories[2].importance, 1)
    
    def test_update_memory(self):
        """测试更新记忆"""
        memory_item = MemoryItem(
            content="原始内容",
            category="测试",
            importance=1
        )
        
        self.memory_manager.add_memory(self.test_personality_id, memory_item)
        
        # 更新记忆
        success = self.memory_manager.update_memory(
            memory_item.id,
            content="更新后的内容",
            importance=5
        )
        self.assertTrue(success)
        
        # 验证更新
        memories = self.memory_manager.get_memories(self.test_personality_id)
        self.assertEqual(memories[0].content, "更新后的内容")
        self.assertEqual(memories[0].importance, 5)
    
    def test_delete_memory(self):
        """测试删除记忆"""
        memory_item = MemoryItem(
            content="要删除的记忆",
            category="测试",
            importance=1
        )
        
        self.memory_manager.add_memory(self.test_personality_id, memory_item)
        
        # 删除记忆
        success = self.memory_manager.delete_memory(memory_item.id)
        self.assertTrue(success)
        
        # 验证删除
        memories = self.memory_manager.get_memories(self.test_personality_id)
        self.assertEqual(len(memories), 0)
    
    def test_search_memories(self):
        """测试搜索记忆"""
        # 添加测试数据
        test_memories = [
            MemoryItem("我喜欢吃苹果", "喜好", 2),
            MemoryItem("我讨厌下雨天", "情感", 1),
            MemoryItem("苹果很好吃", "喜好", 3)
        ]
        
        for memory in test_memories:
            self.memory_manager.add_memory(self.test_personality_id, memory)
        
        # 搜索包含"苹果"的记忆
        results = self.memory_manager.search_memories(self.test_personality_id, "苹果")
        self.assertEqual(len(results), 2)
        
        # 搜索不存在的内容
        results = self.memory_manager.search_memories(self.test_personality_id, "不存在")
        self.assertEqual(len(results), 0)
    
    def test_extract_key_info(self):
        """测试关键信息提取"""
        text = "我叫张三，我喜欢打篮球，今天心情很好。"
        
        memories = self.memory_manager.extract_key_info(text)
        
        # 验证提取的信息
        self.assertGreater(len(memories), 0)
        
        # 检查是否包含个人信息
        personal_info = [m for m in memories if m.category == "个人信息"]
        self.assertGreater(len(personal_info), 0)
    
    def test_memory_summary(self):
        """测试记忆摘要"""
        # 添加不同类别的记忆
        categories = ["个人信息", "喜好", "情感"]
        for i, category in enumerate(categories):
            for j in range(i + 1):  # 不同数量
                memory_item = MemoryItem(
                    content=f"{category}记忆{j}",
                    category=category,
                    importance=1
                )
                self.memory_manager.add_memory(self.test_personality_id, memory_item)
        
        # 获取摘要
        summary = self.memory_manager.get_memory_summary(self.test_personality_id)
        
        self.assertEqual(summary['total_count'], 6)  # 1+2+3=6
        self.assertEqual(len(summary['category_stats']), 3)
        self.assertEqual(summary['category_stats']['个人信息'], 1)
        self.assertEqual(summary['category_stats']['喜好'], 2)
        self.assertEqual(summary['category_stats']['情感'], 3)


if __name__ == '__main__':
    unittest.main() 