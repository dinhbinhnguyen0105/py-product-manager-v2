from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QWidget,
    QGridLayout,
    QHBoxLayout,
    QComboBox,
    QFrame,
    QLineEdit,
    QPushButton,
    QLabel,
    QCheckBox,
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, pyqtSignal, QThread

from .ProfileManager import ProfileManager
from .ItemManager import ItemManager
from .ControlTable import ControlTable
from .Bot import Bot
from ....CONSTANTS import PATH_ICON_ROBOTCONTROL
from ....helper import _getExactlyPath

class RobotControl(QDialog):
    isShowed = pyqtSignal(bool)
    isDelayCycleFinised = pyqtSignal(bool)
    isdelayGroupFinised = pyqtSignal(bool)
    isBotFinised = pyqtSignal(bool)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.__setStyle() 

        self.control = Control()
        self.buttonBox = ButtonBoxDialog(self)
        self.buttonBox.btnRun.clicked.connect(lambda : self.__btnRunOnClick())



        self.layout.addWidget(self.control)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def __setStyle(self):
        self.setWindowTitle('Robot Control')
        self.setStyleSheet('''
            QDialog {
                background-color: white;
            }
            QLineEdit {
                padding: 5px 28px 5px 11px;
                font-size: 14px;
                line-height: 20px;
                min-height: 20px;
                background-color: rgb(255, 255, 255);
                color: rgb(44, 44, 44);
                outline: none;
                border: 1px solid rgb(204, 204, 204);
                border-radius: 4px;
            }
        ''')
        iconURL = _getExactlyPath(PATH_ICON_ROBOTCONTROL)
        self.setWindowIcon(QIcon(iconURL))
        self.setFixedSize(750, 500)
        self.layout.setContentsMargins(0,0,0,0)

    def __btnRunOnClick(self):
        def reportProgress(e):
            print(e)
            pass
        def reportFinished(e):
            print(e)
            pass
        def reportChangeAccount(e):
            self.control.setting.lineEditChangeAccount.setText(str(e))
            pass
        def reportsellDelay(e):
            self.control.setting.lineEditSellDelay.setText(str(e))
            pass
        def reportDelayTime(e):
            if e['action'] == 'newfeed':
                self.control.setting.lineEditNewfeed.setText(str(e['time']))
            elif e['action'] == 'video':
                self.control.setting.lineEditVideo.setText(str(e['time']))
            elif e['action'] == 'groupFeed':
                self.control.setting.lineEditGroupFeed.setText(str(e['time']))

        profiles = self.control.table._getValues()
        payload = self.control._getValues()
        payload['profiles'] = profiles

        self.botThread = QThread(self)
        self.bot  = Bot(payload)
        self.bot.moveToThread(self.botThread)

        self.botThread.started.connect(self.bot.run)
        self.botThread.started.connect(self.botThread.deleteLater)

        self.bot.progress_msg.connect(reportProgress)
        self.bot.changeAccount.connect(reportChangeAccount)
        self.bot.sellDelay.connect(reportsellDelay)
        self.bot.delayTime.connect(reportDelayTime)
        self.bot.finished.connect(reportFinished)
        self.bot.finished.connect(self.botThread.quit)
        self.bot.finished.connect(self.botThread.deleteLater)
        self.bot.finished.connect(self.bot.deleteLater)

        self.botThread.start()
        
        

    def showEvent(self, event):
        self.control.table.isReload.emit(True)

