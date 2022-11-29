import sys
from PyQt6.QtWidgets import (
    QApplication,
)
from .main_window.MainWindow import MainWindow

def initUI():
    app = QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec())