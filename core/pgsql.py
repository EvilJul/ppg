import psycopg2, os
from psycopg2 import sql
from dotenv import load_dotenv
from ..config import DB_CONFIG
from .models import ProjectHisModel
from psycopg2.extras import Json

load_dotenv()


class DB:
    def __init__(self):
        self.conn = None

    def db_connection(self) -> bool:
        """
        数据库额连接
        :return: 数据库连接对象
        """
        self.conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            database=DB_CONFIG["database"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
        )
        if self.conn:
            print("数据库连接成功")
            return True
        else:
            print("数据库连接失败")
            return False

    def db_close(self) -> bool:
        """
        数据库关闭连接
        :return:
        """
        if self.conn:
            self.conn.close()
            return True
        else:
            return False

    def db_inert(self, project: ProjectHisModel) -> bool:
        """
        数据库插入数据
        :param sql: sql语句
        :return:
        """

        if not self.conn:
            if self.db_connection():
                return False

        cursor = self.conn.cursor()
        # 构建字段和值
        fields = []
        values = []
        placeholders = []

        for filed_name, value in project.items():
            if filed_name is not None:
                fields.append(filed_name)
                if filed_name in [""]:
                    values.append(Json(value))
                else:
                    values.append(value)
                placeholders.append("%s")

        sql_ = sql.SQL("insert into projects_his ({}) values ({});").format(
            sql.SQL(", ").join(map(sql.Identifier, fields)),
            sql.SQL(", ").join(map(sql.Placeholder, placeholders)),
        )

        try:
            cursor.execute(sql_, values)
            self.conn.commit()
            cursor.close()
            print("✅数据插入成功")
            return True

        except Exception as e:
            self.conn.rollback()
            cursor.close()
            print(f"❌ 插入失败: {e}")
            return False

    def db_select(self, sql):
        """
        数据库查询数据
        :param sql: sql语句
        :return: 查询结果
        """
        conn, cursor = self.db_connection()
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            conn.close()
            print("数据查询成功")
            return result

        except Exception as e:
            print("数据查询失败")
            print(e)

    def __enter__(self):
        self.db_connection()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db_close()
