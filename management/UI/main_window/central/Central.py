from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
)
from .ListProduct import ListProduct
from .DetailProduct import DetailProduct

class Central(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setFixedSize(int(self.parent().width()*0.8), self.parent().height())
        self.centralLayout = QVBoxLayout()
        self.listProduct = ListProduct(self)
        self.listProduct.setFixedSize(int(self.parent().width()), int(self.parent().height()*0.5))

        self.detailProduct = QWidget()     

        self.listProduct.currentProductChanged.connect(self.displayCurrentProduct)

        self.centralLayout.addWidget(self.listProduct)
        self.setLayout(self.centralLayout)

    def displayCurrentProduct(self, e):
        if self.detailProduct:
            self.centralLayout.removeWidget(self.detailProduct)
            self.detailProduct.deleteLater()
        self.detailProduct  = DetailProduct(e, self)

        self.centralLayout.addWidget(self.detailProduct)