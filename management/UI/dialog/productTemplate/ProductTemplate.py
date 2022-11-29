import os
import json
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QWidget,
    QPlainTextEdit,
    QLineEdit
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, pyqtSignal
from .ButtonBox import ButtonBox
from ....CONSTANTS import PATH_ICON_PRODUCT_TEMPLATE, PATH_PRODUCT_TEMPLATE
from ....helper import _getExactlyPath

class Body(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        self.header = QPlainTextEdit()
        self.header.setPlaceholderText('Header')
        self.description = QPlainTextEdit()
        self.description.setPlaceholderText('Description')
        self.contact = QLineEdit()
        self.contact.setPlaceholderText('Contact')

        layout.addWidget(self.header)
        layout.addWidget(self.description)
        layout.addWidget(self.contact)
        self.setLayout(layout)
    pass

class ProductTemplate(QDialog):
    isShowed = pyqtSignal(bool)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pathProductTemplate = _getExactlyPath(PATH_PRODUCT_TEMPLATE)

        self.layout = QVBoxLayout()

        self.body = Body()
        self.buttonBox = ButtonBox()
        self.buttonBox.btnSave.clicked.connect(lambda : self.__writeData())
        self.layout.addWidget(self.body)
        self.layout.addWidget(self.buttonBox)

        self.setLayout(self.layout)
        self.__setStyle()

    def __setStyle(self):
        self.setWindowTitle('Product template')
        self.setStyleSheet('background-color: white;')
        iconURL = _getExactlyPath(PATH_ICON_PRODUCT_TEMPLATE)
        self.setWindowIcon(QIcon(iconURL))
        self.setFixedSize(500, 300)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def __loadData(self):
        if os.path.exists(self.pathProductTemplate):
            try:
                with open(self.pathProductTemplate, 'r', encoding='utf8') as f:
                    productTemplate = json.load(f)
                return productTemplate
            except json.decoder.JSONDecodeError as e:
                print(e)
                return None
        else:
            return None

    def __writeData(self):
        header = self.body.header.toPlainText()
        description = self.body.description.toPlainText()
        contact = self.body.contact.text()
        productTemplate = self.__loadData()
        try:
            _header = productTemplate['headers']
            _description = productTemplate['descriptions']
            _contact = productTemplate['contacts']
        except KeyError:
            _header = []
            _description = []
            _contact = []

        _header.append(header)
        _description.append(description)
        _contact.append(contact)

        productTemplate['headers'] = _header
        productTemplate['descriptions'] = _description
        productTemplate['contacts'] = _contact
        with open(_getExactlyPath(PATH_PRODUCT_TEMPLATE), 'w', encoding='utf8') as f:
            json.dump(productTemplate, f)