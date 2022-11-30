import random
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPushButton,
    QPlainTextEdit
)
from PyQt6.QtGui import QIcon

from ....CONSTANTS import PATH_ICON_AUTO, ICONS
from ....helper import _getExactlyPath

class InitItem(QDialog):
    def __init__(self, payload, parent=None):
        super().__init__(parent)
        self.payload = payload
        self.mainLayout = QVBoxLayout()

        self.item = QPlainTextEdit()
        self._item = Item(payload)
        self.item.setPlainText(self._item.init())

        self.btnRefresh = QPushButton('Refresh')
        self.btnRefresh.clicked.connect(lambda : self._onClickBtnRefresh())

        self.mainLayout.addWidget(self.item)
        self.mainLayout.addWidget(self.btnRefresh)
        self.setLayout(self.mainLayout)
        self._setStyle()
    
    def _setStyle(self):
        _id = self.payload['ID']
        self.setWindowTitle(f'{_id}')
        self.setStyleSheet('background-color: white;')
        iconURL = _getExactlyPath(PATH_ICON_AUTO)
        self.setWindowIcon(QIcon(iconURL))
        self.setFixedSize(500, 900)
        self.mainLayout.setContentsMargins(0,0,0,0)

    def _onClickBtnRefresh(self):
        self.item.setPlainText(self._item.init())
        pass

class Item():
    def __init__(self, payload) -> None:
        self._category = payload['Category']
        self._district = payload['District']
        self._ward = payload['Ward']
        self._street = payload['Street name']
        self._buildingLine = payload['Building line']
        self._acreage = payload['Acreage']
        self._construction = payload['Construction']
        self._function = payload['Function']
        self._fuiture = payload['Fuiture']
        self._legal = payload['Legal']
        self._price = payload['Price']
        self._desciption = payload['Description']
    
    def header(self):
        header = [
            'bán',
            'hạ giá',
            'hạ giá bán nhanh',
            'giá trong tháng',
            'hạ giá trong tuần',
            'bán nhanh',
            'bán gấp',
            'giá đầu tư',
            'giá cực mềm',
            'giá mềm nhất',
            'giá HOT',
            f'bán {self._category}',
            f'hạ giá {self._category}',
            f'hạ giá {self._category} bán nhanh',
            f'hạ giá {self._category} trong tuần',
            f'bán nhanh {self._category}',
            f'bán {self._category} giá rẻ',
            f'bán {self._category} giá đầu tư',
            f'{self._category} {self._ward}',
            f'chỉ {self._price} tỷ',
        ]
        return header[random.randint(0, len(header) -1)].upper()

    def desc(self):
        def home():
            d1 = f'Bán gấp nhà {self._ward} chỉ {self._price} tỷ\n\n🗺 Vị trí: {self._ward}, TP. {self._district}\n📏 Diện tích: {self._acreage} m2.\n🏚 Kết cấu: {self._construction}\n🛌 Công năng: {self._function}\n📺 Nội thất: {self._fuiture}\n{ICONS[random.randint(0, len(ICONS) - 1)]}{ICONS[random.randint(0, len(ICONS) - 1)]} Mô tả: {self._desciption}\n💲 Giá: {self._price} tỷ - Thương lượng chính chủ\n☎ Liên hệ: 0375155525 - Đ. Bình\n'
            d2 = f'{ICONS[random.randint(0, len(ICONS) - 1)]*4}Bán gấp nhà {self._ward} chỉ {self._price} tỷ{ICONS[random.randint(0, len(ICONS) - 1)]*4}\n\n{ICONS[random.randint(0, len(ICONS) - 1)]*2} Vị trí: {self._ward}, TP. {self._district}\n{ICONS[random.randint(0, len(ICONS) - 1)]*2} Diện tích: {self._acreage} m2.\n{ICONS[random.randint(0, len(ICONS) - 1)]*2} Kết cấu: {self._construction}\n{ICONS[random.randint(0, len(ICONS) - 1)]*2}Công năng: {self._function}\n{ICONS[random.randint(0, len(ICONS) - 1)]*2} Nội thất: {self._fuiture}\n{ICONS[random.randint(0, len(ICONS) - 1)]}{ICONS[random.randint(0, len(ICONS) - 1)]} Mô tả: {self._desciption}\n{ICONS[random.randint(0, len(ICONS) - 1)]*2} Giá: {self._price} tỷ - Thương lượng chính chủ\n{ICONS[random.randint(0, len(ICONS) - 1)]*2} Liên hệ: 0375155525 - Đ. Bình\n'
            d3 = f'{ICONS[random.randint(0, len(ICONS) - 1)]*4}Cần bán gấp nhà nhà{self._ward} chỉ {self._price} tỷ{ICONS[random.randint(0, len(ICONS) - 1)]*4}\n\n{ICONS[random.randint(0, len(ICONS) - 1)]*2} Vị trí: {self._ward}, TP. {self._district}\n{ICONS[random.randint(0, len(ICONS) - 1)]*2} Diện tích: {self._acreage} m2.\n{ICONS[random.randint(0, len(ICONS) - 1)]*2} Kết cấu: {self._construction}\n{ICONS[random.randint(0, len(ICONS) - 1)]*2}Công năng: {self._function}\n{ICONS[random.randint(0, len(ICONS) - 1)]*2} Nội thất: {self._fuiture}\n{ICONS[random.randint(0, len(ICONS) - 1)]}{ICONS[random.randint(0, len(ICONS) - 1)]} Mô tả: {self._desciption}\n{ICONS[random.randint(0, len(ICONS) - 1)]*2} Giá: {self._price} tỷ - Thương lượng chính chủ\n{ICONS[random.randint(0, len(ICONS) - 1)]*2} Liên hệ: 0375155525 - Đ. Bình\n'
            des = [d1, d2]
            return des[random.randint(0, len(des) - 1)]
        def area():
            d1 = f'{random.randint(0, len(ICONS) - 1)}Bán gấp lô đất {self._ward} chỉ {self._price} tỷ\n\n🗺 Vị trí: {self._ward}, TP. {self._district}\n📏 Diện tích: {self._acreage} m2.\n{ICONS[random.randint(0, len(ICONS) - 1)]}{ICONS[random.randint(0, len(ICONS) - 1)]} Mô tả: {self._desciption}\n💲 Giá: {self._price} tỷ - Thương lượng chính chủ\n☎ Liên hệ: 0375155525 - Đ. Bình\n'
            return d1
        if self._category == 'Nhà riêng':
            return home()
        elif self._category == 'Đất':
            return area

    def init(self):
        return self.header() + '\n\n' + self.desc()
