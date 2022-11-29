from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
)

from ....CONSTANTS import PATH_MAIN_STYLE
from ....helper import _getExactlyPath

class ButtonBox(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        layout = QHBoxLayout()

        self.btnNext = QPushButton('Next')
        self.btnNext.setObjectName('btnNext')
        self.btnPrev = QPushButton('Prev')
        self.btnPrev.setObjectName('btnPrev')

        layout.addWidget(self.btnPrev)
        layout.addWidget(self.btnNext)
        
        self.setLayout(layout)
        layout.setContentsMargins(0,0,0,0)
        self.__setStyle()
    
    def __setStyle(self):
        with open(_getExactlyPath(PATH_MAIN_STYLE), 'r') as f:
            style = f.read()
        
        self.setStyleSheet(style)
