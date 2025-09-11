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
)
from PySide6.QtCore import Signal, Qt
from ..core.models import ProjectHisModel

# from ..core.database import DatabaseManager
from ..core.pgsql import DB
from ..core.utils import validate_json_string, show_error, show_success


class ProjectEntryForm(QWidget):
    saved = Signal()  # 保存成功后发出信号，通知主窗口刷新或其他操作

    def __init__(self):
        super().__init__()
        self.setup_ui()

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
            "file_attachments": ("附件列表 (JSON)", QTextEdit),
            "success_rating": ("成功评分 (1-5)", QSpinBox),
        }

        self.widgets = {}

        for field_name, (label_text, widget_class) in self.fields.items():
            row_layout = QHBoxLayout()
            label = QLabel(label_text)
            label.setMinimumWidth(150)
            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            row_layout.addWidget(label)

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
                    hint.setStyleSheet("font-size: 10px; color: gray;")
                    row_layout.addWidget(hint)
            else:  # QLineEdit
                widget = QLineEdit()

            row_layout.addWidget(widget, 1)
            layout.addLayout(row_layout)
            self.widgets[field_name] = widget

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

    def get_form_data(self) -> dict:
        data = {}
        for field_name, widget in self.widgets.items():
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

    def save_record(self):
        raw_data = self.get_form_data()

        # 必填字段校验
        if not raw_data.get("name") or not raw_data.get("client_name"):
            show_error(self, "项目名称和客户名称为必填项！")
            return

        # JSON 字段校验
        for json_field in ["selected_products", "file_attachments"]:
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
            if db.insert_project(project):
                show_success(self, "✅ 项目保存成功！")
                self.clear_form()
                self.saved.emit()  # 发出信号
            else:
                show_error(self, "❌ 保存失败，请检查数据库连接或字段格式。")

    def clear_form(self):
        for widget in self.widgets.values():
            if isinstance(widget, QTextEdit):
                widget.clear()
            elif isinstance(widget, QLineEdit):
                widget.clear()
            elif isinstance(widget, QSpinBox):
                widget.setValue(0)
            elif isinstance(widget, QDoubleSpinBox):
                widget.setValue(0.0)
