# A股选股工具

一个综合的中国A股选股分析平台，支持技术面、基本面、资金面多维度分析。

## 功能特性

- 📊 **技术面分析**：MA、MACD、RSI、KDJ 等指标
- 💹 **基本面分析**：市盈率、市净率、ROE、净利润增长等
- 💰 **资金面分析**：主力净流入、融资余额、持仓分析
- 🎯 **综合评分**：多维度打分体系
- 🌐 **Web 界面**：实时数据展示、条件筛选、图表分析
- 📈 **定期扫描**：自动更新数据、推送通知

## 项目结构

```
a-stock-picker/
├── backend/          # Python FastAPI 后端
├── frontend/         # React 前端
├── data/            # 数据存储
├── docs/            # 文档
└── docker-compose.yml
```

## 快速开始

### 环境要求

- Python 3.9+
- Node.js 16+
- Docker & Docker Compose（可选）

### 安装

1. 克隆仓库
```bash
git clone https://github.com/qifengla666-droid/a-stock-picker.git
cd a-stock-picker
```

2. 后端安装
```bash
cd backend
pip install -r requirements.txt
```

3. 前端安装
```bash
cd ../frontend
npm install
```

### 运行

#### 方式1：本地运行

```bash
# 终端1：后端
cd backend
python main.py

# 终端2：前端
cd frontend
npm start
```

#### 方式2：Docker 运行

```bash
docker-compose up
```

访问 http://localhost:3000

## 数据源

- **Tushare**：中国股票数据（需要 API Token）
- **Baostock**：免费实时数据
- **新浪财经**：基本面数据

## 使用说明

1. 注册/登录账户
2. 设置选股条件（可选择模板或自定义）
3. 运行筛选分析
4. 查看结果报告和详细分析
5. 添加到自选股或导出数据

## 配置

复制 `.env.example` 为 `.env` 并填写配置：

```
TUSHARE_TOKEN=your_token_here
DATABASE_URL=sqlite:///stocks.db
API_HOST=http://localhost:8000
```

## API 文档

运行后端后访问：http://localhost:8000/docs

## 贡献

欢迎提交 Issues 和 Pull Requests！

## License

MIT License

## 免责声明

本工具仅供学习和研究使用，不作为投资建议。使用本工具产生的投资损失与开发者无关。