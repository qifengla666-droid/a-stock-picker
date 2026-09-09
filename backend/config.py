from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """应用配置"""
    
    # API 配置
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # 数据库
    database_url: str = "sqlite:///data/stocks.db"
    
    # Tushare 配置
    tushare_token: str = ""
    
    # 日志
    log_level: str = "INFO"
    
    # 数据更新间隔（分钟）
    update_interval: int = 60
    
    # 扫描时间
    scan_time: str = "09:30"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()