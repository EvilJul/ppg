"""
PPG 项目数据管理系统
主包初始化文件
"""

# ppg/__init__.py
from .views.main_windows import MainWindow
from .views.entry_form import ProjectEntryForm
from .core.models import ProjectHisModel
from .core.database import DatabaseManager
from .config import DB_CONFIG

__all__ = [
    "MainWindow",
    "ProjectEntryForm",
    "ProjectHisModel",
    "DatabaseManager",
    "DB_CONFIG",
]

__version__ = "1.0.0"
__author__ = "Jinhua Tian"
