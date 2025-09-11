# main.py
import sys
from PySide6.QtWidgets import QApplication

from .views.main_windows import MainWindow

# from ppg import MainWindow, ProjectEntryForm

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # 统一风格基础

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
