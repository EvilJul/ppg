# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# 数据库配置（建议后期改用 .env 或配置文件）
DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST"),
    "database": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "port": os.getenv("POSTGRES_PORT"),
}

# 默认主题
DEFAULT_THEME = "dark"  # 可选: "light", "dark"

# 项目根路径（用于资源定位）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
