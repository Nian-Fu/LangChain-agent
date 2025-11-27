#!/bin/bash

# 启动脚本
# 用法: ./run.sh [dev|prod|test]

set -e

MODE=${1:-dev}

echo "================================"
echo "携程式多智能体旅行平台"
echo "================================"

# 检查 Python 环境
if ! command -v python &> /dev/null; then
    echo "错误: 未找到 Python，请先安装 Python 3.10+"
    exit 1
fi

# 检查虚拟环境
if [ -z "$VIRTUAL_ENV" ] && [ -z "$CONDA_DEFAULT_ENV" ]; then
    echo "警告: 未检测到虚拟环境，建议使用虚拟环境"
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

# 创建必要的目录
mkdir -p logs

case $MODE in
    dev)
        echo "启动开发模式..."
        python main.py
        ;;
    prod)
        echo "启动生产模式..."
        if ! command -v gunicorn &> /dev/null; then
            echo "安装 gunicorn..."
            pip install gunicorn
        fi
        gunicorn main:app \
            --workers 4 \
            --worker-class uvicorn.workers.UvicornWorker \
            --bind 0.0.0.0:8000 \
            --timeout 120 \
            --access-logfile logs/access.log \
            --error-logfile logs/error.log
        ;;
    test)
        echo "运行测试..."
        python test_client.py
        ;;
    *)
        echo "用法: $0 [dev|prod|test]"
        echo "  dev  - 开发模式（默认）"
        echo "  prod - 生产模式（使用 gunicorn）"
        echo "  test - 运行测试"
        exit 1
        ;;
esac

