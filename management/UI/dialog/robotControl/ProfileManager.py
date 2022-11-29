import os
import json
import sys
import shutil
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
from PyQt6.QtCore import Qt, pyqtSignal, QThread

from .login import Login
from ....CONSTANTS import PATH_ICON_PROFILE, PATH_PROFILES_BROWSER, PATH_PROFILE_CONFIG
from ....helper import _getExactlyPath

class ProfileManager(QDialog):
    isShow = pyqtSignal(bool)
    isSave = pyqtSignal(bool)
    isClose = pyqtSignal(bool)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pathProfileConfig = _getExactlyPath(PATH_PROFILE_CONFIG)
        self.mainLayout = QVBoxLayout()
        self.__setstyle()

        self.profileTable = ProfileTable(self)
        self.buttonBox = ButtonBox()
        self.buttonBox.btnAddProfile.clicked.connect(lambda : self.__addProfile())

        self.isShow.connect(lambda : self.__fillProfileTable())
        self.mainLayout.addWidget(self.profileTable)
        self.mainLayout.addWidget(self.buttonBox)
        self.setLayout(self.mainLayout)

    def __setstyle(self):
        self.setWindowTitle('Profile manager')
        self.setFixedSize(750, 500)
        iconPath = _getExactlyPath(PATH_ICON_PROFILE)
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

    def __fillProfileTable(self):
        for i in range(self.profileTable.rowCount()):
            self.profileTable.removeRow(0)

        self.profiles = self.__loadProfile()
    
        if self.profiles is not None:
            for profile in self.profiles.values():
                rowPosition =  self.profileTable.rowCount()
                self.profileTable.insertRow(rowPosition)

                username = QTableWidgetItem(profile['username'])
                password = QTableWidgetItem(profile['password'])
                name = QTableWidgetItem(profile['name'])
                name.setFlags(Qt.ItemFlag.ItemIsEditable)
                status = QTableWidgetItem(profile['status'])
                status.setFlags(Qt.ItemFlag.ItemIsEditable)

                self.profileTable.setItem(rowPosition, 0,username)
                self.profileTable.setItem(rowPosition, 1, password)
                self.profileTable.setItem(rowPosition, 2, name)
                self.profileTable.setItem(rowPosition, 3, status)
                # self.profileTable.item(rowPosition, 2).setFlags(Qt.ItemFlag.ItemIsEditable)
                # self.profileTable.item(rowPosition, 3).setFlags(Qt.ItemFlag.ItemIsEditable)
                self.btnLogin = QPushButton('Login')
                self.btnDelete = QPushButton('Delete')
                self.profileTable.setCellWidget(rowPosition, 4, self.btnLogin)
                self.profileTable.setCellWidget(rowPosition, 5, self.btnDelete)
                self.btnLogin.clicked.connect(lambda : self.__onBtnLoginClick(self.profileTable.currentRow()))
                self.btnDelete.clicked.connect(lambda : self.__onBtnDeleteClick(self.profileTable.currentRow()))

    def __addProfile(self):
        rowPosition = self.profileTable.rowCount()
        self.profileTable.insertRow(self.profileTable.rowCount())
        self.profileTable.setItem(rowPosition, 0, QTableWidgetItem(''))
        self.profileTable.setItem(rowPosition, 1, QTableWidgetItem(''))
        self.profileTable.setItem(rowPosition, 2, QTableWidgetItem(''))
        self.profileTable.setItem(rowPosition, 3, QTableWidgetItem(''))
        self.profileTable.item(rowPosition, 2).setFlags(Qt.ItemFlag.ItemIsEditable)
        self.profileTable.item(rowPosition, 3).setFlags(Qt.ItemFlag.ItemIsEditable)

        self.btnLogin = QPushButton('Login')
        self.btnDelete = QPushButton('Delete')
        self.profileTable.setCellWidget(rowPosition, 4, self.btnLogin)
        self.profileTable.setCellWidget(rowPosition, 5, self.btnDelete)
        self.btnLogin.clicked.connect(lambda : self.__onBtnLoginClick(self.profileTable.currentRow()))

    def __onBtnLoginClick(self, row):
        self.currentRow = row
        def reportProgress(payload):
            print(payload)
            self.profileTable.item(self.currentRow, 2).setText('')
            self.profileTable.item(self.currentRow, 3).setText(payload['msg'])
            
        def reportFinished(payload):
            print(payload)
            self.profileTable.item(self.currentRow, 2).setText(payload['name'])
            self.profileTable.item(self.currentRow, 3).setText(payload['status'])

            jsonObject = {}
            for row in range(self.profileTable.rowCount()):
                _username = self.profileTable.item(row, 0).text()
                _password = self.profileTable.item(row, 1).text()
                _name = self.profileTable.item(row, 2).text()
                _status = self.profileTable.item(row, 3).text()
                try:
                    _items = self.profiles[_username]['items']
                except KeyError:
                    _items = []

                jsonObject[_username] = {
                    'username' : _username,
                    'password' : _password,
                    'name': _name,
                    'status': _status,
                    'items': _items
                }
            self.__writeProfie(jsonObject)

        username = self.profileTable.item(row, 0).text()
        password = self.profileTable.item(row, 1).text()
        print('Username: ', username)
        self.loginThread = QThread()
        self.login = Login({'username': username, 'password': password})
        self.login.moveToThread(self.loginThread)

        self.loginThread.started.connect(self.login.run)
        self.loginThread.finished.connect(self.loginThread.deleteLater)

        self.login.progress_msg.connect(reportProgress)
        self.login.finished.connect(reportFinished)
        self.login.finished.connect(self.loginThread.quit)
        self.login.finished.connect(self.loginThread.deleteLater)
        self.login.finished.connect(self.login.deleteLater)

        self.loginThread.start()

    def __onBtnDeleteClick(self, row):
        username = self.profileTable.item(row, 0).text()
        pathProfile = _getExactlyPath(PATH_PROFILES_BROWSER) + '\\' + f'profile_{username}'
        profigleConfig = self.__loadProfile()
        del profigleConfig[username]
        self.__writeProfie(profigleConfig)
        if os.path.exists(pathProfile):
            shutil.rmtree(pathProfile)
        print('Removed profile: ', username)
        self.__fillProfileTable()

    def closeEvent(self, event):
        self.isClose.emit(True)

class ProfileTable(QTableWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.__setStyle()
        
    def __setStyle(self):
        width = self.parent().width()
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels(['Username', 'Password', 'Name', 'Status', '', ''])
        self.setColumnWidth(0, int(width/6))
        self.setColumnWidth(1, int(width/6))
        self.setColumnWidth(2, int(width/6))
        self.setColumnWidth(3, int(width/6))
        self.setColumnWidth(4, int(width/6))
        self.setColumnWidth(5, int(width/6))
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)

class ButtonBox(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.buttonBoxLayout = QHBoxLayout()

        self.btnAddProfile = QPushButton('Add profile')
        self.btnAddProfile.setObjectName('btnAddProfile')
        self.btnQuit = QPushButton('Quit')
        self.btnQuit.setObjectName('btnQuit')
        self.btnQuit.clicked.connect(lambda : self._onBtnQuitClick())

        self.buttonBoxLayout.addWidget(self.btnQuit)
        self.buttonBoxLayout.addWidget(self.btnAddProfile)

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
            QPushButton#btnAddProfile {
                background-color: rgba(0, 167, 78, 1);
                color: rgb(225, 225, 255);
            }
            QPushButton#btnAddProfile::hover {
                background-color: rgba(0, 167, 78, 0.75);
            }
        ''')
    
    def _onBtnQuitClick(self):
        self.parent().close()
