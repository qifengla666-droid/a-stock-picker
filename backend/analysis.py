"""选股分析模块"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class StockAnalyzer:
    """股票分析器"""
    
    @staticmethod
    def calculate_technical_indicators(df: pd.DataFrame) -> Dict[str, float]:
        """计算技术指标"""
        try:
            close = df['close'].astype(float)
            
            # 计算移动平均线
            ma5 = close.rolling(window=5).mean()
            ma10 = close.rolling(window=10).mean()
            ma20 = close.rolling(window=20).mean()
            ma50 = close.rolling(window=50).mean()
            ma200 = close.rolling(window=200).mean()
            
            # 计算 RSI
            rsi = StockAnalyzer._calculate_rsi(close)
            
            # 计算 MACD
            macd = StockAnalyzer._calculate_macd(close)
            
            # 计算 KDJ
            kdj_k, kdj_d, kdj_j = StockAnalyzer._calculate_kdj(
                df['high'].astype(float),
                df['low'].astype(float),
                close
            )
            
            return {
                'ma5': ma5.iloc[-1],
                'ma10': ma10.iloc[-1],
                'ma20': ma20.iloc[-1],
                'ma50': ma50.iloc[-1],
                'ma200': ma200.iloc[-1],
                'rsi': rsi.iloc[-1],
                'macd': macd.iloc[-1],
                'kdj_k': kdj_k.iloc[-1],
                'kdj_d': kdj_d.iloc[-1],
                'kdj_j': kdj_j.iloc[-1],
            }
        except Exception as e:
            logger.error(f"计算技术指标失败: {e}")
            return {}
    
    @staticmethod
    def _calculate_rsi(close: pd.Series, period: int = 14) -> pd.Series:
        """计算 RSI"""
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    @staticmethod
    def _calculate_macd(close: pd.Series) -> pd.Series:
        """计算 MACD"""
        exp1 = close.ewm(span=12, adjust=False).mean()
        exp2 = close.ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        return macd
    
    @staticmethod
    def _calculate_kdj(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 9):
        """计算 KDJ"""
        low_min = low.rolling(window=period).min()
        high_max = high.rolling(window=period).max()
        
        rsv = (close - low_min) / (high_max - low_min) * 100
        rsv = rsv.fillna(0)
        
        k = rsv.ewm(com=2, adjust=False).mean()
        d = k.ewm(com=2, adjust=False).mean()
        j = 3 * k - 2 * d
        
        return k, d, j
    
    @staticmethod
    def score_technical(indicators: Dict[str, float]) -> float:
        """技术面评分 (0-100)"""
        try:
            score = 50  # 基础分
            
            # RSI 评分
            rsi = indicators.get('rsi', 50)
            if 30 < rsi < 70:
                score += 10
            
            # MACD 评分
            macd = indicators.get('macd', 0)
            if macd > 0:
                score += 10
            
            # 均线评分
            close_price = indicators.get('close', 0)
            ma20 = indicators.get('ma20', 0)
            ma50 = indicators.get('ma50', 0)
            
            if close_price > ma20 > ma50:
                score += 15
            
            return min(100, max(0, score))
        except Exception as e:
            logger.error(f"技术面评分失败: {e}")
            return 50
    
    @staticmethod
    def score_fundamental(fundamental: Dict) -> float:
        """基本面评分 (0-100)"""
        try:
            score = 50
            
            # PE 评分
            pe = fundamental.get('pe_ratio', 0)
            if 0 < pe < 30:
                score += 15
            
            # PB 评分
            pb = fundamental.get('pb_ratio', 0)
            if 0 < pb < 3:
                score += 15
            
            # ROE 评分
            roe = fundamental.get('roe', 0)
            if roe > 15:
                score += 10
            
            # 净利润增长
            growth = fundamental.get('net_profit_growth', 0)
            if growth > 20:
                score += 10
            
            return min(100, max(0, score))
        except Exception as e:
            logger.error(f"基本面评分失败: {e}")
            return 50
    
    @staticmethod
    def score_money_flow(money_flow: Dict) -> float:
        """资金面评分 (0-100)"""
        try:
            score = 50
            
            # 主力净流入
            main_inflow = money_flow.get('main_inflow', 0)
            if main_inflow > 0:
                score += 15
            
            # 融资余额
            margin = money_flow.get('margin_balance', 0)
            if margin > 0:
                score += 10
            
            return min(100, max(0, score))
        except Exception as e:
            logger.error(f"资金面评分失败: {e}")
            return 50