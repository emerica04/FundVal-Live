import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 判断是否为打包后的应用
if getattr(sys, 'frozen', False):
    # 打包后：使用用户目录
    BASE_DIR = Path.home() / '.fundval-live'
    BASE_DIR.mkdir(parents=True, exist_ok=True)
else:
    # 开发模式：使用项目目录
    BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env from project root (one level up from backend)
if not getattr(sys, 'frozen', False):
    load_dotenv(BASE_DIR.parent / ".env")

class Config:
    # Database
    DB_PATH = os.path.join(BASE_DIR, "data", "fund.db")
    DB_URL = f"sqlite:///{DB_PATH}"
    
    # Data Sources
    # Options: 'eastmoney', 'sina' (future)
    DEFAULT_DATA_SOURCE = "eastmoney" 
    
    # External APIs (Eastmoney)
    EASTMONEY_API_URL = "http://fundgz.1234567.com.cn/js/{code}.js"
    EASTMONEY_DETAILED_API_URL = "http://fund.eastmoney.com/pingzhongdata/{code}.js"
    EASTMONEY_ALL_FUNDS_API_URL = "http://fund.eastmoney.com/js/fundcode_search.js"
    
    # AI Configuration
    # Defaults to empty, expecting environment variables or user input
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    AI_MODEL_NAME = os.getenv("AI_MODEL_NAME", "gpt-3.5-turbo")
    
    # Email / Subscription Configuration
    SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    EMAIL_FROM = os.getenv("EMAIL_FROM", "noreply@fundval.live")

    # Update Intervals
    FUND_LIST_UPDATE_INTERVAL = 86400  # 24 hours
    STOCK_SPOT_CACHE_DURATION = 60     # 1 minute (for holdings calculation)
