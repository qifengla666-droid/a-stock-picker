"""FastAPI 主应用"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging

from config import settings
from database import init_db, get_db
from data_provider import DataProvider
from analysis import StockAnalyzer
from models import Stock, DailyQuote, TechnicalIndicator, ScanResult
from schemas import StockResponse, ScanRequest, ScanResultResponse

# 配置日志
logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建 FastAPI 应用
app = FastAPI(
    title="A股选股工具",
    description="综合选股分析平台",
    version="1.0.0"
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化数据库
@app.on_event("startup")
async def startup():
    """应用启动"""
    logger.info("应用启动中...")
    init_db()
    logger.info("数据库初始化完成")

@app.get("/")
async def root():
    """根路径"""
    return {"message": "A股选股工具 API", "version": "1.0.0"}

@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "healthy"}

# ========== 股票相关接口 ==========

@app.get("/api/stocks", response_model=list[StockResponse])
async def get_stocks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取股票列表"""
    try:
        stocks = db.query(Stock).offset(skip).limit(limit).all()
        return stocks
    except Exception as e:
        logger.error(f"获取股票列表失败: {e}")
        raise HTTPException(status_code=500, detail="获取失败")

@app.post("/api/stocks/sync")
async def sync_stocks(db: Session = Depends(get_db)):
    """同步股票列表"""
    try:
        provider = DataProvider()
        stocks_data = provider.get_stock_list()
        
        for stock_data in stocks_data:
            existing = db.query(Stock).filter(
                Stock.code == stock_data['ts_code']
            ).first()
            
            if not existing:
                stock = Stock(
                    code=stock_data['ts_code'],
                    name=stock_data['name'],
                    industry=stock_data.get('industry', '')
                )
                db.add(stock)
        
        db.commit()
        logger.info(f"同步 {len(stocks_data)} 只股票")
        return {"message": f"成功同步 {len(stocks_data)} 只股票"}
    except Exception as e:
        logger.error(f"同步股票失败: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="同步失败")

# ========== 选股接口 ==========

@app.post("/api/scan", response_model=list[ScanResultResponse])
async def scan_stocks(
    request: ScanRequest,
    db: Session = Depends(get_db)
):
    """执行选股扫描"""
    try:
        logger.info("开始选股扫描...")
        
        results = []
        stocks = db.query(Stock).limit(100).all()
        
        for stock in stocks:
            try:
                # 获取日行情
                end_date = datetime.now().strftime('%Y%m%d')
                start_date = (datetime.now() - timedelta(days=200)).strftime('%Y%m%d')
                
                provider = DataProvider()
                daily_df = provider.get_daily_quote(stock.code, start_date, end_date)
                
                if daily_df is None or daily_df.empty:
                    continue
                
                # 计算指标
                analyzer = StockAnalyzer()
                indicators = analyzer.calculate_technical_indicators(daily_df)
                
                # 评分
                tech_score = analyzer.score_technical(indicators)
                fundamental_score = analyzer.score_fundamental({})
                money_flow_score = analyzer.score_money_flow({})
                overall_score = (tech_score + fundamental_score + money_flow_score) / 3
                
                # 判断是否符合条件
                if (tech_score >= request.technical_min_score and
                    fundamental_score >= request.fundamental_min_score and
                    money_flow_score >= request.money_flow_min_score and
                    overall_score >= request.overall_min_score):
                    
                    result = ScanResult(
                        code=stock.code,
                        name=stock.name,
                        scan_date=end_date,
                        technical_score=tech_score,
                        fundamental_score=fundamental_score,
                        money_flow_score=money_flow_score,
                        overall_score=overall_score,
                        reason="符合综合选股条件"
                    )
                    db.add(result)
                    results.append(result)
                
                if len(results) >= request.limit:
                    break
            
            except Exception as e:
                logger.error(f"处理 {stock.code} 失败: {e}")
                continue
        
        db.commit()
        logger.info(f"选股扫描完成，找到 {len(results)} 只符合条件的股票")
        return results
    
    except Exception as e:
        logger.error(f"选股扫描失败: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="扫描失败")

@app.get("/api/scan/history")
async def get_scan_history(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """获取选股历史"""
    try:
        results = db.query(ScanResult).order_by(
            ScanResult.created_at.desc()
        ).offset(skip).limit(limit).all()
        return results
    except Exception as e:
        logger.error(f"获取选股历史失败: {e}")
        raise HTTPException(status_code=500, detail="获取失败")

# ========== 分析接口 ==========

@app.get("/api/analysis/{code}")
async def analyze_stock(code: str, db: Session = Depends(get_db)):
    """分析单只股票"""
    try:
        stock = db.query(Stock).filter(Stock.code == code).first()
        if not stock:
            raise HTTPException(status_code=404, detail="股票不存在")
        
        # 获取最近数据
        result = db.query(ScanResult).filter(
            ScanResult.code == code
        ).order_by(ScanResult.created_at.desc()).first()
        
        if not result:
            return {"message": "暂无分析数据"}
        
        return {
            "code": result.code,
            "name": result.name,
            "technical_score": result.technical_score,
            "fundamental_score": result.fundamental_score,
            "money_flow_score": result.money_flow_score,
            "overall_score": result.overall_score,
            "reason": result.reason
        }
    except Exception as e:
        logger.error(f"分析失败: {e}")
        raise HTTPException(status_code=500, detail="分析失败")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port
    )