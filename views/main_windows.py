# views/main_window.py
from PySide6.QtWidgets import (
    QMainWindow,
    QToolBar,
    QStackedWidget,
    QMessageBox,
)
from PySide6.QtGui import QAction
from PySide6.QtGui import QIcon
from .entry_form_ import ProjectEntryForm
from ..config import DEFAULT_THEME, BASE_DIR
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("项目数据管理系统")
        # self.setGeometry(100, 100, 1000, 750)
        self.resize(1000, 400)  # 宽度1000，高度800

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.entry_form = ProjectEntryForm()
        self.entry_form.saved.connect(self.on_project_saved)
        self.stacked_widget.addWidget(self.entry_form)

        self.create_toolbar()
        self.load_theme(DEFAULT_THEME)

    def create_toolbar(self):
        toolbar = QToolBar("主工具栏")
        self.addToolBar(toolbar)

        theme_action = QAction("🌓 切换主题", self)
        theme_action.triggered.connect(self.toggle_theme)
        toolbar.addAction(theme_action)

        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about)
        toolbar.addAction(about_action)

    def toggle_theme(self):
        current = self.property("theme") or "light"
        new_theme = "dark" if current == "light" else "light"
        self.load_theme(new_theme)

    def load_theme(self, theme_name: str):
        qss_path = os.path.join(BASE_DIR, "resources", "style", f"{theme_name}.qss")
        try:
            with open(qss_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
            self.setProperty("theme", theme_name)
            # 通知entry_form应用主题
            self.entry_form.apply_theme(theme_name)
        except Exception as e:
            QMessageBox.warning(self, "样式加载失败", f"无法加载主题 {theme_name}: {e}")

    def on_project_saved(self):
        # 可扩展：刷新数据列表、发送通知等
        pass

    def show_about(self):
        QMessageBox.about(
            self, "关于", "项目数据管理系统 v1.0\n基于 PySide6 + PostgreSQL"
        )
