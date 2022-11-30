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
from ...CONSTANTS import (
    WIDTH_MAIN,
    HEIGHT_MAIN,
    WIDTH_SIZEBAR,
    HEIGHT_SIZEBAR,
)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Product management')
        self.setFixedSize(WIDTH_MAIN, HEIGHT_MAIN)

        self.centralWidget = QWidget()
        self.centralLayout = QHBoxLayout()

        self.sidebar = SideBar(self)
        self.central = Central(self)
        self.createDialog = Create()
        self.productTemplateDialog = ProductTemplate()
        self.robotControlDialog = RobotControl()

        self.sidebar.setFixedWidth(WIDTH_SIZEBAR)
        self.central.setFixedWidth(WIDTH_MAIN-WIDTH_SIZEBAR)
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
