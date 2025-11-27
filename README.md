# 🌍 智能旅行助手 - 多智能体旅行规划平台

> 针对旅游信息滞后、大模型幻觉等痛点，基于旅游知识库构建具备智能问答与自主规划的助手

[![GitHub](https://img.shields.io/badge/GitHub-Agent-blue)](https://github.com/Nian-Fu/Agent)
[![Demo](https://img.shields.io/badge/Demo-Experience-green)](https://uiagent-171000-8-1367279107.sh.run.tcloudbase.com)

基于 LangChain、LangGraph、FastAPI 和通义千问模型的智能旅行助手平台，通过Serverless云部署。

## 📋 项目简介

本项目是一个完整的多智能体旅行服务平台，遵循单一职责原则，通过 8 个专业化智能体协同工作，为用户提供全方位的旅行服务。

### 🎯 核心特性

- 🤖 **8个专业智能体**：意图识别、机票查询、酒店预订、景点推荐等全流程服务
- 🔄 **LangGraph工作流**：智能路由和状态管理，支持复杂业务流程编排
- 🚀 **FastAPI服务**：高性能异步API，响应时间≤300ms
- 🧠 **通义千问驱动**：DashScope API，强大的自然语言理解能力
- 💾 **数据持久化**：SQLite/PostgreSQL存储，支持对话历史和用户偏好
- 📊 **实时日志**：完整的操作追踪和性能监控
- 🔧 **MCP工具集成**：支持高德地图等外部工具调用
- 🌐 **Serverless部署**：云原生架构，弹性伸缩

## 🏗️ 系统架构

### 🛠️ 技术栈

| 组件 | 版本 | 说明 |
|------|------|------|
| **核心框架** | | |
| Python | 3.10+ | 核心开发语言 |
| LangChain | 0.2.x | 智能体框架，Agent编排 |
| LangGraph | 0.1.x | 工作流编排，状态管理 |
| FastAPI | 0.104+ | 高性能Web服务框架 |
| **AI模型** | | |
| 通义千问 (DashScope) | qwen-turbo/plus/max | 大语言模型，意图理解与生成 |
| **数据存储** | | |
| SQLite/PostgreSQL | 3.37+/13+ | 数据持久化，支持切换 |
| ChatMemory | - | 对话上下文管理 |
| **工具集成** | | |
| MCP (Model Context Protocol) | - | 工具调用协议 |
| 高德地图 API | - | 地理位置服务 |
| **部署** | | |
| Conda | - | Python环境管理 |
| Serverless | - | 云原生部署（可选）|

### ✨ 项目亮点

#### 1️⃣ 知识库构建与RAG检索
- 📚 **私有文档处理**：读取并切片旅游相关文档
- 🔍 **语义向量化**：使用嵌入模型转换文本为向量
- 💾 **向量存储**：PostgreSQL存储，支持相似度搜索
- ⚡ **快速检索**：信息检索响应时间≤300ms
- 🎯 **查询优化**：查询重写器与检索增强器，优化问答过程

#### 2️⃣ 对话持久化机制
- 💬 **ChatMemory**：基于会话上下文机制
- 🔄 **拦截器设计**：捕获对话流程关键节点
- 📦 **序列化存储**：Kryo序列化库实现消息转换
- 🗃️ **持久化支持**：对话历史和用户偏好长期保存

#### 3️⃣ 多智能体协同编排
- 🤖 **8个专业智能体**：各司其职，协同工作
- 🔀 **LangGraph编排**：智能路由和条件分支
- 🔧 **工具集成**：MCP协议调用外部API
- 🎨 **Prompt工程**：精心设计的提示词模板

### 🤖 8个专业智能体架构

```
┌─────────────────────────────────────────────────────────┐
│                   用户查询入口                           │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│  1. 意图解析智能体 (Intent Parse Agent)                  │
│  职责：识别机票/酒店/行程/景点/价格/预订/客服等意图      │
│  技术：Prompt工程 + 通义千问 + 结构化输出               │
└─────────────────┬───────────────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
┌───────────────┐   ┌───────────────┐
│ 2. 机票查询   │   │ 3. 酒店查询   │
│ Flight Agent  │   │ Hotel Agent   │
│ Tool调用+数据 │   │ 筛选+价格对比 │
└───────┬───────┘   └───────┬───────┘
        │                   │
        └─────────┬─────────┘
                  ▼
        ┌───────────────────┐
        │ 4. 景点推荐        │
        │ Attraction Agent  │
        │ RAG检索+偏好匹配  │
        └─────────┬─────────┘
                  │
                  ▼
        ┌───────────────────┐
        │ 5. 行程规划        │
        │ Itinerary Agent   │
        │ 整合多源数据      │
        └───────────────────┘

        ┌───────────────────┐
        │ 6. 价格对比        │
        │ Price Agent       │
        │ 跨平台比价        │
        └───────────────────┘

        ┌───────────────────┐
        │ 7. 预订执行        │
        │ Booking Agent     │
        │ 订单创建+确认     │
        └───────────────────┘

        ┌───────────────────┐
        │ 8. 客服咨询        │
        │ Service Agent     │
        │ 智能客服+FAQ      │
        └───────────────────┘
```

## 📦 项目结构

```
LangChain-agent/
├── agents/                         # 🤖 智能体模块
│   ├── __init__.py                # 智能体导出
│   ├── base_agent.py              # 智能体基类（抽象模板）
│   ├── intent_agent.py            # 意图解析智能体
│   ├── flight_agent.py            # 机票查询智能体
│   ├── hotel_agent.py             # 酒店查询智能体
│   ├── attraction_agent.py        # 景点推荐智能体
│   ├── itinerary_agent.py         # 行程规划智能体
│   ├── price_agent.py             # 价格对比智能体
│   ├── booking_agent.py           # 预订执行智能体
│   └── customer_service_agent.py  # 客服咨询智能体
│
├── frontend/                       # 🎨 前端界面
│   ├── index.html                 # 主页面
│   ├── app.js                     # 前端逻辑
│   ├── styles.css                 # 样式文件
│   └── README.md                  # 前端说明
│
├── logs/                          # 📊 日志目录
│   ├── backend.log                # 后端日志
│   └── frontend.log               # 前端日志
│
├── config.py                      # ⚙️ 配置管理（环境变量）
├── models.py                      # 📋 数据模型（Pydantic）
├── database.py                    # 💾 数据库配置（SQLAlchemy）
├── workflow.py                    # 🔄 LangGraph工作流编排
├── main.py                        # 🚀 FastAPI应用入口
├── test_client.py                 # 🧪 测试客户端
│
├── start_all.sh                   # ▶️ 一键启动脚本（推荐）
├── run.sh                         # 🔧 灵活启动脚本
├── setup_env.sh                   # 🐍 环境设置脚本
│
├── requirements.txt               # 📦 项目依赖
├── .env.example                  # 🔐 环境变量模板
├── README.md                      # 📖 项目文档（本文件）
├── ARCHITECTURE.md                # 🏗️ 架构设计文档
├── DEPLOYMENT.md                  # 🚀 部署指南
└── FRONTEND.md                    # 💻 前端开发文档
```

## 🚀 快速开始

### 1. 环境准备

确保已安装 Python 3.10+：

```bash
python --version
```

### 2. 创建虚拟环境

```bash
# 使用 conda (推荐)
conda create -n travel-agent python=3.10
conda activate travel-agent

# 或使用 venv
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入你的通义千问 API Key
# DASHSCOPE_API_KEY=your_api_key_here
```

获取通义千问 API Key：
1. 访问 [阿里云百炼平台](https://dashscope.console.aliyun.com/)
2. 注册/登录账号
3. 创建 API Key

### 5. 启动服务

#### 方式1: 一键启动前后端（推荐）⭐

```bash
./start_all.sh
```

这将同时启动：
- 后端服务：http://localhost:8000
- 前端界面：http://localhost:8080

#### 方式2: 分别启动

**启动后端：**
```bash
python main.py
# 或
./run.sh dev
```

**启动前端：**
```bash
cd frontend
python -m http.server 8080
```

#### 方式3: 仅启动后端API

```bash
python main.py
```

服务将在 `http://localhost:8000` 启动。

访问 API 文档：`http://localhost:8000/docs`

### 6. 访问应用

- **前端界面**: http://localhost:8080 （推荐）
- **API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health

## 📚 API 使用示例

### 通用查询接口

```bash
curl -X POST "http://localhost:8000/api/v1/travel/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "我想查询12月1日从北京到上海的机票",
    "user_id": "user123"
  }'
```

### 机票查询

```bash
curl -X POST "http://localhost:8000/api/v1/travel/flight" \
  -H "Content-Type: application/json" \
  -d '{
    "departure": "北京",
    "destination": "上海",
    "departure_date": "2025-12-01",
    "passengers": 1
  }'
```

### 酒店查询

```bash
curl -X POST "http://localhost:8000/api/v1/travel/hotel" \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "上海",
    "budget": 500,
    "preferences": ["四星级", "市中心"]
  }'
```

### 景点推荐

```bash
curl -X POST "http://localhost:8000/api/v1/travel/attraction" \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "杭州",
    "days": 3,
    "preferences": ["自然风光", "历史文化"]
  }'
```

## 🧪 测试

### 运行测试客户端

```bash
# 自动测试模式（测试多个场景）
python test_client.py

# 交互模式（手动输入查询）
python test_client.py interactive
```

### 测试场景示例

1. **机票查询**
   - "我想查询12月1日从北京到上海的机票，1个人"

2. **酒店查询**
   - "帮我找一下上海的酒店，预算500元左右，想要四星级的"

3. **景点推荐**
   - "推荐一些杭州的景点，我喜欢自然风光和历史文化"

4. **行程规划**
   - "帮我规划一个3天的成都之旅，12月10日出发，12月12日返回"

5. **客服咨询**
   - "请问机票改签需要什么条件？收费标准是怎样的？"

## 📖 详细说明

### 🔍 核心技术实现

#### RAG（检索增强生成）系统
1. **文档处理流程**
   - 读取私有旅游文档（PDF、Word、Markdown等）
   - 设计切片策略（按章节、段落、语义单元切分）
   - 使用嵌入模型（如通义千问Embedding）转换为向量

2. **向量存储与检索**
   - PostgreSQL + pgvector 扩展存储语义向量
   - 支持相似度搜索（余弦相似度、欧氏距离）
   - 多维度过滤（地域、类型、价格等）
   - 响应时间优化：≤300ms

3. **查询优化**
   - **查询重写器**：将用户口语化查询转换为检索友好格式
   - **检索增强器**：结合向量检索和关键词匹配
   - **重排序**：根据相关性和时效性重新排序结果

#### 对话持久化机制
1. **ChatMemory实现**
   - 基于LangChain的ChatMemory
   - 支持短期记忆（会话内）和长期记忆（跨会话）
   - 自动总结历史对话，压缩上下文

2. **拦截器设计**
   - 在LangGraph节点间插入拦截器
   - 捕获关键状态变化（意图识别、查询结果等）
   - 异步写入数据库，不阻塞主流程

3. **序列化存储**
   - 使用Kryo/Pickle序列化消息对象
   - 支持复杂数据结构（嵌套对象、自定义类型）
   - 压缩存储，节省空间

### 🤖 智能体详细介绍

#### 1. 意图解析智能体 (IntentParseAgent)
- **职责**：识别用户查询意图，提取关键信息
- **输入**：自然语言查询（如"我想去北京玩3天"）
- **输出**：结构化意图信息（类型、出发地、目的地、日期等）
- **技术**：Few-shot Prompt + 结构化输出 + 意图分类

#### 2. 机票查询智能体 (FlightQueryAgent)
- **职责**：航班查询、比价、余票校验
- **输入**：出发地、目的地、日期、乘客数
- **输出**：航班列表（价格、时间、余票、航空公司等）
- **技术**：MCP工具调用 + 多源数据聚合 + 智能排序

#### 3. 酒店查询智能体 (HotelQueryAgent)
- **职责**：酒店搜索、筛选、价格对比
- **输入**：目的地、日期、预算、偏好
- **输出**：酒店列表（价格、星级、设施、评分等）
- **技术**：地理位置过滤 + 用户偏好匹配 + 价格区间筛选

#### 4. 景点推荐智能体 (AttractionRecommendAgent)
- **职责**：基于目的地和偏好推荐景点
- **输入**：目的地、天数、兴趣标签
- **输出**：景点列表（类别、门票、开放时间、评分等）
- **技术**：RAG知识库检索 + 协同过滤 + 热度排序

#### 5. 行程规划智能体 (ItineraryPlanAgent)
- **职责**：整合交通、住宿、景点生成完整行程
- **输入**：意图 + 其他智能体结果
- **输出**：每日详细行程表（时间轴、费用明细、路线规划）
- **技术**：多智能体结果融合 + 约束满足 + 时间优化

#### 6. 价格对比智能体 (PriceCompareAgent)
- **职责**：跨平台价格比对，寻找最优价格
- **输入**：产品ID（航班/酒店）
- **输出**：多平台价格对比表（最低价、价差、推荐平台）
- **技术**：并发API调用 + 价格趋势分析 + 优惠券叠加

#### 7. 预订执行智能体 (BookingAgent)
- **职责**：处理订单创建、确认、取消
- **输入**：选择结果 + 用户信息 + 支付信息
- **输出**：订单号、确认信息、电子票据
- **技术**：事务管理 + 订单状态机 + 异步通知

#### 8. 客服咨询智能体 (CustomerServiceAgent)
- **职责**：解答售后问题、特殊需求处理、FAQ
- **输入**：问题描述 + 订单号（可选）
- **输出**：专业回答和解决方案
- **技术**：FAQ匹配 + 订单查询 + 情感分析 + 人工转接

### 🔄 LangGraph 工作流编排

#### 工作流特性
- ✅ **智能路由**：根据意图类型动态选择执行路径
- ✅ **条件分支**：支持复杂的业务逻辑判断
- ✅ **状态管理**：跨节点数据传递和状态共享
- ✅ **错误处理**：异常捕获、重试机制、降级策略
- ✅ **并行执行**：支持多智能体并发调用
- ✅ **循环控制**：支持迭代优化和人工反馈

#### 工作流执行流程
1. **意图解析阶段**：识别用户需求，提取关键信息
2. **信息收集阶段**：根据意图类型调用相应智能体
3. **结果整合阶段**：汇总各智能体输出
4. **答案生成阶段**：生成结构化、友好的回复
5. **持久化阶段**：保存对话历史和用户偏好

#### 路由策略
```python
意图类型           → 执行路径
flight           → 机票查询 → 生成答案
hotel            → 酒店查询 → 生成答案
itinerary        → 机票查询 → 酒店查询 → 景点推荐 → 行程规划 → 生成答案
price_compare    → 价格对比 → 生成答案
booking          → 预订执行 → 生成答案
customer_service → 客服咨询 → 生成答案
```

### 数据模型

项目使用 Pydantic 进行数据验证，包含：
- 意图模型（ParsedIntent）
- 航班模型（Flight）
- 酒店模型（Hotel）
- 景点模型（Attraction）
- 行程模型（Itinerary）
- 订单模型（Order）
- 响应模型（AgentResponse, FinalResponse）

## 🔧 配置说明

### 环境变量

```bash
# 通义千问 API
DASHSCOPE_API_KEY=your_api_key

# LLM 配置
LLM_MODEL=qwen-turbo          # 模型名称
LLM_TEMPERATURE=0.7           # 温度参数
LLM_MAX_TOKENS=2000          # 最大token数

# 应用配置
APP_HOST=0.0.0.0
APP_PORT=8000
LOG_LEVEL=INFO

# 数据库
DATABASE_URL=sqlite+aiosqlite:///./travel_agent.db
```

### 模型选择

通义千问支持多个模型：
- `qwen-turbo`（推荐）：性价比高，响应快
- `qwen-plus`：能力更强
- `qwen-max`：最强能力

## 📊 日志系统

日志文件位置：`logs/app_YYYY-MM-DD.log`

日志级别：
- INFO：正常操作日志
- WARNING：警告信息
- ERROR：错误信息

## 🛠️ 开发指南

### 添加新智能体

1. 在 `agents/` 目录创建新文件
2. 继承 `BaseAgent` 类
3. 实现必要方法：
   - `_create_prompt_template()`
   - `process()`
4. 在 `agents/__init__.py` 中导出
5. 在 `workflow.py` 中集成

### 扩展功能

- 添加新的数据模型到 `models.py`
- 添加新的API端点到 `main.py`
- 修改工作流逻辑到 `workflow.py`

## 🐛 常见问题

### 1. API Key 无效

```
解决方案：检查 .env 文件中的 DASHSCOPE_API_KEY 是否正确
```

### 2. 端口被占用

```bash
# 修改 .env 文件中的 APP_PORT
APP_PORT=8001
```

### 3. 依赖安装失败

```bash
# 更新 pip
pip install --upgrade pip

# 使用清华镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 4. LLM 响应慢

```
解决方案：
1. 切换到 qwen-turbo 模型
2. 减少 LLM_MAX_TOKENS 值
3. 优化提示词长度
```

## 📈 性能优化策略

### 🚀 响应速度优化
1. **异步IO架构**
   - FastAPI + asyncio 全异步处理
   - httpx 异步HTTP客户端
   - 数据库异步操作（AsyncSession）
   - 目标响应时间：≤300ms

2. **缓存机制**
   - **LLM响应缓存**：相同查询直接返回缓存结果
   - **数据缓存**：热门景点、航班信息缓存
   - **用户偏好缓存**：减少数据库查询
   - 缓存策略：LRU + TTL

3. **并发优化**
   - 多智能体并行调用（asyncio.gather）
   - 数据库连接池（SQLAlchemy pool）
   - API限流与熔断
   - 批量操作优化

### 💡 模型调用优化
1. **Prompt优化**
   - 精简提示词，减少token消耗
   - Few-shot示例优化
   - 结构化输出格式

2. **模型选择策略**
   - 简单任务：qwen-turbo（快速响应）
   - 复杂任务：qwen-plus/max（高质量输出）
   - 动态切换模型

3. **降低成本**
   - 意图识别使用轻量模型
   - 批量请求合并
   - 智能缓存策略

### 📊 数据库优化
1. **索引优化**
   - 用户ID、订单ID、时间戳索引
   - 复合索引优化查询

2. **查询优化**
   - 分页加载
   - 延迟加载
   - 查询计划分析

3. **数据清理**
   - 定期清理过期日志
   - 归档历史订单

## 🔐 安全建议

- ✅ 不要将 `.env` 文件提交到版本控制
- ✅ 定期更新依赖包
- ✅ 在生产环境使用HTTPS
- ✅ 实施API访问限流

## 📝 许可证

MIT License

## 🔗 相关链接

- 🏠 **项目主页**: [GitHub - Nian-Fu/Agent](https://github.com/Nian-Fu/Agent)
- 🚀 **在线体验**: [https://uiagent-171000-8-1367279107.sh.run.tcloudbase.com](https://uiagent-171000-8-1367279107.sh.run.tcloudbase.com)
- 📚 **技术文档**: 查看 `ARCHITECTURE.md` 了解详细架构设计

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📞 联系方式

- 📧 如有问题，请提交 [GitHub Issue](https://github.com/Nian-Fu/Agent/issues)
- 💬 技术交流欢迎 Star 和 Fork

## 🙏 致谢

### 技术框架
- [LangChain](https://github.com/langchain-ai/langchain) - 智能体框架
- [LangGraph](https://github.com/langchain-ai/langgraph) - 工作流编排
- [FastAPI](https://fastapi.tiangolo.com/) - Web框架
- [通义千问](https://tongyi.aliyun.com/) - 大语言模型

### 工具与服务
- [DashScope](https://dashscope.console.aliyun.com/) - 阿里云百炼平台
- [高德地图开放平台](https://lbs.amap.com/) - 地理位置服务
- [腾讯云 CloudBase](https://cloud.tencent.com/product/tcb) - Serverless部署

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

<div align="center">

⭐ **如果这个项目对你有帮助，请给个星标！** ⭐

Made with ❤️ by [Nian-Fu](https://github.com/Nian-Fu)

[⬆ 回到顶部](#-智能旅行助手---多智能体旅行规划平台)

</div>

