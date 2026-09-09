"""数据获取模块 - 获取股票数据"""

import tushare as ts
import baostock as bs
import pandas as pd
from typing import List, Dict, Optional
from config import settings
import logging

logger = logging.getLogger(__name__)

class DataProvider:
    """数据提供者"""
    
    def __init__(self):
        # 初始化 Tushare
        if settings.tushare_token:
            ts.set_token(settings.tushare_token)
            self.pro = ts.pro_connect()
        
        # 初始化 Baostock
        bs.login()
    
    def get_stock_list(self) -> List[Dict]:
        """获取 A 股列表"""
        try:
            # 使用 Tushare 获取 A 股列表
            df = self.pro.stock_basic(
                exchange='',
                list_status='L',
                fields='ts_code,symbol,name,area,industry,market,list_date'
            )
            return df.to_dict('records')
        except Exception as e:
            logger.error(f"获取股票列表失败: {e}")
            return []
    
    def get_daily_quote(self, code: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        """获取日行情数据"""
        try:
            df = bs.query_history_k_data_plus(
                code,
                "date,code,open,high,low,close,volume,amount",
                start_date=start_date,
                end_date=end_date,
                frequency='d',
                adjustflag='2'
            )
            if df[0] == '0':
                return df[1]
            else:
                logger.warning(f"获取 {code} 日行情失败")
                return None
        except Exception as e:
            logger.error(f"获取 {code} 日行情异常: {e}")
            return None
    
    def get_fundamental_data(self, code: str) -> Optional[Dict]:
        """获取基本面数据"""
        try:
            # 这里使用 Tushare 获取基本面数据
            # 需要根据实际 API 调整
            df = self.pro.daily_basic(
                ts_code=code,
                fields='ts_code,trade_date,pe,pb,ps,dv_ratio,dv_ttm,total_mv'
            )
            if not df.empty:
                return df.iloc[0].to_dict()
            return None
        except Exception as e:
            logger.error(f"获取 {code} 基本面数据失败: {e}")
            return None
    
    def get_money_flow(self, code: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        """获取资金流向数据"""
        try:
            # 这里使用 Tushare 获取资金流向数据
            df = self.pro.moneyflow(
                ts_code=code,
                start_date=start_date,
                end_date=end_date
            )
            return df
        except Exception as e:
            logger.error(f"获取 {code} 资金流向失败: {e}")
            return None
    
    def close(self):
        """关闭数据连接"""
        bs.logout()