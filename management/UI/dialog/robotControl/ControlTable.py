import os
import json
import sys
from time import sleep

from PyQt6.QtWidgets import (
    QVBoxLayout,
    QTableWidget,
    QHeaderView,
    QTableWidgetItem,
    QWidget,
    QPushButton,
    QCheckBox,
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QObject

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import InvalidSessionIdException, WebDriverException

from ....CONSTANTS import PATH_PROFILE_CONFIG, PATH_CHROME, PATH_CHROMEDRIVER, PATH_PROFILES_BROWSER
from ....helper import _getExactlyPath

class ControlTable(QWidget):
    isReload = pyqtSignal(bool)
    def __init__(self,  parent=None):
        super().__init__(parent)
        self.pathProfileConfig = _getExactlyPath(PATH_PROFILE_CONFIG)
        self.mainLayout = QVBoxLayout()
        self.__setStyle()
        
        self.table = Table(self)
        self.isReload.connect(lambda : self.__fillTable())

        self.mainLayout.addWidget(self.table)
        self.setLayout(self.mainLayout)
    
    def __setStyle(self):
        pass

    def __fillTable(self):
        profiles = self.__loadProfile()
        for i in range(self.table.rowCount()):
            self.table.removeRow(0)
               
        if profiles is not None:
            for profile in profiles.values():
                rowPosition = self.table.rowCount()
                self.table.insertRow(rowPosition)
                _name = QTableWidgetItem(profile['name'])
                _status = QTableWidgetItem(profile['status'])
                _select = QCheckBox()
                self.openBtn = QPushButton('Open')

                _name.setFlags(Qt.ItemFlag.ItemIsEditable)
                _status.setFlags(Qt.ItemFlag.ItemIsEditable)


                self.table.setItem(rowPosition, 0, _name)
                self.table.setItem(rowPosition, 1, _status)
                self.table.setCellWidget(rowPosition, 2, _select)
                self.table.setCellWidget(rowPosition, 3, self.openBtn)

                self.openBtn.clicked.connect(lambda : self.__onOpenClick(self.table.currentRow()))
    
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

    def __onOpenClick(self, row):
        def reportFinished(e):
            print(e)

        profiles = self.__loadProfile()
        _name = self.table.item(row, 0).text()

        for profile in profiles.values():
            if profile['name'] == _name:
                _username = profile['username']
                break

        print(f'Username: {_username} - Name: {_name}')

        self.openBrowserThread = QThread(self)
        self.openBrowser = OpenBrowser({'username' : _username, 'name': _name})
        self.openBrowser.moveToThread(self.openBrowserThread)

        self.openBrowserThread.started.connect(self.openBrowser.run)
        self.openBrowserThread.finished.connect(self.openBrowserThread.deleteLater)

        self.openBrowser.finished_msg.connect(reportFinished)
        self.openBrowser.finished_msg.connect(self.openBrowserThread.quit)
        self.openBrowser.finished_msg.connect(self.openBrowserThread.deleteLater)
        self.openBrowser.finished_msg.connect(self.openBrowser.deleteLater)

        self.openBrowserThread.start()

    def _getValues(self):
        _row = self.table.rowCount()
        profiles = self.__loadProfile()
        _profiles = {}
        _names = []
        for i in range(_row):
            if self.table.cellWidget(i, 2).isChecked():
                _names.append(self.table.item(i, 0).text())
        for _name in _names:
            for profile in profiles.values():
                if profile['name'] == _name:
                    _profiles[profile['username']] = profile
                    continue
        return _profiles

class Table(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__setStyle()
        
    def __setStyle(self):
        width = self.parent().width()
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(['Username', 'Status', 'Select', 'Login'])
        self.setColumnWidth(0, int(width/5*2))
        self.setColumnWidth(1, int(width/5))
        self.setColumnWidth(2, int(width/5))
        self.setColumnWidth(3, int(width/5))
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)

class OpenBrowser(QObject):
    progress_msg = pyqtSignal(dict)
    finished_msg = pyqtSignal(dict)
    def __init__(self, payload, parent=None):
        super().__init__(parent)
        self.username = payload['username']
    
    def run(self):
        self.__mainControl()
        self.finished_msg.emit({'status': 'closed', 'msg': 'browser window closed'})
    
    def __mainControl(self):
        if self.__initDriver():
            while True:
                try:
                    _ = self.driver.window_handles
                except InvalidSessionIdException as error:
                    return
                except WebDriverException as error:
                    return
                sleep(1)

    def __initDriver(self):
        self.urlLogin = 'https://www.facebook.com/login'
        self.urlCheckpoint = 'https://www.facebook.com/checkpoint/'
        self.urlProfile = 'https://www.facebook.com/profile.php'
        pathProfile = _getExactlyPath(PATH_PROFILES_BROWSER) + '\\' + f'profile_{self.username}'
        pathChromeDrive = _getExactlyPath(PATH_CHROMEDRIVER)
        options = Options()
        options.add_experimental_option('debuggerAddress', 'localhost:9223')
        options.add_argument('--disable-notifications')
        service = Service(pathChromeDrive)

        if os.path.exists(pathProfile) is False:
            os.mkdir(pathProfile)
        os.popen(f'"{PATH_CHROME}" --remote-debugging-port=9223 --user-data-dir="{pathProfile}"')
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.set_window_size(960, 1080)
        self.wait = WebDriverWait(self.driver, 10)
        
        self.driver.get(self.urlLogin)
        return True
