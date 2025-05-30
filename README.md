# Sentimemory - AI聊天工具

## 项目简介
Sentimemory是一款基于Python开发的智能AI聊天工具，通过情感化的互动和记忆功能，为用户创建个性化的对话体验。程序采用PyQt5实现现代化的可视化界面，支持多种人格模式和智能记忆管理。

## 功能特性
- **智能对话**: 基于OpenAI API的自然语言对话
- **多重人格**: 5种预设人格（友善型、幽默型、知识型、创意型、沉稳型）
- **智能记忆**: AI能够记录、存储和检索关键对话信息
- **记忆管理**: 可视化查看、编辑和管理AI记忆内容
- **现代界面**: 基于PyQt5的直观用户界面，支持高DPI显示
- **日志系统**: 完整的日志记录和错误追踪
- **配置管理**: 灵活的应用设置和人格配置

## 项目结构
```
Sentimemory/
├── main.py                 # 主程序入口
├── requirements.txt        # 依赖包列表
├── .gitignore             # Git忽略文件
├── config/                 # 配置文件
│   ├── __init__.py
│   ├── settings.py         # 应用设置管理
│   ├── app_settings.json   # 应用配置文件
│   └── personalities.json  # 人格配置文件
├── src/                    # 源代码
│   ├── __init__.py
│   ├── ai/                 # AI相关模块
│   │   ├── __init__.py
│   │   ├── chat_engine.py  # 聊天引擎核心
│   │   ├── personality.py  # 人格管理系统
│   │   └── memory.py       # 记忆系统
│   ├── ui/                 # 用户界面
│   │   ├── __init__.py
│   │   ├── main_window.py  # 主窗口界面
│   │   ├── chat_widget.py  # 聊天界面组件
│   │   ├── memory_widget.py # 记忆管理界面
│   │   └── personality_widget.py # 人格选择界面
│   └── utils/              # 工具模块
│       ├── __init__.py
│       ├── logger.py       # 日志系统
│       └── helpers.py      # 辅助函数
├── data/                   # 数据文件
│   └── memories/           # 记忆数据存储
├── log/                    # 日志文件
└── tests/                  # 测试文件
    ├── __init__.py
    ├── test_memory.py      # 记忆系统测试
    └── test_logging.py     # 日志系统测试
```

## 安装和运行

### 环境要求
- Python 3.8+
- OpenAI API密钥

### 安装步骤
1. 克隆项目到本地
   ```bash
   git clone <repository-url>
   cd Sentimemory
   ```

2. 安装依赖包
   ```bash
   pip install -r requirements.txt
   ```

3. 配置OpenAI API密钥
   - 创建`.env`文件或在系统环境变量中设置`OPENAI_API_KEY`

4. 运行程序
   ```bash
   python main.py
   ```

## 依赖包
- **PyQt5** (>=5.12.0): GUI框架
- **openai** (>=1.0.0): OpenAI API客户端
- **requests** (>=2.25.0): HTTP请求库
- **json5** (>=0.9.0): JSON5格式支持
- **python-dotenv** (>=0.19.0): 环境变量管理
- **typing-extensions** (>=4.0.0): 类型注解扩展

## 人格类型
- **友善型**: 温和友善，善于倾听和安慰
- **幽默型**: 风趣幽默，善于调节气氛
- **知识型**: 博学多才，善于分析和解答
- **创意型**: 富有想象力，善于创新思考
- **沉稳型**: 冷静理性，善于深度思考

## 开发和测试
项目包含完整的测试套件，可以运行以下命令进行测试：
```bash
python -m pytest tests/
```

## 贡献
欢迎提交Issue和Pull Request来改进项目。请确保：
1. 代码符合项目的编码规范
2. 添加适当的测试用例
3. 更新相关文档
