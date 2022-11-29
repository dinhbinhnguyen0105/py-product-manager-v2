from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
)
from ....CONSTANTS import PATH_DIALOG_STYLE
from ....helper import _getExactlyPath

class LineText(QWidget):
    def __init__(self, label = '', key = '', prevValue = '', placeholder = '', parent = None):
        super().__init__(parent)
        self.key = key
        self.prevValue = prevValue
        layout = QVBoxLayout()
        _label = QLabel(label)
        _label.setObjectName('_label')
        self.inputField = QLineEdit()
        self._setValue()
        layout.addWidget(_label)
        layout.addWidget(self.inputField)
        self.__setStyle()
        self.setLayout(layout)
    
    def _getValue(self):
        return {
            self.key : self.inputField.text()
        }
    def _setValue(self):
        self.inputField.setText(self.prevValue)

    
    def __setStyle(self):
        self.setFixedHeight(65)

        self.inputField.setFixedHeight(32)
        with open(_getExactlyPath(PATH_DIALOG_STYLE), 'r') as f:
            style = f.read()
        self.setStyleSheet(style)