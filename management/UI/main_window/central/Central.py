from PyQt6.QtWidgets import (
    QHBoxLayout,
    QWidget,
)
from .ListProduct import ListProduct
from .DetailProduct import DetailProduct

class Central(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.centralLayout = QHBoxLayout()
        self.listProduct = ListProduct(self)

        self.detailProduct = QWidget()     
        self.detailProduct.setFixedSize(int(self.parent().width()*0.3), self.parent().height())
        self.listProduct.currentProductChanged.connect(self.displayCurrentProduct)

        self.centralLayout.addWidget(self.listProduct)
        self.centralLayout.addWidget(self.detailProduct)

        self.setLayout(self.centralLayout)

    def displayCurrentProduct(self, e):
        if self.detailProduct:
            self.centralLayout.removeWidget(self.detailProduct)
            self.detailProduct.deleteLater()
        self.detailProduct  = DetailProduct(e, self)

        self.centralLayout.addWidget(self.detailProduct)