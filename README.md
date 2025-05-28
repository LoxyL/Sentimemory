# Sentimemory - AI聊天工具

## 项目简介
Sentimemory是一款基于Python开发的简易AI聊天工具，能够通过情感化的互动和记忆功能，为用户创建个性化的对话体验。程序通过Python + PyQt实现可视化页面，为用户提供友好的交互界面。

## 功能特性
- **单轮对话**: 与AI进行自然的聊天交流
- **人格选择**: 多个预设人格（友善型、幽默型、知识型等）
- **记忆库系统**: AI能够记录和提取关键信息
- **记忆管理**: 可视化查看和编辑AI记忆内容
- **可视化界面**: 基于PyQt的直观用户界面

## 项目结构
```
Sentimemory/
├── main.py                 # 主程序入口
├── requirements.txt        # 依赖包列表
├── config/                 # 配置文件
│   ├── __init__.py
│   ├── settings.py         # 应用设置
│   └── personalities.json  # 人格配置
├── src/                    # 源代码
│   ├── __init__.py
│   ├── ai/                 # AI相关模块
│   │   ├── __init__.py
│   │   ├── chat_engine.py  # 聊天引擎
│   │   ├── personality.py  # 人格管理
│   │   └── memory.py       # 记忆系统
│   ├── ui/                 # 用户界面
│   │   ├── __init__.py
│   │   ├── main_window.py  # 主窗口
│   │   ├── chat_widget.py  # 聊天界面
│   │   ├── memory_widget.py # 记忆管理界面
│   │   └── personality_widget.py # 人格选择界面
│   └── utils/              # 工具模块
│       ├── __init__.py
│       ├── database.py     # 数据库操作
│       └── helpers.py      # 辅助函数
├── data/                   # 数据文件
│   ├── memories/           # 记忆数据
│   └── chat_history/       # 聊天记录
├── assets/                 # 资源文件
│   ├── icons/              # 图标
│   └── styles/             # 样式文件
└── tests/                  # 测试文件
    ├── __init__.py
    └── test_*.py
```

## 安装和运行
1. 克隆项目到本地
2. 安装依赖: `pip install -r requirements.txt`
3. 运行程序: `python main.py`

## 开发环境
- Python 3.8+
- PyQt5/PyQt6
- 其他依赖见requirements.txt

## 贡献
欢迎提交Issue和Pull Request来改进项目。
