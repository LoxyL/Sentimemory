# -*- coding: utf-8 -*-
"""
工具模块

这个包包含了项目中使用的各种辅助函数和工具：
- 文件操作工具
- 文本处理工具
- 时间格式化工具
- 数据验证工具
"""

# 导入常用的工具函数
from .helpers import (
    ensure_dir_exists,
    load_json_file,
    save_json_file,
    format_timestamp,
    clean_text,
    extract_keywords,
    calculate_text_similarity,
    truncate_text,
    validate_memory_content,
    format_memory_category,
    get_personality_color,
    format_file_size,
    get_app_version,
    get_system_info
)

# 定义包的公开接口
__all__ = [
    'ensure_dir_exists',
    'load_json_file', 
    'save_json_file',
    'format_timestamp',
    'clean_text',
    'extract_keywords',
    'calculate_text_similarity',
    'truncate_text',
    'validate_memory_content',
    'format_memory_category',
    'get_personality_color',
    'format_file_size',
    'get_app_version',
    'get_system_info'
] 