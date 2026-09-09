from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Stock(Base):
    """股票信息表"""
    __tablename__ = "stocks"
    
    id = Column(Integer, primary_key=True)
    code = Column(String(20), unique=True, index=True)  # 股票代码
    name = Column(String(100))  # 股票名称
    industry = Column(String(100))  # 所属行业
    market_cap = Column(Float)  # 市值（亿元）
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class DailyQuote(Base):
    """日行情表"""
    __tablename__ = "daily_quotes"
    
    id = Column(Integer, primary_key=True)
    code = Column(String(20), index=True)
    date = Column(String(20), index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)
    amount = Column(Float)
    created_at = Column(DateTime, default=datetime.now)

class TechnicalIndicator(Base):
    """技术指标表"""
    __tablename__ = "technical_indicators"
    
    id = Column(Integer, primary_key=True)
    code = Column(String(20), index=True)
    date = Column(String(20), index=True)
    ma5 = Column(Float)  # 5日均线
    ma10 = Column(Float)  # 10日均线
    ma20 = Column(Float)  # 20日均线
    ma50 = Column(Float)  # 50日均线
    ma200 = Column(Float)  # 200日均线
    rsi = Column(Float)  # RSI
    macd = Column(Float)  # MACD
    kdj_k = Column(Float)  # KDJ-K值
    kdj_d = Column(Float)  # KDJ-D值
    kdj_j = Column(Float)  # KDJ-J值
    created_at = Column(DateTime, default=datetime.now)

class FundamentalData(Base):
    """基本面数据表"""
    __tablename__ = "fundamental_data"
    
    id = Column(Integer, primary_key=True)
    code = Column(String(20), unique=True, index=True)
    date = Column(String(20))
    pe_ratio = Column(Float)  # 市盈率
    pb_ratio = Column(Float)  # 市净率
    ps_ratio = Column(Float)  # 市销率
    roe = Column(Float)  # 净资产收益率
    gross_margin = Column(Float)  # 毛利率
    net_profit_margin = Column(Float)  # 净利率
    debt_ratio = Column(Float)  # 资产负债率
    current_ratio = Column(Float)  # 流动比率
    net_profit_growth = Column(Float)  # 净利润增长率
    revenue_growth = Column(Float)  # 营收增长率
    created_at = Column(DateTime, default=datetime.now)

class MoneyFlow(Base):
    """资金流向表"""
    __tablename__ = "money_flow"
    
    id = Column(Integer, primary_key=True)
    code = Column(String(20), index=True)
    date = Column(String(20), index=True)
    main_inflow = Column(Float)  # 主力净流入（万元）
    institutional_flow = Column(Float)  # 机构净流入
    retail_flow = Column(Float)  # 散户净流入
    margin_balance = Column(Float)  # 融资余额
    short_balance = Column(Float)  # 融券余额
    created_at = Column(DateTime, default=datetime.now)

class ScanResult(Base):
    """选股结果表"""
    __tablename__ = "scan_results"
    
    id = Column(Integer, primary_key=True)
    code = Column(String(20), index=True)
    name = Column(String(100))
    scan_date = Column(String(20))
    technical_score = Column(Float)  # 技术面评分
    fundamental_score = Column(Float)  # 基本面评分
    money_flow_score = Column(Float)  # 资金面评分
    overall_score = Column(Float)  # 综合评分
    reason = Column(Text)  # 选股理由
    created_at = Column(DateTime, default=datetime.now)