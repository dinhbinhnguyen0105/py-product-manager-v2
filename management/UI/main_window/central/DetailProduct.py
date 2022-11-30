import os
from shutil import rmtree
import json
import subprocess
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QFrame,
    QPushButton,
    QHBoxLayout,
    QWidget,
    QGridLayout,
    QLabel,
    QGridLayout,
    QPlainTextEdit
)
from PyQt6.QtGui import QPixmap

from ....CONSTANTS import (
    PATH_MAIN_STYLE,
    PATH_INFO_TEMPLATE,
)

from ...dialog import initItem
from ....APIs.APIs import DELETE
from ....helper import _getExactlyPath
from ....helper import _randomIcon

class ImageCard(QWidget):
    def __init__(self, url, parent = None):
        super().__init__(parent)
        layout = QVBoxLayout()
        label = QLabel()
        label.setObjectName('imagecard')
        pixmap = QPixmap(url)
        pixmap = pixmap.scaled(100, 100)
        label.setPixmap(pixmap)
        layout.addWidget(label)
        self.setLayout(layout)
        self._setStyle()
    
    def _setStyle(self):
        self.setFixedSize(100, 100)

class ImageList(QWidget):
    def __init__(self, urls, parent = None):
        super().__init__(parent)
        layout = QGridLayout()
        displayImages = []

        if len(urls) > 8:
            for i in range(8):
                displayImages.append(urls[i])
        else:
            displayImages = urls

        rows = int(len(displayImages)/4)
        if int(len(displayImages)%4) > 0:
            rows += 1
        urlsReduce = len(displayImages)
        urlsIndex = 0
        for row in range(0, rows):
            for col in range(0, 4):
                layout.addWidget(ImageCard(displayImages[urlsIndex]), row, col, 1, 1)
                urlsReduce -= 1
                urlsIndex += 1
                if urlsReduce <= 0:
                    break
        self.setLayout(layout)

class DefaultInfo(QFrame):
    def __init__(self, payload, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        self.detailInfo = QPlainTextEdit()

        self.detailInfo.setPlainText(self._loadDefaultInfo(payload))
        layout.addWidget(self.detailInfo)
        self.setLayout(layout)
    
    def _loadDefaultInfo(self, payload):
        pathInfoTemplate = _getExactlyPath(PATH_INFO_TEMPLATE)
        if os.path.exists(pathInfoTemplate):
            with open(pathInfoTemplate, 'r', encoding='utf8') as f:
                infoTemplate = json.load(f)
            
            if payload['Category'] == 'Đất': 
                defaultInfo = infoTemplate['default_info_dat']
            else:
                defaultInfo = infoTemplate['default_info']
            icons = infoTemplate['icons']
            contact = infoTemplate['contact']

            defaultInfo = defaultInfo.replace('{icon}', _randomIcon(icons))
            defaultInfo = defaultInfo.replace('{category}', payload['Category'])
            defaultInfo = defaultInfo.replace('{price}', str(payload['Price']))
            defaultInfo = defaultInfo.replace('{ward}', payload['Ward'])
            defaultInfo = defaultInfo.replace('{district}', payload['District'])
            defaultInfo = defaultInfo.replace('{contact}', contact)
            defaultInfo = defaultInfo.replace('{street_name}', payload['Street name'])
            defaultInfo = defaultInfo.replace('{acreage}', str(payload['Acreage']))
            defaultInfo = defaultInfo.replace('{construction}', payload['Construction'])
            defaultInfo = defaultInfo.replace('{function}', payload['Function'])
            defaultInfo = defaultInfo.replace('{fuiture}', payload['Fuiture'])
            defaultInfo = defaultInfo.replace('{building_line}', payload['Building line'])
            defaultInfo = defaultInfo.replace('{legal}', payload['Legal'])
            defaultInfo = defaultInfo.replace('{description}', payload['Description'])

        return defaultInfo

class ButtonBox(QWidget):
    def __init__(self, payload, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        self.payload = payload

        self.btnInit = QPushButton('Init')
        self.btnInit.setObjectName('btnOpen')
        self.btnInit.clicked.connect(lambda : self._onBtnInitClick())
        self.btnEdit = QPushButton('Edit')
        self.btnEdit.setObjectName('btnEdit')
        self.btnEdit.clicked.connect(lambda : self._onBtnEditClick())
        self.btnRemove = QPushButton('Remove')
        self.btnRemove.setObjectName('btnRemove')
        self.btnRemove.clicked.connect(lambda : self._onBtnRemoveClick())
        self.btnOpenImageFolder = QPushButton('Folder')
        self.btnOpenImageFolder.setObjectName('btnOpenImageFolder')
        self.btnOpenImageFolder.clicked.connect(lambda : self._onbtnOpenImageFolderClick())

        layout.addWidget(self.btnInit) 
        layout.addWidget(self.btnEdit) 
        layout.addWidget(self.btnRemove)
        layout.addWidget(self.btnOpenImageFolder)

        self.setLayout(layout)

    def _onBtnInitClick(self):
        self.initDialog = initItem.InitItem(self.payload)
        self.initDialog.show()
        pass
    def _onBtnEditClick(self):

        pass
    def _onBtnRemoveClick(self):
        _id = self.payload['ID']
        _folder = self.payload['Folder path']
        rmtree(_folder)
        res = DELETE(_id)
        print(f'Delete {_id}: {res}')

    def _onbtnOpenImageFolderClick(self):
        pathFolderImage = self.payload['Folder path'] + os.sep
        subprocess.Popen(rf'explorer /select, {pathFolderImage}')


class DetailProduct(QFrame):
    def __init__(self, payload, parent=None):
        super().__init__(parent)
        _height = self.parent().height()

        self.centralLayout = QVBoxLayout()
        self.imageList = ImageList(payload['Image path'], self)
        self.imageList.setFixedHeight(int(_height* 0.4))
        self.info = DefaultInfo(payload)
        self.info.setFixedHeight(int(_height* 0.4))
        self.buttonBox = ButtonBox(payload)
        self.buttonBox.setFixedHeight(int(_height* 0.2))

        self.centralLayout.addWidget(self.imageList)
        self.centralLayout.addWidget(self.info)
        self.centralLayout.addWidget(self.buttonBox)
        self.setLayout(self.centralLayout)

        self.__setStyle()
    def __setStyle(self):
        with open(_getExactlyPath(PATH_MAIN_STYLE), 'r') as f:
            style = f.read()
        self.setStyleSheet(style)