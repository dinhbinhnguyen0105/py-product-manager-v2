from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
)
from .DropDownMenu import DropDownMenu
from .LineText import LineText
from .PlainText import PlainText
from ....CONSTANTS import PATH_CREATE_CONFIG
from ....helper import _importDataConfig

class InputField(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QGridLayout()

        data = _importDataConfig(PATH_CREATE_CONFIG)
        self.category = DropDownMenu(data['category']['label'], 'category', data['category']['items'], data['category']['defaul_item'])
        
        self.city = DropDownMenu(data['city']['label'], 'city', data['city']['items'], data['city']['defaul_item'])
        self.district = DropDownMenu(data['district']['label'], 'district', data['district']['items'], data['district']['defaul_item'])
        self.ward = DropDownMenu(data['ward']['label'], 'ward', data['ward']['items'], data['ward']['defaul_item'])
        self.streetName = LineText(data['street_name']['label'], 'street_name', data['street_name']['prev_value'], data['street_name']['placeholder'])

        self.buildingLine = DropDownMenu(data['building_line']['label'], 'buildingLine', data['building_line']['items'], data['building_line']['defaul_item'])
        self.acreage = LineText(data['acreage']['label'], 'acreage', data['acreage']['prev_value'], data['acreage']['placeholder'])

        self.construction = LineText(data['construction']['label'], 'construction', data['construction']['prev_value'], data['construction']['placeholder'])
        self.function = LineText(data['function']['label'], 'function', data['function']['prev_value'], data['function']['placeholder'])

        self.fuiture = DropDownMenu(data['fuiture']['label'], 'fuiture', data['fuiture']['items'], data['fuiture']['defaul_item'])
        self.legal = DropDownMenu(data['legal']['label'], 'legal', data['legal']['items'], data['legal']['defaul_item'])

        self.price = LineText(data['price']['label'], 'price', data['price']['prev_value'], data['price']['placeholder'])

        self.description = PlainText(data['description']['label'], 'description', data['description']['prev_value'], data['description']['placeholder'])
        self.source = LineText(data['source']['label'], 'source', data['source']['prev_value'], data['source']['placeholder'])
        
        layout.addWidget(self.category, 0, 0, 1, 2)
        layout.addWidget(self.city, 1, 0, 1, 1)
        layout.addWidget(self.district, 1, 1, 1, 1)
        layout.addWidget(self.ward, 2, 0, 1, 1)
        layout.addWidget(self.streetName, 2, 1, 1, 1)
        layout.addWidget(self.buildingLine, 3, 0 , 1, 1)
        layout.addWidget(self.acreage, 3, 1 , 1, 1)
        layout.addWidget(self.construction, 4, 0 , 1, 1)
        layout.addWidget(self.function, 4, 1 , 1, 1)
        layout.addWidget(self.fuiture, 5, 0 , 1, 1)
        layout.addWidget(self.legal, 5, 1 , 1, 1)
        layout.addWidget(self.price, 6, 0 , 1, 1)
        layout.addWidget(self.description, 7, 0, 1, 2)
        layout.addWidget(self.source, 8, 0, 1, 2)

        self.setLayout(layout)

    def _getValues(self):
        data = {}
        data.update(self.category._getValue())
        data.update(self.city._getValue())
        data.update(self.district._getValue())
        data.update(self.ward._getValue())
        data.update(self.streetName._getValue())
        data.update(self.buildingLine._getValue())
        data.update(self.acreage._getValue())
        data.update(self.construction._getValue())
        data.update(self.function._getValue())
        data.update(self.fuiture._getValue())
        data.update(self.legal._getValue())
        data.update(self.price._getValue())
        data.update(self.description._getValue())
        data.update(self.source._getValue())
        return data

    def _resetValues(self):
        self.streetName._setValue()
        self.acreage._setValue()
        self.construction._setValue()
        self.function._setValue()
        self.price._setValue()
        self.description._setValue()
        self.source._setValue()
        pass

