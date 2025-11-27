#!/bin/bash

# 完整启动脚本 - 同时启动前后端服务
# 用法: ./start_all.sh

set -e

echo "================================"
echo "携程式多智能体旅行平台 - 完整启动"
echo "================================"

# 检查 Python 环境
if ! command -v python &> /dev/null; then
    echo "错误: 未找到 Python，请先安装 Python 3.10+"
    exit 1
fi

# 检查 .env 文件
if [ ! -f .env ]; then
    echo "错误: 未找到 .env 文件"
    echo "请复制 .env.example 并配置 API Key："
    echo "  cp .env.example .env"
    exit 1
fi

# 检查依赖
echo "检查依赖..."
pip list | grep -q "fastapi" || {
    echo "安装依赖..."
    pip install -r requirements.txt
}

# 创建日志目录
mkdir -p logs

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 清理函数
cleanup() {
    echo ""
    echo "================================"
    echo "正在关闭服务..."
    echo "================================"
    
    if [ ! -z "$BACKEND_PID" ]; then
        echo "关闭后端服务 (PID: $BACKEND_PID)"
        kill $BACKEND_PID 2>/dev/null || true
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        echo "关闭前端服务 (PID: $FRONTEND_PID)"
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    
    echo "所有服务已关闭"
    exit 0
}

# 注册清理函数
trap cleanup SIGINT SIGTERM EXIT

# 启动后端服务
echo ""
echo "================================"
echo "启动后端服务..."
echo "================================"
cd "$SCRIPT_DIR"
python main.py > logs/backend.log 2>&1 &
BACKEND_PID=$!
echo "后端服务已启动 (PID: $BACKEND_PID)"
echo "日志文件: logs/backend.log"

# 等待后端启动
echo "等待后端服务启动..."
sleep 3

# 检查后端是否启动成功
if ! ps -p $BACKEND_PID > /dev/null; then
    echo "错误: 后端服务启动失败"
    echo "请查看日志: logs/backend.log"
    exit 1
fi

# 启动前端服务
echo ""
echo "================================"
echo "启动前端服务..."
echo "================================"
cd "$SCRIPT_DIR/frontend"
python -m http.server 8080 > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "前端服务已启动 (PID: $FRONTEND_PID)"
echo "日志文件: logs/frontend.log"

# 等待前端启动
sleep 2

# 检查前端是否启动成功
if ! ps -p $FRONTEND_PID > /dev/null; then
    echo "错误: 前端服务启动失败"
    echo "请查看日志: logs/frontend.log"
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

# 显示访问信息
echo ""
echo "================================"
echo "✅ 所有服务启动成功！"
echo "================================"
echo ""
echo "📱 前端访问地址:"
echo "   http://localhost:8080"
echo ""
echo "🔧 后端API地址:"
echo "   http://localhost:8000"
echo ""
echo "📚 API文档:"
echo "   http://localhost:8000/docs"
echo ""
echo "💡 提示:"
echo "   - 在浏览器中打开 http://localhost:8080 开始使用"
echo "   - 按 Ctrl+C 关闭所有服务"
echo "   - 查看日志: tail -f logs/backend.log"
echo ""
echo "================================"
echo "服务运行中，按 Ctrl+C 停止..."
echo "================================"

# 保持脚本运行
wait

