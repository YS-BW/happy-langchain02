# Chat RAG Project

一个基于 LangChain 构建的 Retrieval-Augmented Generation (RAG) 聊天应用，结合了检索增强生成技术和智能代理(Agent)能力。

## 项目特点

- **RAG 检索增强生成**: 利用向量数据库检索相关文档，提高回答准确性
- **智能代理系统**: 集成工具调用能力，能够根据问题类型选择合适的处理方式
- **流式响应**: 支持流式输出，提供更好的用户体验
- **前后端分离**: FastAPI 后端 + HTML/JavaScript 前端
- **模块化设计**: 清晰的代码结构，便于扩展和维护

## 技术栈

### 后端
- Python 3.8+
- FastAPI - 高性能 Web 框架
- LangChain - 构建语言模型应用的框架
- LangChain-Ollama - Ollama 集成
- ChromaDB - 向量数据库
- Pydantic - 数据验证
- Uvicorn - ASGI 服务器

### 前端
- HTML/CSS/JavaScript
- Tailwind CSS - 样式框架
- Fetch API - 与后端通信

## 项目结构

```
chat-rag-project/
├── app/
│   ├── api/          # API 路由
│   ├── chains/       # LangChain 链逻辑
│   ├── models/       # 数据模型
│   └── rag/          # RAG 设置
├── rag_docs/         # RAG 文档资料
├── requirements.txt  # 依赖包
└── run.py           # 应用入口
front/
├── index.html       # 前端页面
└── script.js        # 前端脚本
```

## 快速开始

### 环境要求

- Python 3.8 或更高版本
- Ollama (用于本地运行大语言模型)
- Node.js (可选，用于前端开发)

### 安装步骤

1. 克隆项目仓库：
```bash
git clone <repository-url>
cd chat-rag-project
```

2. 创建虚拟环境并激活：
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置环境变量（可选）：
创建 `.env` 文件并设置以下变量：
```env
OLLAMA_CHAT_MODEL_NAME=qwen2.5:1.5b
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_TEMPERATURE=0.7
APP_NAME=Chat RAG API
```

5. 准备 RAG 文档：
将您的文档放入 `rag_docs/` 目录，支持 PDF、TXT 等格式。

6. 启动应用：
```bash
python run.py
```

默认情况下，后端将在 `http://localhost:8000` 上运行。

### 启动前端

直接打开 `front/index.html` 文件即可访问前端界面，确保后端服务正在运行。

## API 接口

### POST /chat-stream

流式聊天接口

**请求体：**
```json
{
  "question": "你的问题"
}
```

**响应：**
流式文本响应

## 自定义配置

### 更换大语言模型

通过修改环境变量 `OLLAMA_CHAT_MODEL_NAME` 来更换 Ollama 提供的模型。

### 调整检索参数

可以在 [rag.py](chat-rag-project/app/chains/rag.py) 中调整检索器参数，如检索文档数量等。

## 扩展功能

1. 添加新的工具函数到 Agent
2. 集成更多类型的文档解析器
3. 添加对话历史管理
4. 实现用户认证和权限控制

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。