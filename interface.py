from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QComboBox
from PyQt6.QtCore import Qt, QLocale
from PyQt6.QtGui import QGuiApplication, QDoubleValidator
from tags_and_info import getECBEuro
from decimal import Decimal as dec

DVALIDATOR = QDoubleValidator()
DVALIDATOR.setLocale(QLocale(QLocale.Language.English, QLocale.Country.AnyCountry))

class EuroInterface(QWidget):
    def __init__(self):
        super(EuroInterface, self).__init__()
        self.values = getECBEuro()
        self.setWindowTitle("Euro Based Currency Converter")
        x, y = self.centerWidgetCoord()
        self.setGeometry(x, y, 800, 600)
        self.setWidgets()
        self.currency_value = 1
                
        self.combo_box_A.currentIndexChanged.connect(self.currAdjustA)
        self.combo_box_B.currentIndexChanged.connect(self.currAdjustB)
        self.combo_box_A.currentIndexChanged.connect(self.setBoxesEmpty)
        self.combo_box_B.currentIndexChanged.connect(self.setBoxesEmpty)
        self.combo_box_A.currentIndexChanged.connect(self.setConvLabel)
        self.combo_box_B.currentIndexChanged.connect(self.setConvLabel)
        self.edit_value_A.textChanged.connect(self.boxValueA)
        self.edit_value_B.textChanged.connect(self.boxValueB)
        
    def centerWidgetCoord(self):
        available_screens = QGuiApplication.screens()
        screen_geometry = available_screens[0].availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        return x, y

    def setWidgets(self):
        layout = QVBoxLayout(self)
        title_layout = QVBoxLayout()
        options_layout = QGridLayout()
                
        self.title(title_layout)
        self.showRatingLabel(options_layout)
        self.currOptionA(options_layout)
        self.setToSpace(options_layout)
        self.currOptionB(options_layout)
        self.showCurrValue(options_layout)
        self.showConversionLabel(options_layout)
        self.editBoxes(options_layout)
        
        layout.addLayout(title_layout)      
        layout.addLayout(options_layout)
        layout.setSpacing(20)
        layout.setStretch(0, 0)
        layout.addStretch()
                
    def title(self, layout):
        self.label_title = QLabel("Euro Based Currency Converter")
        self.label_title.setStyleSheet("font-size: 24px; background-color: #f0f0f0; color: #ebab34;")
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.label_title)
                
    def currOptionA(self, layout):
        self.combo_box_A = QComboBox(self)
        for value in self.values:
            contents = self.values[value]
            self.combo_box_A.addItem(f'{value} - {contents[0]}')
        layout.addWidget(self.combo_box_A, 1, 0)
        
    def currOptionB(self, layout):
        self.combo_box_B = QComboBox(self)
        for value in self.values:
            contents = self.values[value]
            self.combo_box_B.addItem(f'{value} - {contents[0]}') 
        layout.addWidget(self.combo_box_B, 1, 2)
     
    def setToSpace(self, layout):
        self.adjacent_label = QLabel("<center>to<center>")
        self.adjacent_label.setFixedWidth(100)
        self.adjacent_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.adjacent_label, 1, 1)
        
    def showCurrValue(self, layout):
        self.curr_value_label = QLabel('<center> 1 <center>')
        self.curr_value_label.setFixedWidth(100)
        self.adjacent_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.curr_value_label, 1, 3)
        
    def showRatingLabel(self, layout):
        self.rate_label = QLabel('<center> Rating <center>')
        self.rate_label.setStyleSheet("font-size: 18px; color: #3440eb;")
        self.rate_label.setFixedWidth(100)
        layout.addWidget(self.rate_label, 0, 3)
        
    def showConversionLabel(self, layout):
        self.rate_label = QLabel(f'<center>{self.combo_box_A.currentText()[:3]} To {self.combo_box_B.currentText()[:3]}<center>')
        self.setConvLabel()
        self.rate_label.setStyleSheet("font-size: 18px; color: #3440eb;")
        self.rate_label.setFixedWidth(100)
        layout.addWidget(self.rate_label, 2, 1)
        
    def setConvLabel(self):
        self.rate_label.setText(f'<center>{self.combo_box_A.currentText()[:3]} To {self.combo_box_B.currentText()[:3]}<center>')
        
    def editBoxes(self, layout):
        self.edit_value_A = QLineEdit()
        self.edit_value_A.setValidator(DVALIDATOR)
        self.edit_value_B = QLineEdit()
        self.edit_value_B.setValidator(DVALIDATOR)
        
        layout.addWidget(self.edit_value_A, 3, 0)
        layout.addWidget(self.edit_value_B, 3, 2)
        
    def boxValueA(self):
        if self.edit_value_A.text():
            text = self.edit_value_A.text()
            self.edit_value_B.textChanged.disconnect(self.boxValueB)
            value = dec(text) * self.currency_value
            value_text = f"{value:.2f}"
            self.edit_value_B.setText(value_text)
            self.edit_value_B.textChanged.connect(self.boxValueB)
        else: self.edit_value_B.setText('')
        
    def boxValueB(self):
        if self.edit_value_B.text():
            text = self.edit_value_B.text()
            self.edit_value_A.textChanged.disconnect(self.boxValueA)
            value = dec(text) / self.currency_value
            value_text = f"{value:.2f}"
            self.edit_value_A.setText(value_text)
            self.edit_value_A.textChanged.connect(self.boxValueA)
        else: self.edit_value_A.setText('')
        
    def setBoxesEmpty(self):
        self.edit_value_A.setText('')
        self.edit_value_A.setText('')
                 
    def currAdjustA(self):
        if self.combo_box_A.currentText() != 'EUR - European euro':
            self.combo_box_B.setCurrentText('EUR - European euro')
        key = self.combo_box_A.currentText()[:3]
        self.currValue(key)
        self.curr_value_label.setText(f"<center> {str(self.currency_value.quantize(dec('0.000000')))} <center>")
        
    def currAdjustB(self):
        if self.combo_box_B.currentText() != 'EUR - European euro':
            self.combo_box_A.setCurrentText('EUR - European euro')
        key = self.combo_box_B.currentText()[:3]
        list_values = self.values[key]
        self.currency_value = dec(list_values[1])
        self.curr_value_label.setText(f"<center> {str(self.currency_value.quantize(dec('0.000000')))} <center>")
            
    def currValue(self, key):
        listv = self.values[key]
        value = 1 / dec(listv[1])
        self.currency_value = value
