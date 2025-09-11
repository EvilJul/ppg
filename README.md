# ppg-项目方案生成器(Project Plan generator)

### 初步想法：

集合已有项目案例数据，对新项目生成项目方案、关键参数计算、产品选型、工期预算、项目节点安排、成本核算

### 项目目录架构
```
your_app/
├── main.py                  # 启动入口
├── core/
│   ├── database.py          # 数据库连接、CRUD 封装
│   ├── models.py            # 数据模型（Pydantic 或 dataclass）
│   └── utils.py             # 工具函数（JSON 校验、日志等）
├── views/
│   ├── main_window.py       # 主窗口（带导航菜单）
│   ├── entry_form.py        # 录入表单页
│   ├── data_browser.py      # 数据浏览页（后期）
│   └── settings_dialog.py   # 设置页（主题切换等）
├── resources/
│   ├── style/
│   │   ├── light.qss
│   │   └── dark.qss         # Qt 样式表
│   └── icons/               # 图标资源
├── config.py                # 配置文件（数据库、主题默认值等）
└── requirements.txt
```