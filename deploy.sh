#!/bin/bash

echo "================================"
echo "A股选股工具 - 部署脚本"
echo "================================"

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ 错误: 未找到Docker，请先安装Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ 错误: 未找到Docker Compose，请先安装Docker Compose"
    exit 1
fi

echo "✅ Docker环境检查通过"

# 创建必要目录
echo "📁 创建数据目录..."
mkdir -p data logs

# 检查.env文件
if [ ! -f .env ]; then
    echo "⚠️  未找到.env文件，正在复制.env.example..."
    cp .env.example .env
    echo "⚠️  请编辑.env文件并添加TUSHARE_TOKEN"
fi

# 构建镜像
echo "🔨 构建Docker镜像..."
docker-compose build

if [ $? -ne 0 ]; then
    echo "❌ 镜像构建失败"
    exit 1
fi

echo "✅ 镜像构建成功"

# 启动服务
echo "🚀 启动服务..."
docker-compose up -d

if [ $? -ne 0 ]; then
    echo "❌ 服务启动失败"
    exit 1
fi

echo "✅ 服务启动成功"

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 5

# 检查服务状态
echo "🔍 检查服务状态..."
docker-compose ps

echo ""
echo "================================"
echo "✅ 部署完成！"
echo "================================"
echo ""
echo "📱 访问地址:"
echo "  前端: http://localhost:3000"
echo "  后端: http://localhost:8000"
echo "  API文档: http://localhost:8000/docs"
echo ""
echo "📝 常用命令:"
echo "  查看日志: docker-compose logs -f"
echo "  停止服务: docker-compose down"
echo "  重启服务: docker-compose restart"
echo ""
echo "🔑 注意: 请确保已在.env文件中设置TUSHARE_TOKEN"
echo ""
