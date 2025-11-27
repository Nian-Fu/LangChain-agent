# 部署指南

本文档提供多种部署方式的详细说明。

## 目录

- [本地开发部署](#本地开发部署)
- [生产环境部署](#生产环境部署)
- [Docker部署](#docker部署)
- [云服务部署](#云服务部署)

## 本地开发部署

### 1. 基础部署

```bash
# 1. 克隆项目
git clone <repository_url>
cd LangChain-agent

# 2. 创建虚拟环境
conda create -n travel-agent python=3.10
conda activate travel-agent

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入 API Key

# 5. 启动服务
python main.py
```

### 2. 开发模式

```bash
# 使用 uvicorn 的热重载功能
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 生产环境部署

### 1. 使用 Gunicorn + Uvicorn

```bash
# 安装 gunicorn
pip install gunicorn

# 启动服务（4个worker进程）
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log
```

### 2. 使用 Supervisor 管理进程

安装 supervisor：

```bash
sudo apt-get install supervisor  # Ubuntu/Debian
# 或
sudo yum install supervisor      # CentOS/RHEL
```

创建配置文件 `/etc/supervisor/conf.d/travel-agent.conf`：

```ini
[program:travel-agent]
command=/path/to/venv/bin/gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
directory=/path/to/LangChain-agent
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/travel-agent.err.log
stdout_logfile=/var/log/travel-agent.out.log
environment=PATH="/path/to/venv/bin"
```

启动服务：

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start travel-agent
```

### 3. 使用 Systemd 服务

创建服务文件 `/etc/systemd/system/travel-agent.service`：

```ini
[Unit]
Description=Travel Agent API Service
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/path/to/LangChain-agent
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable travel-agent
sudo systemctl start travel-agent
sudo systemctl status travel-agent
```

## Docker 部署

### 1. 创建 Dockerfile

创建 `Dockerfile`：

```dockerfile
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制项目文件
COPY . .

# 创建日志目录
RUN mkdir -p logs

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. 创建 docker-compose.yml

```yaml
version: '3.8'

services:
  travel-agent:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DASHSCOPE_API_KEY=${DASHSCOPE_API_KEY}
      - APP_HOST=0.0.0.0
      - APP_PORT=8000
      - LOG_LEVEL=INFO
    volumes:
      - ./logs:/app/logs
      - ./travel_agent.db:/app/travel_agent.db
    restart: unless-stopped
```

### 3. 构建和运行

```bash
# 构建镜像
docker build -t travel-agent:latest .

# 运行容器
docker run -d \
  --name travel-agent \
  -p 8000:8000 \
  -e DASHSCOPE_API_KEY=your_api_key \
  -v $(pwd)/logs:/app/logs \
  travel-agent:latest

# 或使用 docker-compose
docker-compose up -d
```

### 4. Docker 管理命令

```bash
# 查看日志
docker logs -f travel-agent

# 停止服务
docker stop travel-agent

# 重启服务
docker restart travel-agent

# 进入容器
docker exec -it travel-agent bash
```

## 云服务部署

### 1. 阿里云 ECS 部署

```bash
# 1. 登录ECS服务器
ssh user@your-ecs-ip

# 2. 安装Docker
curl -fsSL https://get.docker.com | bash -s docker

# 3. 克隆项目
git clone <repository_url>
cd LangChain-agent

# 4. 配置环境变量
echo "DASHSCOPE_API_KEY=your_api_key" > .env

# 5. 使用Docker部署
docker-compose up -d

# 6. 配置Nginx反向代理（可选）
sudo apt-get install nginx
```

Nginx 配置示例 `/etc/nginx/sites-available/travel-agent`：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 120s;
        proxy_send_timeout 120s;
        proxy_read_timeout 120s;
    }
}
```

启用配置：

```bash
sudo ln -s /etc/nginx/sites-available/travel-agent /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 2. 腾讯云 Serverless 部署

安装 Serverless Framework：

```bash
npm install -g serverless
```

创建 `serverless.yml`：

```yaml
component: fastapi
name: travel-agent

inputs:
  src: ./
  region: ap-guangzhou
  runtime: Python3.9
  apigatewayConf:
    protocols:
      - http
      - https
    environment: release
  functionConf:
    timeout: 120
    memorySize: 512
    environment:
      variables:
        DASHSCOPE_API_KEY: ${env.DASHSCOPE_API_KEY}
```

部署：

```bash
serverless deploy
```

### 3. AWS Lambda 部署

使用 Mangum 适配器：

```bash
pip install mangum
```

修改 `main.py` 添加：

```python
from mangum import Mangum

# 在文件末尾添加
handler = Mangum(app)
```

使用 AWS SAM 部署：

```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  TravelAgentFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: .
      Handler: main.handler
      Runtime: python3.10
      Timeout: 120
      Environment:
        Variables:
          DASHSCOPE_API_KEY: !Ref DashscopeApiKey
      Events:
        Api:
          Type: HttpApi
          Properties:
            Path: /{proxy+}
            Method: ANY

Parameters:
  DashscopeApiKey:
    Type: String
    NoEcho: true
```

部署：

```bash
sam build
sam deploy --guided
```

## 性能优化建议

### 1. 使用 Redis 缓存

```bash
# 安装 redis
pip install redis aioredis

# 在代码中添加缓存逻辑
```

### 2. 使用 PostgreSQL 替代 SQLite

修改 `DATABASE_URL`：

```
DATABASE_URL=postgresql+asyncpg://user:password@localhost/travel_agent
```

### 3. 配置负载均衡

使用 Nginx 负载均衡：

```nginx
upstream travel_agent_backend {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}

server {
    listen 80;
    
    location / {
        proxy_pass http://travel_agent_backend;
    }
}
```

### 4. 启用 HTTPS

使用 Let's Encrypt：

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## 监控和日志

### 1. 集成 Prometheus

```bash
pip install prometheus-fastapi-instrumentator
```

在 `main.py` 中添加：

```python
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

### 2. 使用 ELK Stack

配置 Filebeat 收集日志：

```yaml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /path/to/logs/*.log

output.elasticsearch:
  hosts: ["localhost:9200"]
```

### 3. 健康检查

添加到 Docker Compose：

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

## 安全加固

### 1. 防火墙配置

```bash
# 允许必要端口
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

### 2. API 限流

安装 slowapi：

```bash
pip install slowapi
```

添加限流：

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/api/v1/travel/query")
@limiter.limit("10/minute")
async def query(request: Request):
    ...
```

### 3. CORS 配置

在生产环境限制允许的源：

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## 备份策略

### 1. 数据库备份

```bash
# 创建备份脚本
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp travel_agent.db backups/travel_agent_$DATE.db

# 只保留最近7天的备份
find backups/ -name "*.db" -mtime +7 -delete
```

### 2. 定时任务

```bash
# 添加到 crontab
crontab -e

# 每天凌晨2点备份
0 2 * * * /path/to/backup.sh
```

## 故障排查

### 1. 查看服务状态

```bash
# Systemd
sudo systemctl status travel-agent

# Docker
docker ps
docker logs travel-agent
```

### 2. 查看应用日志

```bash
tail -f logs/app_*.log
```

### 3. 性能分析

```bash
# 查看进程资源使用
top -p $(pgrep -f "main:app")

# 查看网络连接
netstat -tlnp | grep 8000
```

## 更新和回滚

### 1. 更新应用

```bash
# 拉取最新代码
git pull

# 重启服务
sudo systemctl restart travel-agent

# 或 Docker
docker-compose down
docker-compose up -d --build
```

### 2. 回滚版本

```bash
# Git回滚
git checkout <previous-commit>

# 重新部署
sudo systemctl restart travel-agent
```

---

如有问题，请查看主 README 或提交 Issue。

