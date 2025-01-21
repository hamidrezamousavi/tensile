from PyQt5.QtWidgets import (
    QPushButton,
    QLabel,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QButtonGroup,
    QRadioButton,
    QGridLayout,
    QGroupBox,
   )
from PyQt5.QtCore import  Qt, QSize
from PyQt5.QtGui import QIcon,QCursor


class InputLabel(QLabel):
    def __init__(self,label):
        super().__init__(label)
        self.setStyleSheet("""
        font-size:18px;
        font-family: 'Courier New';
        """)
class InputLine(QLineEdit):
    def __init__(self,*arg):
        super().__init__(*arg)
        self.setStyleSheet("""
        font-size:20px;
        font-family: 'Courier New';
        background: rgb(30,30,30);
        color: white;
        """)
        self.setFixedSize(QSize(90,30))
        self.returnPressed.connect(self.return_press)
    def return_press(self):
        self.focusNextChild()

class UpTriAngleButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setCheckable(True)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFixedSize(QSize(90,90))
        self.setStyleSheet("""
        background-color:  rgba(0, 0, 0, 0) ;
        """);
        self.setIconSize(QSize(90,90))
        self.setIcon(QIcon('upOff.png'))

    def refresh(self):
        if self.isChecked():
            self.setIcon(QIcon('upOn.png'))
        else:
            self.setIcon(QIcon('upOff.png'))
       
        
class DownTriAngleButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setCheckable(True)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFixedSize(QSize(90,90))
        self.setStyleSheet("""
        background-color:  rgba(0, 0, 0, 0) ;
        """);
        self.setIconSize(QSize(90,90))
        self.setIcon(QIcon('downOff.png'))
  
    def refresh(self):
        if self.isChecked():
            self.setIcon(QIcon('downOn.png'))
        else:
            self.setIcon(QIcon('downOff.png'))

class BlackLabel(QLabel):
    def __init__(self,text):
        super().__init__(text)
        self.setStyleSheet("""
        background: rgba(0,0,0,20);
        color:rgba(255,255,255,180);
        font-size:14pt;
        font-family: 'Courier New';
        border: 0;
        """)
class BorderlessGroupBox(QGroupBox):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""border: 0;""")


class ResultsTable(QTableWidget):
    def __init__(self,):
        super().__init__()

        #self.verticalHeader().setHidden(True)
   
    def set_value(self,labels= None, data = None,eng_stress_strain = None ):
            self.refresh()
            self.setRowCount(len(data))
            self.labels = labels
            self.data = data
            self.setColumnCount(len(self.labels))
            self.setHorizontalHeaderLabels(self.labels)


            for i,item in enumerate(data):
                self.setItem(i,0,QTableWidgetItem(str(item.ext)))
                self.setItem(i,1,QTableWidgetItem(str(item.r100)))
                self.setItem(i,2,QTableWidgetItem(str(item.force)))

            if not eng_stress_strain:
                return

            self.strains = eng_stress_strain.curve[0]
            self.stresses = eng_stress_strain.curve[1]

            for i,item in enumerate(self.strains):
                self.setItem(i,3,QTableWidgetItem(f'{item:0.5f}'))
            for i,item in enumerate(self.stresses):
                self.setItem(i,4,QTableWidgetItem(f'{item:0.3f}'))
    def refresh(self):
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                self.setItem(i, j, None)


class TwoRadioGroup(QGridLayout):
    def __init__(self,header,first_radio_name,first_radio_id, 
                      second_radio_name, second_radio_id):
        super().__init__()
        self.header = InputLabel(header)
        self.first_radio = QRadioButton(first_radio_name)
        self.second_radio = QRadioButton(second_radio_name)
        self.addWidget(self.header,0,0)
        self.addWidget(self.first_radio,1,0)
        self.addWidget(self.second_radio,1,1)
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.first_radio)
        self.button_group.addButton(self.second_radio)
        self.button_group.setId(self.first_radio,first_radio_id)
        self.button_group.setId(self.second_radio,second_radio_id)
        self.first_radio.setChecked(True)

        self.button_group.setExclusive(True)

    def check_id(self):
        return self.button_group.checkedId()



