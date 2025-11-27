# 系统架构文档

## 1. 整体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                          用户界面层                              │
│                    (Web/Mobile/API Client)                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       FastAPI 服务层                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ 查询接口 │  │ 机票接口 │  │ 酒店接口 │  │ 其他接口 │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LangGraph 工作流层                            │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                      状态图引擎                           │  │
│  │  • 意图识别路由                                           │  │
│  │  • 智能体调度                                            │  │
│  │  • 条件分支                                              │  │
│  │  • 状态管理                                              │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       智能体层                                   │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │ 意图解析    │  │ 机票查询    │  │ 酒店查询    │            │
│  │ 智能体      │  │ 智能体      │  │ 智能体      │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │ 景点推荐    │  │ 行程规划    │  │ 价格对比    │            │
│  │ 智能体      │  │ 智能体      │  │ 智能体      │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐                              │
│  │ 预订执行    │  │ 客服咨询    │                              │
│  │ 智能体      │  │ 智能体      │                              │
│  └─────────────┘  └─────────────┘                              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       LLM 服务层                                 │
│                    (通义千问 API)                                │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       数据持久化层                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                      │
│  │ 订单数据 │  │ 搜索历史 │  │ 用户偏好 │                      │
│  └──────────┘  └──────────┘  └──────────┘                      │
│                    (SQLite 数据库)                               │
└─────────────────────────────────────────────────────────────────┘
```

## 2. 工作流详解

### 2.1 主工作流

```
用户查询
   │
   ▼
┌──────────────────┐
│ 意图解析智能体    │
│ 输出: 意图类型    │
└────────┬─────────┘
         │
         ├─ flight ────────┐
         │                 ▼
         │          ┌──────────────┐
         │          │ 机票查询智能体│
         │          └──────┬───────┘
         │                 │
         ├─ hotel ─────────┤
         │                 ▼
         │          ┌──────────────┐
         │          │ 酒店查询智能体│
         │          └──────┬───────┘
         │                 │
         ├─ attraction ────┤
         │                 ▼
         │          ┌──────────────┐
         │          │ 景点推荐智能体│
         │          └──────┬───────┘
         │                 │
         ├─ itinerary ─────┼──────────┐
         │                 │          ▼
         │                 │   ┌──────────────┐
         │                 │   │ 查询机票+酒店 │
         │                 │   │ + 推荐景点    │
         │                 │   └──────┬───────┘
         │                 │          ▼
         │                 │   ┌──────────────┐
         │                 │   │ 行程规划智能体│
         │                 │   └──────┬───────┘
         │                 │          │
         ├─ price_compare ─┤          │
         │                 ▼          │
         │          ┌──────────────┐  │
         │          │ 价格对比智能体│  │
         │          └──────┬───────┘  │
         │                 │          │
         ├─ booking ───────┤          │
         │                 ▼          │
         │          ┌──────────────┐  │
         │          │ 预订执行智能体│  │
         │          └──────┬───────┘  │
         │                 │          │
         └─ service ───────┤          │
                           ▼          │
                    ┌──────────────┐  │
                    │ 客服咨询智能体│  │
                    └──────┬───────┘  │
                           │          │
                           └──────────┘
                                 │
                                 ▼
                         ┌──────────────┐
                         │ 生成最终答案  │
                         └──────────────┘
```

### 2.2 状态流转

```python
AgentState = {
    # 输入
    "query": str,           # 用户查询
    "user_id": str,         # 用户ID
    "session_id": str,      # 会话ID
    
    # 中间状态
    "intent": dict,         # 解析的意图
    "intent_type": str,     # 意图类型
    
    # 智能体结果
    "flight_result": dict,
    "hotel_result": dict,
    "attraction_result": dict,
    "itinerary_result": dict,
    "price_result": dict,
    "booking_result": dict,
    "service_result": dict,
    
    # 输出
    "final_answer": str,         # 最终答案
    "recommendations": list,     # 建议列表
    "error": str                 # 错误信息
}
```

## 3. 智能体设计

### 3.1 智能体基类

```python
class BaseAgent(ABC):
    def __init__(self, llm, agent_name):
        self.llm = llm
        self.agent_name = agent_name
        self.prompt_template = self._create_prompt_template()
    
    @abstractmethod
    def _create_prompt_template(self):
        """创建提示词模板"""
        pass
    
    @abstractmethod
    async def process(self, input_data):
        """处理输入数据"""
        pass
```

### 3.2 智能体通信

智能体之间通过共享状态（AgentState）进行通信：

```
┌──────────────┐
│ Agent A      │──┐
└──────────────┘  │
                  │
┌──────────────┐  │   ┌─────────────┐
│ Agent B      │──┼──▶│ AgentState  │
└──────────────┘  │   └─────────────┘
                  │
┌──────────────┐  │
│ Agent C      │──┘
└──────────────┘
```

## 4. 数据模型

### 4.1 核心模型

- **ParsedIntent**: 解析后的用户意图
- **Flight**: 航班信息
- **Hotel**: 酒店信息
- **Attraction**: 景点信息
- **Itinerary**: 完整行程
- **Order**: 订单信息
- **PriceComparison**: 价格对比

### 4.2 数据库表

```sql
-- 订单表
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    order_id VARCHAR(100) UNIQUE,
    user_id VARCHAR(100),
    product_type VARCHAR(50),
    product_id VARCHAR(100),
    product_name VARCHAR(200),
    quantity INTEGER,
    total_price FLOAT,
    status VARCHAR(20),
    contact_info JSON,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- 搜索历史表
