# AI 智能体应用平台 (AI Agent Application Platform)

## 项目介绍 (Project Introduction)



This is an AI agent application platform built based on the ReAct pattern, integrating multiple AI capabilities including Retrieval-Augmented Generation (RAG), multi-model dialogue, multi-turn conversation memory, and autonomous planning. The platform provides a user-friendly frontend interface, supporting services such as AI Travel Advisor and all-capable AI Super Agent.

这是一个基于 ReAct 模式构建的 AI 智能体应用平台，集成了多种人工智能能力，包括文档检索增强生成（RAG）、多模型对话、多轮对话记忆及自主规划等功能。平台提供了用户友好的前端界面，支持 AI 旅游助手和全能型 AI 超级智能体等服务。

## 功能特点 (Features)

- **RAG 文档处理**：基于旅游知识库，实现文档切片、语义向量转换及 PostgreSQL 存储
- **模型集成**：通过 SpringAI 集成通义千问和 DeepSeek 模型，优化提示词处理
- **多轮对话**：利用 ChatMemory 和拦截器实现对话上下文记忆，支持历史对话持久化
- **智能体构建**：基于 OpenManus 的 ReAct 模式，开发在线搜索、PDF 生成等工具
- **前端交互**：使用 Vue 3 构建响应式界面，通过 SSE 实现流式对话体验
- **容器化部署**：提供 Dockerfile 支持项目容器化，Nginx 解决跨域问题

- **RAG Document Processing**: Based on tourism knowledge base, implementing document slicing, semantic vector conversion, and PostgreSQL storage
- **Model Integration**: Integrating Tongyi Qianwen and DeepSeek models via SpringAI, optimizing prompt processing
- **Multi-turn Dialogue**: Implementing conversation context memory using ChatMemory and interceptors, supporting persistent historical dialogues
- **Agent Construction**: Developing tools like online search and PDF generation based on OpenManus's ReAct mode
- **Frontend Interaction**: Building responsive interface with Vue 3, implementing streaming dialogue via SSE
- **Containerized Deployment**: Providing Dockerfile for containerization, using Nginx to solve cross-domain issues

## 技术栈 (Technology Stack)

### 后端 (Backend)
- Java 21
- Spring Boot 3.4.7
- SpringAI
- PostgreSQL (向量数据库)
- Kryo (序列化)
- Maven

### 前端 (Frontend)
- Vue 3
- Vite 4
- Vue Router 4
- Axios
- npm 7+ / Node.js 16+

## 快速开始 (Quick Start)

### 环境要求 (Environment Requirements)
- JDK 21+
- Node.js >= 16.0.0
- npm >= 7.0.0
- PostgreSQL 12+

### 安装步骤 (Installation Steps)

1. 克隆仓库 (Clone the repository)
```bash
git clone https://github.com/Nian-Fu/Agent.git
cd Agent
```

2. 后端部署 (Backend deployment)
```bash
# 编译项目
mvn clean package

# 运行应用
java -jar target/Agent-0.0.1-SNAPSHOT.jar
```

3. 前端部署 (Frontend deployment)
```bash
cd agent-frontend
npm install
npm run dev
```

4. 访问应用 (Access the application)
   - 前端: http://localhost:5173
   - 后端 API: http://localhost:8123/api

## 项目结构 (Project Structure)

```
Agent/
├── src/                     # 后端源代码
│   ├── main/java/com/funian/agent/
│   │   ├── agent/           # 智能体核心实现
│   │   ├── rag/             # RAG 相关功能
│   │   ├── chatmemory/      # 对话记忆管理
│   │   ├── controller/      # API 控制器
│   │   └── app/             # 应用服务
│   └── resources/           # 配置和资源文件
├── agent-frontend/          # 前端代码
│   ├── src/
│   │   ├── api/             # API 调用
│   │   ├── router/          # 路由配置
│   │   └── components/      #  Vue 组件
│   └── package.json         # 前端依赖
└── pom.xml                  # 后端依赖
```

## 核心功能实现 (Core Function Implementation)

1. **智能体架构**：基于 ReAct 模式实现思考-行动循环，支持工具调用和自主规划
2. **RAG 流程**：加载 Markdown 文档，提取元数据，转换为向量存储于数据库
3. **对话记忆**：使用 Kryo 序列化实现基于文件的对话历史持久化
4. **流式通信**：通过 SSE (Server-Sent Events) 实现实时对话反馈

1. **Agent Architecture**: Implementing thought-action cycle based on ReAct pattern, supporting tool calls and autonomous planning
2. **RAG Process**: Loading Markdown documents, extracting metadata, converting to vectors stored in database
3. **Conversation Memory**: Using Kryo serialization for file-based conversation history persistence
4. **Streaming Communication**: Implementing real-time dialogue feedback via SSE (Server-Sent Events)

## 许可证 (License)

本项目采用 MIT 许可证开源 - 详情参见 LICENSE 文件

This project is open-sourced under the MIT License - see the LICENSE file for details.
