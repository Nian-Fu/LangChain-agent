"""
配置管理模块
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用配置"""
    
    # 通义千问配置
    DASHSCOPE_API_KEY: sk-5f6c762ff1fe4a5ea4d89a30dde51912
    
    # 应用配置
    APP_NAME: str = "携程式多智能体旅行平台"
    APP_VERSION: str = "1.0.0"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    
    # 数据库配置
    DATABASE_URL: str = "sqlite+aiosqlite:///./travel_agent.db"
    
    # LLM 配置
    LLM_MODEL: str = "qwen-turbo"
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 2000
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 全局配置实例
settings = Settings()

