import os
import json
import sys
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QTableWidget,
    QHeaderView,
    QTableWidgetItem,
    QWidget,
    QHBoxLayout,
    QPushButton,
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, pyqtSignal

from ....CONSTANTS import PATH_ICON_ITEM, PATH_PROFILE_CONFIG
from ....helper import _getExactlyPath

class ItemManager(QDialog):
    isShow = pyqtSignal(bool)
    isClose = pyqtSignal(bool)
    isSave = pyqtSignal(bool)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pathProfileConfig = _getExactlyPath(PATH_PROFILE_CONFIG)
        self.mainLayout = QVBoxLayout()
        self.__setstyle()

        self.itemTable = ItemTable(self)
        self.buttonBox = ButtonBox()
        self.buttonBox.btnSave.clicked.connect(lambda : self.__saveItem())

        self.isShow.connect(lambda : self.__fillItemTable())
        self.mainLayout.addWidget(self.itemTable)
        self.mainLayout.addWidget(self.buttonBox)
        self.setLayout(self.mainLayout)

    def __setstyle(self):
        self.setWindowTitle('Profile manager')
        self.setFixedSize(750, 500)
        iconPath = _getExactlyPath(PATH_ICON_ITEM)
        self.setWindowIcon(QIcon(iconPath))
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

    def __loadProfile(self):
        if os.path.exists(self.pathProfileConfig):
            try:
                with open(self.pathProfileConfig, 'r', encoding='utf8') as f:
                    profileConfig = json.load(f)
                return profileConfig
            except:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                return None
        else:
            return None

    def __writeProfie(self, payload):
        with open(self.pathProfileConfig, 'w', encoding='utf8') as f:
            json.dump(payload, f)
    
    def __saveItem(self):
        profiles = self.__loadProfile()
        for row in range(self.itemTable.rowCount()):
            items = []
            _username = self.itemTable.item(row, 0).text()
            
            for i in range(2, 7):
                if self.itemTable.item(row, i):
                    item = self.itemTable.item(row, i).text()
                    if item == '':
                        continue
                    items.append(item)
            profiles[_username]['items'] = items
        self.__writeProfie(profiles)

    def __fillItemTable(self):
        profiles = self.__loadProfile()
        for i in range(self.itemTable.rowCount()):
            self.itemTable.removeRow(0)
        
        if profiles is not None:
            for profile in profiles.values():
                rowPosition = self.itemTable.rowCount()
                self.itemTable.insertRow(rowPosition)
                username = QTableWidgetItem(profile['username'])
                username.setFlags(Qt.ItemFlag.ItemIsEditable)
                self.itemTable.setItem(rowPosition, 0, username)
                name = QTableWidgetItem(profile['name'])
                name.setFlags(Qt.ItemFlag.ItemIsEditable)
                self.itemTable.setItem(rowPosition, 1, name)
                if profile['status'] != 'logged':
                    continue
                _col = 2
                for item in profile['items']:
                    self.itemTable.setItem(rowPosition, _col, QTableWidgetItem(item))
                    _col += 1
    
    def closeEvent(self, event):
        self.isClose.emit(True)

class ItemTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__setStyle()
        
    def __setStyle(self):
        width = self.parent().width()
        self.setColumnCount(7)
        self.setHorizontalHeaderLabels(['Username', 'Name', 'Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5'])
        self.setColumnWidth(0, int(width/7))
        self.setColumnWidth(1, int(width/7))
        self.setColumnWidth(2, int(width/7))
        self.setColumnWidth(3, int(width/7))
        self.setColumnWidth(4, int(width/7))
        self.setColumnWidth(5, int(width/7))
        self.setColumnWidth(6, int(width/7))
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)

class ButtonBox(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.buttonBoxLayout = QHBoxLayout()

        self.btnSave = QPushButton('Save')
        self.btnSave.setObjectName('btnSave')
        self.btnQuit = QPushButton('Quit')
        self.btnQuit.setObjectName('btnQuit')
        self.btnQuit.clicked.connect(lambda : self._onBtnQuitClick())

        self.buttonBoxLayout.addWidget(self.btnQuit)
        self.buttonBoxLayout.addWidget(self.btnSave)

        self.setLayout(self.buttonBoxLayout)
        self.setStyleSheet('''
            QPushButton {
                height: 36px;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                color: rgb(255, 255, 255);
            }
            QPushButton#btnQuit {
                background-color: rgba(231, 76, 60, 1);
            }
            QPushButton#btnQuit::hover {
                background-color: rgb(204, 65, 51);
            }
            QPushButton#btnSave {
                background-color: rgba(0, 167, 78, 1);
                color: rgb(225, 225, 255);
            }
            QPushButton#btnSave::hover {
                background-color: rgba(0, 167, 78, 0.75);
            }
        ''')
    
    def _onBtnQuitClick(self):
        self.parent().close()
