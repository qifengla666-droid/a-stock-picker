# A股选股工具 部署指南

## 快速开始

### 方式1: Docker Compose 部署（推荐）

#### 前置要求
- Docker 20.10+
- Docker Compose 2.0+

#### 部署步骤

```bash
# 1. 克隆仓库
git clone https://github.com/qifengla666-droid/a-stock-picker.git
cd a-stock-picker

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，添加 TUSHARE_TOKEN

# 3. 运行部署脚本
chmod +x deploy.sh
./deploy.sh
```

#### 访问应用
- **前端**: http://localhost:3000
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs

#### 常用命令

```bash
# 查看运行日志
docker-compose logs -f

# 查看后端日志
docker-compose logs -f backend

# 查看前端日志
docker-compose logs -f frontend

# 停止所有服务
docker-compose down

# 重启服务
docker-compose restart

# 清理所有数据（谨慎操作）
docker-compose down -v
```

---

### 方式2: 本地运行

#### 前置要求
- Python 3.9+
- Node.js 16+
- npm 或 yarn

#### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/qifengla666-droid/a-stock-picker.git
cd a-stock-picker

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，添加 TUSHARE_TOKEN

# 3. 运行安装脚本
chmod +x run-local.sh
./run-local.sh
```

#### 启动应用

```bash
# 终端 1: 启动后端
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python main.py

# 终端 2: 启动前端
cd frontend
npm start
```

#### 访问应用
- **前端**: http://localhost:3000
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs

---

## 配置说明

### .env 环境变量

```bash
# Tushare API Token（必需）
TUSHARE_TOKEN=your_token_here

# 数据库配置
DATABASE_URL=sqlite:///data/stocks.db

# API 服务配置
API_HOST=0.0.0.0
API_PORT=8000

# 前端API地址
REACT_APP_API_URL=http://localhost:8000

# 日志级别
LOG_LEVEL=INFO

# 数据更新间隔（分钟）
UPDATE_INTERVAL=60

# 扫描时间（HH:MM，24小时制）
SCAN_TIME=09:30
```

### 获取 Tushare Token

1. 访问 [Tushare 官网](https://tushare.pro)
2. 注册账户
3. 在用户中心获取 API Token
4. 将 Token 添加到 .env 文件中的 TUSHARE_TOKEN

---

## 数据库

### SQLite（默认，适合个人使用）

```bash
# 数据库文件位置
./data/stocks.db

# 备份数据库
cp data/stocks.db data/stocks.db.backup

# 恢复数据库
cp data/stocks.db.backup data/stocks.db
```

### 切换到 PostgreSQL（可选，适合生产环境）

```bash
# 1. 修改 .env
DATABASE_URL=postgresql://user:password@localhost/stocks

# 2. 修改 docker-compose.yml，添加 PostgreSQL 服务
# 3. 重启应用
```

---

## 常见问题

### Q1: 后端无法连接到数据源
**A**: 检查 TUSHARE_TOKEN 是否正确配置，确保网络连接正常。

### Q2: 前端无法访问后端 API
**A**: 确保后端服务正在运行，检查 REACT_APP_API_URL 配置是否正确。

### Q3: Docker 构建失败
**A**: 
- 清理旧镜像: `docker system prune -a`
- 重新构建: `docker-compose build --no-cache`

### Q4: 数据库错误
**A**: 
- 删除旧数据库: `rm data/stocks.db`
- 重启应用会自动重建数据库结构

---

## 性能优化

### 后端优化

```python
# main.py 中配置工作进程数
# 生产环境建议使用 Gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

### 前端优化

```bash
# 生产构建
cd frontend
npm run build

# 使用 Nginx 提供静态文件
```

---

## 监控和日志

### Docker 日志

```bash
# 查看所有日志
docker-compose logs

# 实时查看日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend

# 保存日志到文件
docker-compose logs > app.log
```

### 本地日志

日志文件位置: `./logs/app.log`

---

## 生产部署建议

### 1. 使用 Gunicorn + Uvicorn

```bash
pip install gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 2. 使用 Nginx 反向代理

参考项目中的 `nginx.conf` 配置

### 3. 使用 PostgreSQL 数据库

配置数据库连接字符串为 PostgreSQL

### 4. 启用 HTTPS

配置 SSL 证书并在 Nginx 中启用

### 5. 定期备份数据

```bash
# 定时备份脚本
0 2 * * * docker exec a-stock-picker-backend cp /app/data/stocks.db /app/data/stocks.db.$(date +%Y%m%d)
```

---

## 贡献

欢迎提交 Issues 和 Pull Requests！

---

## License

MIT License
