from PyQt6.QtWidgets import (
    QWidget,
    QComboBox,
    QVBoxLayout,
    QLabel
)

from ....helper import _getExactlyPath
from ....CONSTANTS import PATH_DIALOG_STYLE

class ListItem(QComboBox):
    def __init__(self, items = [], default_item = '', parent = None):
        super().__init__(parent)
        for index in range(0, len(items)):
            self.addItem(items[index])
            if items[index] == default_item:
                self.setCurrentIndex(index)

class DropDownMenu(QWidget):
    def __init__(self, menu_label ='', key = '', items = [], default_item = '',  parent = None):
        super().__init__(parent)
        self.key = key

        self.__setStyle()
        layout = QVBoxLayout()
        _label = QLabel(menu_label)
        _label.setObjectName('_label')
        self.dropDownMenu = ListItem(items, default_item)
        layout.addWidget(_label)
        layout.addWidget(self.dropDownMenu)
        self.setLayout(layout)

    def _getValue(self):
        return {
            self.key : self.dropDownMenu.currentText()
        }

    def __setStyle(self):
        self.setFixedHeight(65)
        with open(_getExactlyPath(PATH_DIALOG_STYLE), 'r') as f:
            style = f.read()
        self.setStyleSheet(style)