# core/utils.py
import json
from PySide6.QtWidgets import QMessageBox


def validate_json_string(text: str) -> bool:
    """校验字符串是否为合法 JSON"""
    if not text.strip():
        return True  # 允许为空
    try:
        json.loads(text)
        return True
    except json.JSONDecodeError:
        return False


def show_error(parent, message: str):
    QMessageBox.critical(parent, "错误", message)


def show_success(parent, message: str):
    QMessageBox.information(parent, "成功", message)
