from PyQt5.QtWidgets import (
    QMainWindow,
    QFrame,
    QGridLayout,
    QWidget,
    QLabel,
    QRadioButton,
    QButtonGroup,
    QVBoxLayout,

)
from PyQt5 import QtCore

class TopQRadioButton(QRadioButton):
    def __init__(self, text):
        super().__init__()
    #   # self.frame.setStyleSheet("background-color: yellow;")
        frame_T = QFrame(self)  
    #    #frame_T.setGeometry(130, 5, 50, 50)
        label_TOP = QLabel("dfsdf")
    #   # label_TOP.setFixedWidth(30)             # set a fix width to show up the TOP frame
    #    r_btn_TOP = QRadioButton()
        lay_VERT_TOP = QVBoxLayout()
       # lay_VERT_TOP.addWidget(frame_T)
        lay_VERT_TOP.addWidget(label_TOP)
        self.setLayout(lay_VERT_TOP)
    #    lay_VERT_TOP.addWidget(r_btn_TOP)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 900, 700)
        self.layout = QGridLayout()
        self.b1 = TopQRadioButton('text')
      
        self.layout.addWidget(self.b1 )
        self.b2 = QRadioButton('test2')
        self.layout.addWidget(self.b2 )
        self.group1 = QButtonGroup()
        self.group1.addButton(self.b1)
        self.group1.addButton(self.b2)
        self.b3 = QRadioButton('test3')
        self.layout.addWidget(self.b3 )
        self.b4 = QRadioButton('test4')
        self.layout.addWidget(self.b4 )

        self.w = QWidget()
        self.w.setLayout(self.layout)
        self.setCentralWidget(self.w)
from PyQt5.QtWidgets import QApplication



app = QApplication([])


window = MainWindow()

window.show()
app.exec_()    

