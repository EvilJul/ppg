# core/database.py
import psycopg2
from psycopg2.extras import Json
from psycopg2 import sql
from ..config import DB_CONFIG
from .models import ProjectHisModel


class DatabaseManager:
    def __init__(self):
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            return True
        except Exception as e:
            print(f"❌ 数据库连接失败: {e}")
            return False

    def close(self):
        if self.conn:
            self.conn.close()

    def insert_project(self, project: ProjectHisModel) -> bool:
        """
        插入一条项目记录
        """
        if not self.conn:
            if not self.connect():
                return False

        cursor = self.conn.cursor()

        # 构建字段和值
        fields = []
        values = []
        placeholders = []

        for field_name, value in project.dict().items():
            if value is not None:  # 只插入非空字段（或根据需求调整）
                fields.append(field_name)
                if field_name in ["selected_products", "file_attachments"]:
                    values.append(Json(value))
                else:
                    values.append(value)
                placeholders.append("%s")

        query = sql.SQL("INSERT INTO projects_his ({}) VALUES ({})").format(
            sql.SQL(", ").join(map(sql.Identifier, fields)),
            sql.SQL(", ").join(sql.Placeholder() * len(fields)),
        )

        try:
            cursor.execute(query, values)
            self.conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"❌ 插入失败: {e}")
            self.conn.rollback()
            cursor.close()
            return False

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
