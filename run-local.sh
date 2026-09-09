#!/bin/bash

echo "================================"
echo "A股选股工具 - 本地运行"
echo "================================"

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python 3.9+"
    exit 1
fi

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 错误: 未找到Node.js，请先安装Node.js 16+"
    exit 1
fi

echo "✅ 环境检查通过"

# 创建虚拟环境
if [ ! -d "backend/venv" ]; then
    echo "📦 创建Python虚拟环境..."
    cd backend
    python3 -m venv venv
    cd ..
fi

# 激活虚拟环境并安装依赖
echo "📦 安装后端依赖..."
cd backend
source venv/bin/activate
pip install -r requirements.txt
cd ..

# 安装前端依赖
echo "📦 安装前端依赖..."
cd frontend
npm install
cd ..

echo "✅ 依赖安装完成"

# 创建必要目录
mkdir -p data logs

# 复制环境配置
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  已创建.env文件，请编辑并添加TUSHARE_TOKEN"
fi

echo ""
echo "================================"
echo "✅ 准备完成！"
echo "================================"
echo ""
echo "📝 接下来的步骤:"
echo ""
echo "1️⃣  启动后端服务 (在新终端中):"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo "2️⃣  启动前端服务 (在新终端中):"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "3️⃣  访问应用:"
echo "   前端: http://localhost:3000"
echo "   API文档: http://localhost:8000/docs"
echo ""
echo "🔑 重要: 请确保已在.env文件中设置TUSHARE_TOKEN"
echo ""
