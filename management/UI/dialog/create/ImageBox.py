from functools import partial

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from ....CONSTANTS import PATH_DIALOG_STYLE
from ....helper import _getExactlyPath

class ImageCard(QWidget):
    def __init__(self, url, parent = None):
        super().__init__(parent)
        layout = QVBoxLayout()
        label = QLabel()
        label.setObjectName('imagecard')
        pixmap = QPixmap(url)
        pixmap = pixmap.scaled(120, 120)
        label.setPixmap(pixmap)
        layout.addWidget(label)
        self.setLayout(layout)
        self._setStyle()
    
    def _setStyle(self):
        self.setFixedSize(120, 120)

class ImageList(QWidget):
    def __init__(self, urls, parent = None):
        super().__init__(parent)
        layout = QGridLayout()

        rows = int(len(urls)/4)
        if int(len(urls)%4) > 0:
            rows += 1
        urlsReduce = len(urls)
        urlsIndex = 0
        for row in range(0, rows):
            for col in range(0, 4):
                layout.addWidget(ImageCard(urls[urlsIndex]), row, col, 1, 1)
                urlsReduce -= 1
                urlsIndex += 1
                if urlsReduce <= 0:
                    break
        self.setLayout(layout)

class DragAndDrop(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.centralLayout = QGridLayout()
        self._dropZone()
        
        self.setLayout(self.centralLayout)
        self.files = []

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            self.files.append(f)
        self._removeImageCard()
        self.centralLayout.addWidget(ImageList(self.files))

    def _dropZone(self):
        label = QLabel('<h3>Drag & drop image here</h3>')
        label.setObjectName('dropzone')
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFixedHeight(300) 
        self.centralLayout.addWidget(label)
    
    def _clearUrls(self):
        self.files = []
        self._removeImageCard()
        self._dropZone()

    def _removeImageCard(self):
        for i in reversed(range(self.centralLayout.count())):
            self.centralLayout.itemAt(i).widget().setParent(None)

    def _getUrls(self):
        return self.files
    
class ImageBox(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        layout = QVBoxLayout()
        
        self.dragAndDrop = DragAndDrop()
        clearBtn = QPushButton('Clear all images')
        clearBtn.setObjectName('clearimagebtn')
        clearBtn.clicked.connect(partial(self._resetValues))
        layout.addWidget(self.dragAndDrop)
        layout.addWidget(clearBtn)
        self.setLayout(layout)
        self._setStyle()
    
    def _setStyle(self):
        self.setFixedHeight(400)
        with open(_getExactlyPath(PATH_DIALOG_STYLE), 'r') as f:
            style = f.read()
        self.setStyleSheet(style)
    
    def _getValues(self):
        return self.dragAndDrop._getUrls()

    def _resetValues(self):
        self.dragAndDrop._clearUrls()

