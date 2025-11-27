#!/bin/bash

# 虚拟环境自动设置脚本
# 用法: ./setup_env.sh

set -e

echo "================================"
echo "携程式多智能体旅行平台"
echo "虚拟环境自动设置"
echo "================================"
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 检查 Python 版本
echo "检查 Python 版本..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo "✓ 找到 Python $PYTHON_VERSION"
else
    echo "✗ 错误: 未找到 Python 3"
    echo "请先安装 Python 3.10+"
    exit 1
fi

# 询问使用哪种虚拟环境
echo ""
echo "请选择虚拟环境类型:"
echo "1) Conda (推荐)"
echo "2) venv (Python 内置)"
echo ""
read -p "请输入选择 [1/2]: " choice

case $choice in
    1)
        echo ""
        echo "================================"
        echo "使用 Conda 创建虚拟环境"
        echo "================================"
        
        # 检查 conda 是否可用
        if ! command -v conda &> /dev/null; then
            echo "✗ 错误: 未找到 Conda"
            echo "请先安装 Anaconda 或 Miniconda"
            echo "访问: https://www.anaconda.com/download"
            exit 1
        fi
        
        ENV_NAME="travel-agent"
        
        # 检查环境是否已存在
        if conda env list | grep -q "^$ENV_NAME "; then
            echo "⚠️  环境 $ENV_NAME 已存在"
            read -p "是否删除并重新创建? [y/N]: " recreate
            if [[ $recreate =~ ^[Yy]$ ]]; then
                echo "删除旧环境..."
                conda env remove -n $ENV_NAME -y
            else
                echo "使用现有环境..."
                conda activate $ENV_NAME
                skip_create=true
            fi
        fi
        
        if [ "$skip_create" != "true" ]; then
            echo "创建 Conda 环境: $ENV_NAME (Python 3.10)..."
            conda create -n $ENV_NAME python=3.10 -y
        fi
        
        echo ""
        echo "✓ Conda 环境创建完成"
        echo ""
        echo "激活环境命令:"
        echo "  conda activate $ENV_NAME"
        
        ACTIVATE_CMD="conda activate $ENV_NAME"
        ;;
        
    2)
        echo ""
        echo "================================"
        echo "使用 venv 创建虚拟环境"
        echo "================================"
        
        ENV_DIR="venv"
        
        # 检查环境是否已存在
        if [ -d "$ENV_DIR" ]; then
            echo "⚠️  虚拟环境目录 $ENV_DIR 已存在"
            read -p "是否删除并重新创建? [y/N]: " recreate
            if [[ $recreate =~ ^[Yy]$ ]]; then
                echo "删除旧环境..."
                rm -rf $ENV_DIR
            else
                echo "使用现有环境..."
                skip_create=true
            fi
        fi
        
        if [ "$skip_create" != "true" ]; then
            echo "创建 venv 环境..."
            python3 -m venv $ENV_DIR
        fi
        
        echo ""
        echo "✓ venv 环境创建完成"
        echo ""
        echo "激活环境命令:"
        echo "  source venv/bin/activate"
        
        ACTIVATE_CMD="source venv/bin/activate"
        ;;
        
    *)
        echo "无效的选择"
        exit 1
        ;;
esac

# 提示激活环境
echo ""
echo "================================"
echo "下一步操作"
echo "================================"
echo ""
echo "请在新的终端或当前终端中执行以下命令:"
echo ""
echo "1. 激活虚拟环境:"
echo "   $ACTIVATE_CMD"
echo ""
echo "2. 安装依赖:"
echo "   pip install -r requirements.txt"
echo ""
echo "3. 配置环境变量:"
echo "   cp .env.example .env"
echo "   # 然后编辑 .env 文件，填入 DASHSCOPE_API_KEY"
echo ""
echo "4. 启动项目:"
echo "   ./start_all.sh"
echo ""
echo "================================"
echo "或者运行一键安装脚本:"
echo "   ./install_and_run.sh"
echo "================================"

# 创建快速启动脚本
cat > quick_start.sh << 'EOF'
#!/bin/bash

# 快速启动脚本
echo "激活虚拟环境并启动项目..."

# 检查使用哪种虚拟环境
if [ -d "venv" ]; then
    echo "检测到 venv 环境"
    source venv/bin/activate
elif command -v conda &> /dev/null && conda env list | grep -q "travel-agent"; then
    echo "检测到 Conda 环境"
    eval "$(conda shell.bash hook)"
    conda activate travel-agent
else
    echo "错误: 未找到虚拟环境"
    echo "请先运行: ./setup_env.sh"
    exit 1
fi

# 检查 .env 文件
if [ ! -f .env ]; then
    echo "错误: 未找到 .env 文件"
    echo "请先运行: cp .env.example .env"
    echo "并编辑 .env 文件，填入 DASHSCOPE_API_KEY"
    exit 1
fi

# 启动项目
echo "启动项目..."
./start_all.sh
EOF

chmod +x quick_start.sh

echo ""
echo "✓ 已创建快速启动脚本: quick_start.sh"
echo ""
echo "虚拟环境设置完成！"

