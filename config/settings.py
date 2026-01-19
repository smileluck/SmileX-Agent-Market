"""
项目全局配置文件
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 数据存储路径
DATA_DIR = os.path.join(PROJECT_ROOT, "data", "storage")
os.makedirs(DATA_DIR, exist_ok=True)

# 日志配置
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# 数据库配置
DATABASE_URL = "sqlite:///" + os.path.join(DATA_DIR, "smilex_agent.db")

# 大模型配置
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")

# 爬虫配置
CRAWLER_CONFIG = {
    "ZHIHU": {
        "BASE_URL": "https://www.zhihu.com",
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "COOKIE": os.getenv("ZHIHU_COOKIE", ""),
        "MAX_RETRIES": 3,
        "DOWNLOAD_DELAY": 2,
        "CONCURRENT_REQUESTS": 4,
    }
}

# Agent配置
AGENT_CONFIG = {
    "EVALUATION_DIMENSIONS": ["quality", "spread", "operation"],
    "SCORE_WEIGHTS": {"quality": 0.4, "spread": 0.3, "operation": 0.3},
}