class Control(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.mainLayout = QVBoxLayout()
        self.btnBox = ButtonBoxControl()

        self.setting = Setting()
        self.table = ControlTable()
        self.btnBox.itemManager.isClose.connect(lambda : self.table.isReload.emit(True))
        self.btnBox.profileManager.isClose.connect(lambda : self.table.isReload.emit(True))


        self.mainLayout.addWidget(self.btnBox)
        self.mainLayout.addWidget(self.setting)
        self.mainLayout.addWidget(self.table)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.mainLayout)
    
    def _getValues(self):
        settingObj = {}
        if self.setting.comboboxWorkingMode.currentIndex() == 1:
            settingObj = {
                'sell_delay': self.setting.lineEditSellDelay.text(),
                'change_account': self.setting.lineEditChangeAccount.text(),
                'hidden_browser': self.setting.checkboxHiddenBrowser.isChecked()
            }
            return {
                'action' : 'sell',
                'setting': settingObj
            }
        elif self.setting.comboboxWorkingMode.currentIndex() == 0:
            settingObj = {
                'change_account': self.setting.lineEditChangeAccount.text(),
                'hidden_browser': self.setting.checkboxHiddenBrowser.isChecked(),
                'newfeed': self.setting.lineEditNewfeed.text(),
                'rell': self.setting.lineEditReel.text(),
                'video': self.setting.lineEditVideo.text(),
                'groupFeed': self.setting.lineEditGroupFeed.text(),
                'notification': self.setting.checkboxNotification.isChecked(),
            }
            return {
                'action' : 'care',
                'setting': settingObj
            }

