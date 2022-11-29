from PyQt6.QtWidgets import (
    QVBoxLayout,
    QFrame,
    QMainWindow,
    QPushButton,
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from ....CONSTANTS import (
    PATH_ICON_PLUS,
    PATH_ICON_BOOKMARK,
    PATH_ICON_ROBOTCONTROL,
    PATH_MAIN_STYLE
)
from ....helper import _getExactlyPath

class SideBar(QFrame):
    def __init__(self, parent=QMainWindow):
        super().__init__(parent)
        self.setFixedSize(int(self.parent().width() * 0.2), self.parent().height())
        self.layout = QVBoxLayout()

        pathIconPlus = _getExactlyPath(PATH_ICON_PLUS)
        self.btnCreateNewListing = QPushButton('Create new listing')
        self.btnCreateNewListing.setIcon(QIcon(pathIconPlus))
        self.btnCreateNewListing.setObjectName('btnCreateNewListing')
        pathIconBookmark = _getExactlyPath(PATH_ICON_BOOKMARK)
        self.btnProductTemplate = QPushButton('Product template')
        self.btnProductTemplate.setIcon(QIcon(pathIconBookmark))
        self.btnProductTemplate.setObjectName('btnProductTemplate')
        pathIconRobotControl = _getExactlyPath(PATH_ICON_ROBOTCONTROL)
        self.btnRobotControl = QPushButton('Robot control')
        self.btnRobotControl.setIcon(QIcon(pathIconRobotControl))
        self.btnRobotControl.setObjectName('btnRobotControl')

        self.layout.addWidget(self.btnCreateNewListing)
        self.layout.addWidget(self.btnProductTemplate)
        self.layout.addWidget(self.btnRobotControl)
        self.setLayout(self.layout)

        self._setStyles()       
    
    def _setStyles(self):
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setStyleSheet('''
            QPushButton {
                height: 36px;
                margin: 12px;
                padding-left: 50px;
                border: None;
                border-radius: 6px;
                font-weight: bold;
                background-color: rgb(231, 243, 255);
                color: rgb(24, 119, 242);
                text-align: left;
            }
            QPushButton::hover {
                background-color: rgb(211, 222, 232);
            }
        ''')