CREATE TABLE search_history (
    id INTEGER PRIMARY KEY,
    user_id VARCHAR(100),
    session_id VARCHAR(100),
    query TEXT,
    intent_type VARCHAR(50),
    results JSON,
    created_at TIMESTAMP
);

-- 用户偏好表
CREATE TABLE user_preferences (
    id INTEGER PRIMARY KEY,
    user_id VARCHAR(100) UNIQUE,
    preferences JSON,
    favorite_destinations JSON,
    budget_range JSON,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

## 5. API 设计

### 5.1 RESTful API

```
POST /api/v1/travel/query
  - 通用旅行查询接口
  - 自动路由到相应智能体

POST /api/v1/travel/flight
  - 机票查询接口

POST /api/v1/travel/hotel
  - 酒店查询接口

POST /api/v1/travel/attraction
  - 景点推荐接口

POST /api/v1/travel/booking
  - 预订处理接口

POST /api/v1/customer/service
  - 客服咨询接口

GET /health
  - 健康检查

GET /
  - 服务信息
```

### 5.2 请求/响应格式

```json
// 请求
{
  "query": "我想查询12月1日从北京到上海的机票",
  "user_id": "user123",
  "session_id": "session456"
}

// 响应
{
  "success": true,
  "intent": {
    "intent_type": "flight",
    "departure": "北京",
    "destination": "上海",
    "departure_date": "2025-12-01"
  },
  "final_answer": "为您找到了5个航班选项...",
  "recommendations": ["点击查看详细航班信息"],
  "results": {
    "flight": { /* 航班数据 */ }
  }
}
```

## 6. 提示词工程

### 6.1 提示词结构

```
系统角色定义
├── 身份描述
├── 能力范围
├── 输出格式要求
└── 注意事项

用户输入
├── 查询内容
├── 上下文信息
└── 参数约束
```

### 6.2 示例提示词（意图解析）

```
System: 你是一个专业的旅行意图识别助手。
你的任务是从用户的自然语言查询中提取关键信息。

意图类型：
- flight: 机票查询
- hotel: 酒店查询
- attraction: 景点推荐
...

请以JSON格式返回结果。

User: 用户查询：我想查询12月1日从北京到上海的机票
```

## 7. 性能优化

### 7.1 异步处理

- 所有IO操作使用 async/await
- 智能体并行调用（无依赖时）
- 数据库异步查询

### 7.2 缓存策略

```
┌──────────┐
│ 请求     │
└────┬─────┘
     │
     ▼
┌──────────┐
│ 缓存检查 │──命中──▶ 返回缓存结果
└────┬─────┘
     │未命中
     ▼
┌──────────┐
│ LLM调用  │
└────┬─────┘
     │
     ▼
┌──────────┐
│ 更新缓存 │
└────┬─────┘
     │
     ▼
┌──────────┐
│ 返回结果 │
└──────────┘
```

### 7.3 连接池

- 数据库连接池（SQLAlchemy）
- HTTP连接池（httpx）
- LLM客户端单例

## 8. 错误处理

### 8.1 异常层级

```
ApplicationError
├── AgentError
│   ├── IntentParseError
│   ├── FlightQueryError
│   └── ...
├── WorkflowError
│   ├── RoutingError
│   └── StateError
└── APIError
    ├── ValidationError
    └── AuthenticationError
```

### 8.2 容错机制

- 智能体失败时降级处理
- LLM调用失败时重试（指数退避）
- 工作流异常时返回友好提示

## 9. 安全性

### 9.1 认证授权

- API Key 验证
- 用户身份认证
- 权限控制

### 9.2 数据保护

- 敏感信息加密
- SQL注入防护
- XSS防护
- CORS配置

### 9.3 限流

```python
@limiter.limit("10/minute")
async def query(request: Request):
    ...
```

## 10. 监控和日志

### 10.1 日志层级

- INFO: 正常操作
- WARNING: 潜在问题
- ERROR: 错误异常
- DEBUG: 调试信息

### 10.2 监控指标

- 请求量（QPS）
- 响应时间（P50, P95, P99）
- 错误率
- LLM调用次数和耗时
- 智能体成功率

### 10.3 追踪链

```
Request ID: xxx
  ├── Intent Parse: 200ms
  ├── Flight Query: 1500ms
  │   └── LLM Call: 1200ms
  └── Generate Answer: 300ms
Total: 2000ms
```

## 11. 扩展性

### 11.1 水平扩展

```
Load Balancer
    │
    ├─── Instance 1
    ├─── Instance 2
    ├─── Instance 3
    └─── Instance N
```

### 11.2 智能体扩展

添加新智能体只需：
1. 继承 BaseAgent
2. 实现接口
3. 注册到工作流

### 11.3 存储扩展

- SQLite → PostgreSQL/MySQL
- 添加 Redis 缓存
- 添加 MinIO 对象存储

## 12. 测试策略

### 12.1 单元测试

- 智能体单独测试
- 数据模型验证测试
- 工具函数测试

### 12.2 集成测试

- 工作流端到端测试
- API接口测试
- 数据库操作测试

### 12.3 性能测试

- 压力测试
- 并发测试
- 响应时间测试

---

此架构设计遵循以下原则：
- ✅ 单一职责原则
- ✅ 开放封闭原则
- ✅ 依赖倒置原则
- ✅ 接口隔离原则
- ✅ 高内聚低耦合

