# -*- coding: utf-8 -*-
"""
辅助函数工具
"""

import os
import json
import re
from datetime import datetime
from typing import List, Dict, Any, Optional


def ensure_dir_exists(dir_path: str) -> bool:
    """确保目录存在"""
    try:
        os.makedirs(dir_path, exist_ok=True)
        return True
    except Exception as e:
        print(f"创建目录失败: {e}")
        return False


def load_json_file(file_path: str, default: Any = None) -> Any:
    """加载JSON文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载JSON文件失败 {file_path}: {e}")
        return default


def save_json_file(file_path: str, data: Any) -> bool:
    """保存JSON文件"""
    try:
        # 确保目录存在
        dir_path = os.path.dirname(file_path)
        if dir_path:
            ensure_dir_exists(dir_path)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存JSON文件失败 {file_path}: {e}")
        return False


def format_timestamp(timestamp: str = None, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """格式化时间戳"""
    try:
        if timestamp:
            dt = datetime.fromisoformat(timestamp)
        else:
            dt = datetime.now()
        return dt.strftime(format_str)
    except Exception:
        return datetime.now().strftime(format_str)


def clean_text(text: str) -> str:
    """清理文本"""
    if not text:
        return ""
    
    # 移除多余的空白字符
    text = re.sub(r'\s+', ' ', text.strip())
    
    # 移除特殊字符（保留中文、英文、数字、常用标点）
    text = re.sub(r'[^\w\s\u4e00-\u9fff，。！？；：""''（）【】《》、]', '', text)
    
    return text


def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """提取关键词"""
    if not text:
        return []
    
    # 清理文本
    clean = clean_text(text)
    
    # 分词（简单的空格分割）
    words = clean.split()
    
    # 过滤停用词
    stop_words = {
        '我', '你', '他', '她', '它', '我们', '你们', '他们', '她们', '它们',
        '的', '了', '在', '是', '有', '和', '与', '或', '但', '因为', '所以',
        '这', '那', '这个', '那个', '这些', '那些', '什么', '怎么', '为什么',
        '很', '非常', '特别', '比较', '更', '最', '都', '也', '还', '就',
        '会', '能', '可以', '应该', '必须', '需要', '想要', '希望', '觉得',
        '一', '二', '三', '四', '五', '六', '七', '八', '九', '十'
    }
    
    # 过滤并统计词频
    word_count = {}
    for word in words:
        if len(word) > 1 and word not in stop_words:
            word_count[word] = word_count.get(word, 0) + 1
    
    # 按词频排序
    sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    
    # 返回前N个关键词
    return [word for word, count in sorted_words[:max_keywords]]


def calculate_text_similarity(text1: str, text2: str) -> float:
    """计算文本相似度（简单的词汇重叠度）"""
    if not text1 or not text2:
        return 0.0
    
    words1 = set(extract_keywords(text1, 20))
    words2 = set(extract_keywords(text2, 20))
    
    if not words1 or not words2:
        return 0.0
    
    # 计算Jaccard相似度
    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))
    
    return intersection / union if union > 0 else 0.0


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """截断文本"""
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def validate_memory_content(content: str) -> tuple[bool, str]:
    """验证记忆内容"""
    if not content or not content.strip():
        return False, "记忆内容不能为空"
    
    content = content.strip()
    
    if len(content) < 2:
        return False, "记忆内容太短"
    
    if len(content) > 1000:
        return False, "记忆内容太长（最多1000字符）"
    
    return True, ""


def format_memory_category(category: str) -> str:
    """格式化记忆类别"""
    category_map = {
        "personal": "个人信息",
        "preference": "喜好",
        "emotion": "情感",
        "event": "重要事件",
        "general": "一般",
        "个人信息": "个人信息",
        "喜好": "喜好", 
        "情感": "情感",
        "重要事件": "重要事件"
    }
    
    return category_map.get(category, "一般")


def get_personality_color(personality_id: str) -> str:
    """获取人格对应的颜色"""
    color_map = {
        "friendly": "#4CAF50",      # 绿色 - 友善
        "humorous": "#FF9800",      # 橙色 - 幽默
        "knowledgeable": "#2196F3", # 蓝色 - 知识
        "creative": "#9C27B0",      # 紫色 - 创意
        "calm": "#607D8B"           # 蓝灰色 - 沉稳
    }
    
    return color_map.get(personality_id, "#666666")


def format_file_size(size_bytes: int) -> str:
    """格式化文件大小"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def get_app_version() -> str:
    """获取应用版本"""
    return "1.0.0"


def get_system_info() -> Dict[str, str]:
    """获取系统信息"""
    import platform
    
    return {
        "platform": platform.system(),
        "platform_version": platform.version(),
        "python_version": platform.python_version(),
        "app_version": get_app_version()
    }


def get_system_font(size: int = 10, bold: bool = False) -> 'QFont':
    """获取系统兼容的中文字体"""
    try:
        from PyQt5.QtGui import QFont
        import platform
        
        # 根据操作系统选择合适的中文字体
        if platform.system() == "Darwin":  # macOS
            font_family = "PingFang SC"
        elif platform.system() == "Windows":
            font_family = "Microsoft YaHei"
        else:  # Linux
            font_family = "Noto Sans CJK SC"
        
        font = QFont(font_family, size)
        
        # 如果指定字体不存在，使用系统默认字体
        if not font.exactMatch():
            font = QFont()
            font.setPointSize(size)
        
        if bold:
            font.setBold(True)
        
        return font
    except ImportError:
        # 如果PyQt5不可用，返回None
        return None 