class Setting(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.settingLayout = QHBoxLayout()
        self.config1()
        self.config2()

        self.setLayout(self.settingLayout)
        self.__setStyle()
    
    def __setStyle(self):
        self.settingLayout.setContentsMargins(0, 0, 0, 0)

        pass
    def config1(self):
        def __handleChangeAccount():
            if self.checkboxChangeAccount.isChecked() :
                self.holderChangeAccount.setParent(None)
                self.configLayout1.addWidget(self.lineEditChangeAccount, 2, 1)
            else:
                self.lineEditChangeAccount.setParent(None)
                self.configLayout1.addWidget(self.holderChangeAccount, 2, 1)
        def __handleWorkingMode(e):
            if e == 1:
                
                self.lineEditSellDelay.setPlaceholderText('seconds')
                self.configLayout1.addWidget(self.labelSellDelay, 1, 0)
                self.configLayout1.addWidget(self.lineEditSellDelay, 1, 1)
            else:
                self.labelSellDelay.setParent(None)
                self.lineEditSellDelay.setParent(None)

        self.configWidget1 = QFrame()
        self.configLayout1 = QGridLayout()

        self.labelWorkingMode = QLabel('Working mode')
        self.comboboxWorkingMode = QComboBox()
        self.comboboxWorkingMode.addItem('Take care')
        self.comboboxWorkingMode.addItem('Auto sell')
        self.labelSellDelay = QLabel('Delay auto sell')
        self.lineEditSellDelay = QLineEdit()
        self.comboboxWorkingMode.currentIndexChanged.connect(__handleWorkingMode)
        self.configLayout1.addWidget(self.labelWorkingMode, 0, 0)
        self.configLayout1.addWidget(self.comboboxWorkingMode, 0, 1)


        self.checkboxChangeAccount = QCheckBox('Change Account')
        self.checkboxChangeAccount.stateChanged.connect(lambda : __handleChangeAccount())
        self.lineEditChangeAccount = QLineEdit()
        self.lineEditChangeAccount.setPlaceholderText('seconds')
        self.holderChangeAccount = QLabel()
        self.configLayout1.addWidget(self.checkboxChangeAccount, 2, 0)

        self.checkboxHiddenBrowser = QCheckBox('Hidden Browser')
        self.configLayout1.addWidget(self.checkboxHiddenBrowser, 3, 0)
    
        self.configWidget1.setLayout(self.configLayout1)
        self.configWidget1.setFixedWidth(325)
        self.settingLayout.addWidget(self.configWidget1)
    
    
    def config2(self):
        def __handleNewFeed():
            if self.checkboxNewfeed.isChecked() :
                self.holderNewfeed.setParent(None)
                self.configLayout2.addWidget(self.lineEditNewfeed, 0, 1)
            else:
                self.lineEditNewfeed.setParent(None)
                self.configLayout2.addWidget(self.holderNewfeed, 0, 1)
        def __handleReel():
            if self.checkboxReel.isChecked() :
                self.holderReel.setParent(None)
                self.configLayout2.addWidget(self.lineEditReel, 1, 1)
            else:
                self.lineEditReel.setParent(None)
                self.configLayout2.addWidget(self.holderReel, 1, 1)
        def __handleVideo():
            if self.checkboxVideo.isChecked() :
                self.holderVideo.setParent(None)
                self.configLayout2.addWidget(self.lineEditVideo, 2, 1)
            else:
                self.lineEditVideo.setParent(None)
                self.configLayout2.addWidget(self.holderVideo, 2, 1)
        def __handleGroupFeed():
            if self.checkboxGroupFeed.isChecked() :
                self.holderGroupFeed.setParent(None)
                self.configLayout2.addWidget(self.lineEditGroupFeed, 4, 1)
            else:
                self.lineEditGroupFeed.setParent(None)
                self.configLayout2.addWidget(self.holderGroupFeed, 4, 1)

        self.configWidget2 = QFrame()
        self.configLayout2 = QGridLayout()

        self.checkboxNewfeed = QCheckBox('Newfeed')
        self.checkboxNewfeed.stateChanged.connect(lambda : __handleNewFeed())
        self.lineEditNewfeed = QLineEdit()
        self.lineEditNewfeed.setPlaceholderText('seconds')
        self.holderNewfeed = QLabel()
        self.configLayout2.addWidget(self.checkboxNewfeed,0, 0)

        self.checkboxReel = QCheckBox('Reel')
        self.checkboxReel.stateChanged.connect(lambda : __handleReel())
        self.lineEditReel = QLineEdit()
        self.lineEditReel.setPlaceholderText('amounts')
        self.holderReel = QLabel()
        self.configLayout2.addWidget(self.checkboxReel, 1, 0)

        self.checkboxVideo = QCheckBox('Video')
        self.checkboxVideo.stateChanged.connect(lambda : __handleVideo())
        self.lineEditVideo = QLineEdit()
        self.lineEditVideo.setPlaceholderText('amounts')
        self.holderVideo = QLabel()
        self.configLayout2.addWidget(self.checkboxVideo, 2, 0)

        self.checkboxNotification = QCheckBox('Notification')
        self.configLayout2.addWidget(self.checkboxNotification, 3, 0)

        self.checkboxGroupFeed = QCheckBox('Group Feed')
        self.checkboxGroupFeed.stateChanged.connect(lambda : __handleGroupFeed())
        self.lineEditGroupFeed = QLineEdit()
        self.lineEditGroupFeed.setPlaceholderText('seconds')
        self.holderGroupFeed = QLabel()
        self.configLayout2.addWidget(self.checkboxGroupFeed, 4, 0)

        self.configWidget2.setLayout(self.configLayout2)
        self.configWidget2.setFixedWidth(325)

        self.settingLayout.addWidget(self.configWidget2)

class ButtonBoxControl(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.btnBoxLayout = QHBoxLayout()

        self.profileManager = ProfileManager()
        self.btnProfileManager = QPushButton('Profiles')
        self.btnProfileManager.clicked.connect(lambda : self._onProfileManagerClick())
        self.itemManager = ItemManager()
        self.btnItemsForSellManager = QPushButton('Items')
        self.btnItemsForSellManager.clicked.connect(lambda : self._onItemManagerClick())
        self.btnMsgManager = QPushButton('Messages')

        self.btnBoxLayout.addWidget(self.btnProfileManager)
        self.btnBoxLayout.addWidget(self.btnItemsForSellManager)
        self.btnBoxLayout.addWidget(self.btnMsgManager)
        self.setLayout(self.btnBoxLayout)
        self.__setStyle()
    
    def __setStyle(self):
        self.btnBoxLayout.setContentsMargins(0, 0, 0, 0)
    
    def _onProfileManagerClick(self):
        self.profileManager.show()
        self.profileManager.isShow.emit(True)

    def _onItemManagerClick(self):
        self.itemManager.show()
        self.itemManager.isShow.emit(True)  

class ButtonBoxDialog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.btnBoxLayout = QHBoxLayout()
        self.btnQuit = QPushButton('Quit')
        self.btnQuit.clicked.connect(lambda : self.parent().close())
        self.btnRun = QPushButton('Run')
        self.btnBoxLayout.addWidget(self.btnQuit)
        self.btnBoxLayout.addWidget(self.btnRun)
        self.setLayout(self.btnBoxLayout)