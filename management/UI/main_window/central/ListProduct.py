import os
import json
from PyQt6.QtWidgets import (
    QFrame,
    QWidget,
    QLineEdit,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QTableView
)
from PyQt6.QtCore import QSortFilterProxyModel,  QObject, QThread, pyqtSignal
from PyQt6.QtGui import QMovie, QStandardItemModel, QStandardItem

from ....CONSTANTS import (
    PATH_DATA,
    PATH_FOLDER_OF_IMAGES,
    PATH_LOADING_ANIMATION,
    PATH_MAIN_STYLE,
    FOLDER_KEY,
    IMAGE_KEY,
    HEADER
)
from ....APIs.APIs import GET
from ....Google.Drive import Drive
from ....helper import _getExactlyPath

class Table(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)

class ListProduct(QFrame): 
    currentProductChanged = pyqtSignal(object)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.centralLayout = QVBoxLayout()
        self._handleLoadData()
        
        self.model = QStandardItemModel()
        self.model.setColumnCount(len(HEADER))
        self.model.setHorizontalHeaderLabels(HEADER)
        self.filterProxyModel = SortFilterProxyModel()

        self.setLayout(self.centralLayout)

        with open(_getExactlyPath(PATH_MAIN_STYLE), 'r') as f:
            style = f.read()
        self.setStyleSheet(style)

    def _handleLoadData(self):
        self.thread = QThread(self)
        self.loadData = LoadData()
        self.loadData.moveToThread(self.thread)

        self.thread.started.connect(self.loadData.run)
        self.thread.finished.connect(self.thread.deleteLater)

        self.loadData.getAPIsStatus.connect(self._reportAPIsStatus)
        self.loadData.progress.connect(self._reportProgress)
        self.loadData.finished.connect(self._reportFinished)
        self.loadData.finished.connect(self.loadData.deleteLater)
        self.loadData.finished.connect(self.thread.quit)

        self.thread.start()
    
    def _reportAPIsStatus(self, e):
        if e is False:
            self.loadingScreen = LoadingScreen(self)
            self.centralLayout.addWidget(self.loadingScreen)
        else:
            self.centralLayout.removeWidget(self.loadingScreen)
            self.loadingScreen.deleteLater()
            self.loadingScreen = None
            self.table = Table(self)
            self.searchField = SearchField(self)
            self.centralLayout.addWidget(self.searchField)
            self.centralLayout.addWidget(self.table)

    def _reportProgress(self, e):
        _id = QStandardItem(str(e['ID']))
        _category = QStandardItem(str(e['Category']))
        _ward = QStandardItem(str(e['Ward']))
        _streetName = QStandardItem(str(e['Street name']))
        _acreage = QStandardItem(str(e['Acreage']))
        _price = QStandardItem(str(e['Price']))
        _legal = QStandardItem(str(e['Legal']))
        _buildingLine = QStandardItem(str(e['Building line']))

        rowPosition = self.model.rowCount()
        self.model.insertRow(rowPosition)

        self.model.setItem(rowPosition, 0, _id)
        self.model.setItem(rowPosition, 1, _category)
        self.model.setItem(rowPosition, 2, _ward)
        self.model.setItem(rowPosition, 3, _streetName)
        self.model.setItem(rowPosition, 4, _acreage)
        self.model.setItem(rowPosition, 5, _price)
        self.model.setItem(rowPosition, 6, _legal)
        self.model.setItem(rowPosition, 7, _buildingLine)

        self.filterProxyModel.setSourceModel(self.model)

        self.searchField.searchFieldId.textChanged.connect(lambda text, col=0: self.filterProxyModel.setFilterByColumn(text, col))
        self.searchField.searchFieldCategory.textChanged.connect(lambda text, col=1: self.filterProxyModel.setFilterByColumn(text, col))
        self.searchField.searchFieldWard.textChanged.connect(lambda text, col=2: self.filterProxyModel.setFilterByColumn(text, col))
        self.searchField.searchFieldStreetName.textChanged.connect(lambda text, col=3: self.filterProxyModel.setFilterByColumn(text, col))
        self.searchField.searchFieldAcreage.textChanged.connect(lambda text, col=4: self.filterProxyModel.setFilterByColumn(text, col))
        self.searchField.searchFieldPrice.textChanged.connect(lambda text, col=5: self.filterProxyModel.setFilterByColumn(text, col))

        self.table.setModel(self.filterProxyModel)
         
    def _reportFinished(self, e):
        with open(_getExactlyPath(PATH_DATA), 'w', encoding='utf8') as f:
            json.dump(e, f)
        self.table.selectionModel().selectionChanged.connect(lambda : self.onChange(e))

    def onChange(self, payload):
        currentRow = self.table.currentIndex().row()
        productId = self.table.model().index(currentRow, 0).data()
        try:
            currentProduct = payload[productId]
            self.currentProductChanged.emit(currentProduct)
        except KeyError:
            pass

