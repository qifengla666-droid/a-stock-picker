"""Pydantic 数据模型"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class StockBase(BaseModel):
    code: str
    name: str
    industry: Optional[str] = None

class StockResponse(StockBase):
    market_cap: Optional[float] = None
    created_at: datetime

class DailyQuoteResponse(BaseModel):
    code: str
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    amount: float

class TechnicalIndicatorResponse(BaseModel):
    code: str
    date: str
    ma5: Optional[float] = None
    ma10: Optional[float] = None
    ma20: Optional[float] = None
    ma50: Optional[float] = None
    ma200: Optional[float] = None
    rsi: Optional[float] = None
    macd: Optional[float] = None

class FundamentalDataResponse(BaseModel):
    code: str
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    ps_ratio: Optional[float] = None
    roe: Optional[float] = None
    net_profit_growth: Optional[float] = None

class MoneyFlowResponse(BaseModel):
    code: str
    date: str
    main_inflow: Optional[float] = None
    institutional_flow: Optional[float] = None
    retail_flow: Optional[float] = None

class ScanResultResponse(BaseModel):
    code: str
    name: str
    scan_date: str
    technical_score: float
    fundamental_score: float
    money_flow_score: float
    overall_score: float
    reason: Optional[str] = None

class ScanRequest(BaseModel):
    """选股请求"""
    technical_min_score: float = 60  # 技术面最低分
    fundamental_min_score: float = 60  # 基本面最低分
    money_flow_min_score: float = 50  # 资金面最低分
    overall_min_score: float = 70  # 综合最低分
    limit: int = 50  # 返回结果数量限制

class AnalysisResponse(BaseModel):
    """分析结果"""
    code: str
    name: str
    current_price: float
    technical_analysis: dict
    fundamental_analysis: dict
    money_flow_analysis: dict
    scores: dict
    recommendation: str