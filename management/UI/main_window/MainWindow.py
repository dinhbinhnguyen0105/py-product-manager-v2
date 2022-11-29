from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt

from .sidebar.Sidebar import SideBar
from .central.Central import Central
from ..dialog.create.Create import Create
from ..dialog.productTemplate.ProductTemplate import ProductTemplate
from ..dialog.robotControl import RobotControl

SIZE_WIDTH = 1400
SIZE_HEIGHT = int(SIZE_WIDTH/1.618) + 100

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Product management')
        self.setFixedSize(SIZE_WIDTH, SIZE_HEIGHT)

        self.centralWidget = QWidget()
        self.centralLayout = QHBoxLayout()

        self.sidebar = SideBar(self)
        self.central = Central(self)
        self.createDialog = Create()
        self.productTemplateDialog = ProductTemplate()
        self.robotControlDialog = RobotControl()

        self.centralLayout.addWidget(self.sidebar)
        self.centralLayout.addWidget(self.central)
        self.centralWidget.setLayout(self.centralLayout)
        self.setCentralWidget(self.centralWidget)
        self._onButtonClick()
        self.__setStyle()

    def __setStyle(self):
        self.centralLayout.setContentsMargins(0,0,0,0)
        self.centralLayout.setAlignment(self.sidebar, Qt.AlignmentFlag.AlignLeft)
        self.setStyleSheet('background-color: white;')

    def _onButtonClick(self):
        def __onBtnCreateNewListing():
            self.createDialog.show()
        def __onBtnProductTemplate():
            self.productTemplateDialog.show()
            self.productTemplateDialog.isShowed.emit(True)
        def __onBtnRobotControl():
            self.robotControlDialog.show()
            self.robotControlDialog.isShowed.emit(True)
            

        self.sidebar.btnCreateNewListing.clicked.connect(lambda : __onBtnCreateNewListing())
        self.sidebar.btnProductTemplate.clicked.connect(lambda : __onBtnProductTemplate())
        self.sidebar.btnRobotControl.clicked.connect(lambda : __onBtnRobotControl())