class LoadData(QObject):
    progress = pyqtSignal(dict)
    getAPIsStatus = pyqtSignal(bool)
    finished = pyqtSignal(dict)
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def run(self):
        self.getAPIsStatus.emit(False)
        response = GET('products', 'list')
        self.getAPIsStatus.emit(True)

        drive = Drive()
        if not os.path.exists(_getExactlyPath(PATH_FOLDER_OF_IMAGES)):
            os.mkdir(_getExactlyPath(PATH_FOLDER_OF_IMAGES))
        for product in response.values():
            for folderName in product[FOLDER_KEY]:
                folderPath = _getExactlyPath(PATH_FOLDER_OF_IMAGES + os.sep + folderName)
                if not os.path.exists(folderPath):
                    os.mkdir(folderPath)
                product['Folder path'] = folderPath
                del product[FOLDER_KEY]
                imagePaths = []

                for images in product[IMAGE_KEY]:
                    for imageName in images:
                        imagePath = folderPath + os.path.join(os.sep, imageName)
                        imageId = images[imageName]
                        if not os.path.exists(imagePath):
                            drive._downloadImage(imageId, imagePath)
                            pass
                        imagePaths.append(imagePath)
                product['Image path'] = imagePaths
                del product[IMAGE_KEY]
                self.progress.emit(product)
        self.finished.emit(response)

class SearchField(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        _width = self.parent().width()
        self.centralLayout = QHBoxLayout()
        self.searchFieldId = QLineEdit()
        self.searchFieldId.setFixedWidth(int(_width/6))
        self.searchFieldId.setPlaceholderText('ID')
        self.searchFieldCategory = QLineEdit()
        self.searchFieldCategory.setFixedWidth(int(_width/6))
        self.searchFieldCategory.setPlaceholderText('Category')
        self.searchFieldWard = QLineEdit()
        self.searchFieldWard.setFixedWidth(int(_width/6))
        self.searchFieldWard.setPlaceholderText('Ward')
        self.searchFieldStreetName = QLineEdit()
        self.searchFieldStreetName.setFixedWidth(int(_width/6))
        self.searchFieldStreetName.setPlaceholderText('Street name')
        self.searchFieldAcreage = QLineEdit()
        self.searchFieldAcreage.setFixedWidth(int(_width/6))
        self.searchFieldAcreage.setPlaceholderText('Acreage')
        self.searchFieldPrice = QLineEdit()
        self.searchFieldPrice.setFixedWidth(int(_width/6))
        self.searchFieldPrice.setPlaceholderText('Price')

        self.centralLayout.addWidget(self.searchFieldId)
        self.centralLayout.addWidget(self.searchFieldCategory)
        self.centralLayout.addWidget(self.searchFieldWard)
        self.centralLayout.addWidget(self.searchFieldStreetName)
        self.centralLayout.addWidget(self.searchFieldAcreage)
        self.centralLayout.addWidget(self.searchFieldPrice)
        self.setLayout(self.centralLayout)

class SortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, *args, **kwargs):
        QSortFilterProxyModel.__init__(self, *args, **kwargs)
        self.filters = {}

    def setFilterByColumn(self, regex, column):
        self.filters[column] = regex
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        for key, regex in self.filters.items():
            ix = self.sourceModel().index(source_row, key, source_parent)
            if ix.isValid():
                text = self.sourceModel().data(ix)
                if text:
                    if regex not in text:
                        return False
        return True

class LoadingScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 200)

        self.labelAnimation = QLabel(self)
        self.movie = QMovie(_getExactlyPath(PATH_LOADING_ANIMATION))
        self.labelAnimation.setMovie(self.movie)
        self.movie.start()