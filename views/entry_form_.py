# views/entry_form.py
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QDoubleSpinBox,
    QSpinBox,
    QMessageBox,
    QFileDialog,
    QListWidget,
    QListWidgetItem,
    QFrame,
)
from PySide6.QtCore import Signal, Qt
import os
import shutil
from ..core.models import ProjectHisModel
from ..core.pgsql import DB
from ..core.utils import validate_json_string, show_error, show_success
from ..config import DEFAULT_THEME


class ProjectEntryForm(QWidget):
    saved = Signal()  # 保存成功后发出信号，通知主窗口刷新或其他操作

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.selected_files = []  # 存储选择的文件路径

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # 表单字段映射
        self.fields = {
            "name": ("项目名称 *", QLineEdit),
            "client_name": ("客户名称 *", QLineEdit),
            "project_type": ("项目类型", QLineEdit),
            "area_sqm": ("面积 (㎡)", QDoubleSpinBox),
            "location_city": ("所在城市", QLineEdit),
            "total_heating_load_kw": ("总制热负荷 (kW)", QDoubleSpinBox),
            "total_cooling_load_kw": ("总制冷负荷 (kW)", QDoubleSpinBox),
            "system_type": ("系统类型", QLineEdit),
            "selected_products": ("选型产品 (JSON)", QTextEdit),
            "total_cost_cny": ("总成本 (CNY)", QDoubleSpinBox),
            "annual_energy_consumption_kwh": ("年能耗 (kWh)", QDoubleSpinBox),
            "solution_summary": ("方案摘要", QTextEdit),
            "success_rating": ("成功评分 (1-5)", QSpinBox),
        }

        self.widgets = {}

        # 标题
        self.title_label = QLabel("项目信息录入")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(
            "font-size: 18px; font-weight: bold; margin: 10px;"
        )
        layout.addWidget(self.title_label)

        for field_name, (label_text, widget_class) in self.fields.items():
            # 创建表单行容器
            row_container = QFrame()
            row_container.setFrameStyle(QFrame.StyledPanel)
            self.widgets[f"{field_name}_container"] = row_container

            row_layout = QHBoxLayout(row_container)
            row_layout.setContentsMargins(10, 10, 10, 10)

            label = QLabel(label_text)
            label.setMinimumWidth(150)
            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            row_layout.addWidget(label)
            self.widgets[f"{field_name}_label"] = label

            if widget_class == QDoubleSpinBox:
                widget = QDoubleSpinBox()
                widget.setMaximum(999999999)
                widget.setDecimals(2)
            elif widget_class == QSpinBox:
                widget = QSpinBox()
                widget.setRange(1, 5)
                widget.setSpecialValueText("未评分")
            elif widget_class == QTextEdit:
                widget = QTextEdit()
                widget.setMaximumHeight(80)
                if "JSON" in label_text:
                    hint = QLabel('← 输入合法 JSON，如：{"型号": "A100"}')
                    self.widgets[f"{field_name}_hint"] = hint
                    row_layout.addWidget(hint)
            else:  # QLineEdit
                widget = QLineEdit()

            row_layout.addWidget(widget, 1)
            layout.addWidget(row_container)
            self.widgets[field_name] = widget

        # 文件附件选择区域
        self.setup_file_attachment_ui(layout)

        # 按钮区
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("💾 保存记录")
        self.save_btn.clicked.connect(self.save_record)
        self.clear_btn = QPushButton("🧹 清空表单")
        self.clear_btn.clicked.connect(self.clear_form)

        btn_layout.addStretch()
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.clear_btn)
        layout.addLayout(btn_layout)
        layout.addStretch()

        # 应用初始主题
        self.apply_theme(DEFAULT_THEME)

    def setup_file_attachment_ui(self, layout):
        # 创建文件附件区域容器
        self.file_container = QFrame()
        self.file_container.setFrameStyle(QFrame.StyledPanel)

        file_layout = QVBoxLayout(self.file_container)
        file_layout.setContentsMargins(10, 10, 10, 10)

        # 标题
        self.file_label = QLabel("附件列表")
        self.file_label.setStyleSheet("font-weight: bold;")
        file_layout.addWidget(self.file_label)

        # 文件选择按钮和列表
        file_control_layout = QHBoxLayout()
        self.file_btn = QPushButton("📁 选择文件")
        self.file_btn.clicked.connect(self.select_files)
        file_control_layout.addWidget(self.file_btn)
        file_control_layout.addStretch()

        file_layout.addLayout(file_control_layout)

        # 文件列表显示
        self.file_list_widget = QListWidget()
        self.file_list_widget.setMaximumHeight(100)
        file_layout.addWidget(self.file_list_widget)

        layout.addWidget(self.file_container)

    def apply_theme(self, theme_name: str):
        """应用指定主题到所有控件"""
        if theme_name == "dark":
            bg_color = "#333"
            text_color = "#fff"
            input_bg_color = "#444"
            container_bg_color = "#444"
            border_color = "#555"
        else:
            bg_color = "#f0f0f0"
            text_color = "#333"
            input_bg_color = "#fff"
            container_bg_color = "#fff"
            border_color = "#ccc"

        # 设置整体背景色
        self.setStyleSheet(f"QWidget {{ background-color: {bg_color}; }}")

        # 设置标题样式
        self.title_label.setStyleSheet(
            f"""
            QLabel {{
                color: {text_color};
                font-size: 18px; 
                font-weight: bold; 
                margin: 10px;
            }}
        """
        )

        # 设置容器样式
        for field_name in self.fields:
            container = self.widgets.get(f"{field_name}_container")
            if container:
                container.setStyleSheet(
                    f"background-color: {container_bg_color}; border-radius: 5px;"
                )

            # 设置标签样式
            label = self.widgets.get(f"{field_name}_label")
            if label:
                label.setStyleSheet(f"color: {text_color}; font-weight: bold;")

            # 设置提示文本样式
            hint = self.widgets.get(f"{field_name}_hint")
            if hint:
                hint.setStyleSheet("font-size: 10px; color: gray;")

            # 设置输入控件样式
            widget = self.widgets.get(field_name)
            if widget:
                if isinstance(widget, QTextEdit):
                    widget.setStyleSheet(
                        f"""
                        QTextEdit {{
                            padding: 5px;
                            border: 1px solid {border_color};
                            border-radius: 4px;
                            background-color: {input_bg_color};
                            color: {text_color};
                        }}
                        QTextEdit:focus {{
                            border: 2px solid #4CAF50;
                        }}
                    """
                    )
                elif isinstance(widget, QLineEdit):
                    widget.setStyleSheet(
                        f"""
                        QLineEdit {{
                            padding: 5px;
                            border: 1px solid {border_color};
                            border-radius: 4px;
                            background-color: {input_bg_color};
                            color: {text_color};
                        }}
                        QLineEdit:focus {{
                            border: 2px solid #4CAF50;
                        }}
                    """
                    )
                elif isinstance(widget, (QDoubleSpinBox, QSpinBox)):
                    widget.setStyleSheet(
                        f"""
                        QSpinBox, QDoubleSpinBox {{
                            padding: 5px;
                            border: 1px solid {border_color};
                            border-radius: 4px;
                            background-color: {input_bg_color};
                            color: {text_color};
                        }}
                        QSpinBox:focus, QDoubleSpinBox:focus {{
                            border: 2px solid #4CAF50;
                        }}
                    """
                    )

        # 设置文件附件区域样式
        self.file_container.setStyleSheet(
            f"background-color: {container_bg_color}; border-radius: 5px;"
        )
        self.file_label.setStyleSheet(f"color: {text_color}; font-weight: bold;")

        # 设置文件列表样式
        self.file_list_widget.setStyleSheet(
            f"""
            QListWidget {{
                background-color: {input_bg_color};
                color: {text_color};
                border: 1px solid {border_color};
                border-radius: 4px;
            }}
        """
        )

        # 设置按钮样式
        self.save_btn.setStyleSheet(
            f"""
            QPushButton {{
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
                background-color: #4CAF50;
                color: white;
            }}
            QPushButton:hover {{
                background-color: #45a049;
            }}
        """
        )

        self.clear_btn.setStyleSheet(
            f"""
            QPushButton {{
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
                background-color: #f44336;
                color: white;
            }}
            QPushButton:hover {{
                background-color: #da190b;
            }}
        """
        )

        self.file_btn.setStyleSheet(
            f"""
            QPushButton {{
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
                background-color: #2196F3;
                color: white;
            }}
            QPushButton:hover {{
                background-color: #0b7dda;
            }}
        """
        )

    def select_files(self):
        """选择文件并添加到列表"""
        files, _ = QFileDialog.getOpenFileNames(
            self, "选择附件文件", "", "所有文件 (*.*)"
        )

        if files:
            for file_path in files:
                if file_path not in self.selected_files:
                    self.selected_files.append(file_path)
                    # 添加到列表显示
                    item = QListWidgetItem(os.path.basename(file_path))
                    item.setData(Qt.UserRole, file_path)  # 保存完整路径

                    # 创建带有移除按钮的项
                    widget = QWidget()
                    widget_layout = QHBoxLayout(widget)
                    widget_layout.setContentsMargins(5, 2, 5, 2)

                    file_label = QLabel(os.path.basename(file_path))
                    remove_btn = QPushButton("移除")
                    remove_btn.setFixedSize(60, 25)
                    remove_btn.setStyleSheet(
                        """
                        QPushButton {
                            background-color: #ff9800;
                            color: white;
                            border-radius: 3px;
                            font-size: 12px;
                            padding: 2px 5px;
                        }
                        QPushButton:hover {
                            background-color: #e68a00;
                        }
                    """
                    )
                    remove_btn.clicked.connect(lambda _, i=item: self.remove_file(i))

                    widget_layout.addWidget(file_label)
                    widget_layout.addWidget(remove_btn)
                    widget_layout.addStretch()

                    item.setSizeHint(widget.sizeHint())
                    self.file_list_widget.addItem(item)
                    self.file_list_widget.setItemWidget(item, widget)

    def remove_file(self, item):
        """从列表中移除文件"""
        row = self.file_list_widget.row(item)
        file_path = item.data(Qt.UserRole)
        self.selected_files.remove(file_path)
        self.file_list_widget.takeItem(row)

    def get_form_data(self) -> dict:
        data = {}
        for field_name, widget in self.widgets.items():
            # 跳过容器和标签等非输入控件
            if field_name.endswith(("_container", "_label", "_hint")):
                continue

            if isinstance(widget, QTextEdit):
                value = widget.toPlainText().strip()
            elif isinstance(widget, (QLineEdit, QSpinBox, QDoubleSpinBox)):
                value = (
                    widget.text().strip()
                    if isinstance(widget, QLineEdit)
                    else widget.value()
                )
                if isinstance(widget, (QSpinBox, QDoubleSpinBox)) and value == 0:
                    value = None  # 数值控件 0 视为未填写（可调整）
            else:
                value = None

            # 特殊处理：空字符串转 None（除必填字段）
            if (
                isinstance(value, str)
                and value == ""
                and field_name not in ["name", "client_name"]
            ):
                value = None

            data[field_name] = value

        return data

    def save_files_to_project_dir(self, project_id):
        """将选择的文件保存到项目目录下的save文件夹中"""
        if not self.selected_files:
            return []

        # 创建项目保存目录
        project_save_dir = os.path.join("save", str(project_id))
        os.makedirs(project_save_dir, exist_ok=True)

        saved_files = []
        for file_path in self.selected_files:
            if os.path.exists(file_path):
                filename = os.path.basename(file_path)
                destination = os.path.join(project_save_dir, filename)
                shutil.copy2(file_path, destination)
                saved_files.append(filename)

        return saved_files

    def save_record(self):
        raw_data = self.get_form_data()

        # 必填字段校验
        if not raw_data.get("name") or not raw_data.get("client_name"):
            show_error(self, "项目名称和客户名称为必填项！")
            return

        # JSON 字段校验
        for json_field in ["selected_products"]:
            if raw_data.get(json_field) and not validate_json_string(
                raw_data[json_field]
            ):
                show_error(self, f"“{json_field}”字段不是合法的 JSON 格式！")
                return

        try:
            # Pydantic 自动校验 + 转换
            project = ProjectHisModel(**raw_data)
        except Exception as e:
            show_error(self, f"数据校验失败：\n{str(e)}")
            return

        # 保存到数据库
        with DB() as db:
            project_id = db.insert_project(project)
            if project_id:
                # 保存附件文件
                saved_files = self.save_files_to_project_dir(project_id)

                # 更新数据库中的附件信息（只保存文件名）
                if saved_files:
                    file_attachments_json = str(saved_files).replace("'", '"')
                    db.update_project_attachments(project_id, file_attachments_json)

                show_success(self, "✅ 项目保存成功！")
                self.clear_form()
                self.saved.emit()  # 发出信号
            else:
                show_error(self, "❌ 保存失败，请检查数据库连接或字段格式。")

    def clear_form(self):
        for field_name, widget in self.widgets.items():
            # 跳过容器和标签等非输入控件
            if field_name.endswith(("_container", "_label", "_hint")):
                continue

            if isinstance(widget, QTextEdit):
                widget.clear()
            elif isinstance(widget, QLineEdit):
                widget.clear()
            elif isinstance(widget, QSpinBox):
                widget.setValue(0)
            elif isinstance(widget, QDoubleSpinBox):
                widget.setValue(0.0)

        # 清空文件列表
        self.selected_files.clear()
        self.file_list_widget.clear()
