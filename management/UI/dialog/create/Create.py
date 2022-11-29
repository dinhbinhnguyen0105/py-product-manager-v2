import os
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QScrollArea,
    QProgressBar
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QObject, QThread, pyqtSignal

from .ImageBox import ImageBox
from .InputField import InputField
from .ButtonBox import ButtonBox
from ....Google.Drive import Drive
from ....APIs.APIs import POST

from ....CONSTANTS import PATH_ICON_CREATE, PATH_FOLDER_OF_IMAGES

from ....helper import _getExactlyPath
from ....helper import _initFolderName
from ....helper import _createFolder
from ....helper import _copyImages

class Create(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.mainLayout = QVBoxLayout()

        self.imageBox = ImageBox(self)
        self.scrollArea = QScrollArea()
        self.scrollArea.setStyleSheet('border: none;')
        self.inputField = InputField()
        self.scrollArea.setWidget(self.inputField)
        self.buttonBox = ButtonBox()
        self.buttonBox.btnSave.clicked.connect(lambda : self._onClickSave())


        self.mainLayout.addWidget(self.imageBox)
        self.mainLayout.addWidget(self.scrollArea)
        self.mainLayout.addWidget(self.buttonBox)
        self.setLayout(self.mainLayout)

        self._setStyle()

    def _setStyle(self):
        self.setWindowTitle('Create product')
        self.setStyleSheet('background-color: white;')
        iconURL = _getExactlyPath(PATH_ICON_CREATE)
        self.setWindowIcon(QIcon(iconURL))
        self.setFixedSize(500, 900)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.setAlignment(self.imageBox,Qt.AlignmentFlag.AlignTop)
    
    def _onClickSave(self):
        inputValues = self.inputField._getValues()
        imageValues = self.imageBox._getValues()
        self._handleUpload(inputValues, imageValues)

    def _handleUpload(self, input={}, imageUrls=[]):
        self.thread = QThread(self)
        self.worker = Worker(input, imageUrls)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.thread.finished.connect(self.thread.deleteLater)

        self.worker.progress.connect(self._reportProgress)
        self.worker.finished.connect(self._reportFinish)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.thread.quit)

        self.thread.start()
        self.buttonBox.btnSave.setDisabled(True)
        self.buttonBox.btnQuit.setDisabled(True)
        self.pBar = QProgressBar(self)
        self.mainLayout.addWidget(self.pBar)

        self.thread.finished.connect(lambda : self.buttonBox.btnSave.setEnabled(True))
        self.thread.finished.connect(lambda : self.buttonBox.btnQuit.setEnabled(True))
        self.thread.finished.connect(lambda : self.inputField._resetValues())
        self.thread.finished.connect(lambda : self.imageBox._resetValues())
        # self.thread.finished.connect(lambda : self.__handlePost(self.payload))


    def _reportProgress(self,e):
        self.pBar.setValue(e)

    def _reportFinish(self, e):
        print(e)
        self.pBar.setParent(None)


class Worker(QObject):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    def __init__(self, input={}, imageUrls=[], parent=None):
        super().__init__(parent)
        self.drive = Drive()
        self.input = input
        self.imageUrls = imageUrls
    
    def run(self):
        step = 0

        folderName = _initFolderName(self.input['category'], self.input['street_name'], self.input['acreage'], self.input['price'])
        pathFolder = _createFolder(_getExactlyPath(PATH_FOLDER_OF_IMAGES), folderName)
        pathFolderImagesForSell = _createFolder(pathFolder, 'images_for_sell')
        step = self.__sendMsg(step)
        imageUrlsCopied = _copyImages(self.imageUrls, pathFolder)
        step = self.__sendMsg(step)
        
        if self.drive._searchFolder(folderName):
            driveFolderId = self.drive._searchFolder(folderName)[0]['id']
        else:
            driveFolderId = self.drive._createFolder(folderName)
        step = self.__sendMsg(step)

        image = []
        for imageUrl in imageUrlsCopied:
            driveImageId = self.drive._uploadItem(driveFolderId, imageUrl)
            image.append({imageUrl.split(os.sep)[-1] : driveImageId})

            step = self.__sendMsg(step)

        self.input['folderId'] = str({folderName : driveFolderId})
        self.input['imageIds'] = '|'.join(map(str, image))

        res = POST(wsName='products', action='add', payload=self.input)
        step = self.__sendMsg(step)
        self.finished.emit(res)

    def __sendMsg(self, step):
        total = len(self.imageUrls)  + 4
        self.progress.emit(int((step /total) * 100))
        return step + 1