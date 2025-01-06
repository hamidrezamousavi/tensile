
from PyQt5.QtWidgets import (
    QMainWindow,
    QPushButton,
    QLabel,
    QGridLayout,
    QWidget,
    QTableWidget,
    QLineEdit,
    QFileDialog,
    QRadioButton,
    QButtonGroup,
    QGroupBox,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QToolBar,
    QAction,
    QApplication,
    QLabel,
    QTableWidgetItem,

)
from PyQt5.QtCore import  Qt, QSize
from PyQt5.QtGui import QIcon,QCursor
from resultgraph import Graph
from data import data
from engineering import (
    convert_to_force_displacement,
    convert_to_eng_stress_strain,
    conver_to_real_stress_strain,
)
from widgets import ( 
InputLabel,
InputLine,
ResultsTable,
TwoRadioGroup,
)


class TestWindow(QMainWindow):
    def __init__(self,data):
        super().__init__()
        
        self.data = data
        self.width = 0
        self.thickness = 0
        self.extl0 = 0
        self.r100l0 = 0 
        self.setWindowTitle("Result")
        self.setGeometry(110, 110, 900, 700)
        
        self.thickness_label = InputLabel('Thickness')
        self.thickness_input = InputLine('')
        self.thickness_unit_label = InputLabel('mm')
        #self.thickness_layout = QHBoxLayout()
        #self.thickness_layout.addWidget(self.thickness_label)
        #self.thickness_layout.addWidget(self.thickness_input)


        self.width_label = InputLabel('Width')
        self.width_input = InputLine('')
        self.width_unit_label = InputLabel('mm')
        #self.width_layout = QHBoxLayout()
        #self.width_layout.addWidget(self.width_label)
        #self.width_layout.addWidget(self.width_input)

        self.extl0_label = InputLabel('Extension\'s L0')
        self.extl0_unit_label = InputLabel('mm')
        self.extl0_input = InputLine('')
        #self.extl0_layout = QHBoxLayout()
        #self.extl0_layout.addWidget(self.extl0_label)
        #self.extl0_layout.addWidget(self.extl0_input)

        self.r100l0_label = InputLabel('100R Extension L0')
        self.r100l0_unit_label = InputLabel('mm')
        self.r100l0_input = InputLine('')

        self.displacement_choice = TwoRadioGroup('Displacement Reading',
        'From Ext',1,'From 100R',2)


        self.graph1 = Graph()
        self.graph2 = Graph()
        self.graph3 = Graph()

      #  self.dispalcement_choice.addWidget(QPushButton('sfsf'))

        #self.r100l0_layout = QHBoxLayout()
        #self.r100l0_layout.addWidget(self.r100l0_label)
        #self.r100l0_layout.addWidget(self.r100l0_input)
        
        #self.input_section_layout = QVBoxLayout()
        #self.input_section_layout.addLayout(self.width_layout)
        #self.input_section_layout.addLayout(self.thickness_layout)
        #self.input_section_layout.addLayout(self.extl0_layout)
        #self.input_section_layout.addLayout(self.r100l0_layout)

        #self.graph_layout = QVBoxLayout()
        #self.graph_layout.addWidget(self.graph1)
        #self.graph_layout.addWidget(self.graph2)
        #self.graph_layout.addWidget(self.graph3)


        #self.upper_layout = QHBoxLayout()
        #self.upper_layout.addLayout(self.input_section_layout)
        #self.upper_layout.addLayout(self.graph_layout)
        self.table = ResultsTable(['Strenght', 'elongation'],[1.232, 10.1])
        self.show_graph_button = QPushButton('Show Graph')
        self.show_graph_button.clicked.connect(self.show_graph)
        self.layout = QGridLayout()
        
        
        self.layout.addWidget(self.thickness_label,0,0)
        self.layout.addWidget(self.thickness_input,0,1)
        self.layout.addWidget(self.thickness_unit_label,0,2)
        self.layout.addWidget(self.width_label,1,0)
        self.layout.addWidget(self.width_input,1,1)
        self.layout.addWidget(self.width_unit_label,1,2)
        self.layout.addWidget(self.extl0_label,2,0)
        self.layout.addWidget(self.extl0_input,2,1)
        self.layout.addWidget(self.extl0_unit_label,2,2)
        self.layout.addWidget(self.r100l0_label,3,0)
        self.layout.addWidget(self.r100l0_input,3,1)
        self.layout.addWidget(self.r100l0_unit_label,3,2)
        self.layout.addLayout(self.displacement_choice,4,0)

        self.layout.addWidget(self.graph1,0,3,5,5)
        self.layout.addWidget(self.graph2,5,3,1,5)
        self.layout.addWidget(self.graph3,10,3,1,5)
        self.layout.addWidget(self.table, 15,0,4,8)
        self.layout.addWidget(self.show_graph_button,5,0)
       # self.layout.setRowStretch(5,9)

        
        self.w = QWidget()
        self.w.setLayout(self.layout)
        self.setCentralWidget(self.w)
   # def keyPressEvent(self,e):
   #     self.width = self.width_input.text()
   #     self.thickness = self.thickness_input.text()
   #     self.extl0 = self.extl0_input.text()
   #     self.r100l0 = self.r100l0_input.text()
    def show_graph(self):
        self.width = 0
        self.thickness = 0
        self.extl0 = 0
        self.r100l0 = 0
        try:
            self.width = float(self.width_input.text())
        except Exception :
            pass
        try:    
            self.thickness = float(self.thickness_input.text())
        except Exception:
            pass
        try:
            self.extl0 = float(self.extl0_input.text())
        except Exception:
            pass
        try:
            self.r100l0 = float(self.r100l0_input.text())
        except Exception:
            pass


        force_displacement = convert_to_force_displacement(
                               data  = data,
                               width = self.width,
                               thickness = self.thickness,
                               extl0 = self.extl0,
                               r100l0 = self.r100l0,
                               displacement_choice = self.displacement_choice.check_id()
                               )
        self.graph1.refresh(
                           data = force_displacement, 
                           title = 'Force Displacement',
                           x_ax_label = 'Displacement (mm)',
                           y_ax_label= ' Force (N)')
       
        eng_stress_strain = convert_to_eng_stress_strain(
                               data = data,
                               width = self.width,
                               thickness = self.thickness,
                               extl0 = self.extl0,
                               r100l0 = self.r100l0,
                               displacement_choice = self.displacement_choice.check_id()
                               )
        self.graph2.refresh(data = eng_stress_strain, 
                           title = 'Engineering Stress Strain',
                           x_ax_label = 'Strain (mm/mm)',
                           y_ax_label= ' Stress (Mpa)')
       
        
        real_stress_strain = conver_to_real_stress_strain(
                               data = data,
                               width = self.width,
                               thickness = self.thickness,
                               extl0 = self.extl0,
                               r100l0 = self.r100l0,
                               displacement_choice = self.displacement_choice.check_id()
                               )
        self.graph3.refresh(data = real_stress_strain, 
                           title = 'Real Stress Strain',
                           x_ax_label = 'Strain (mm/mm)',
                           y_ax_label= ' Stress (Mpa)')
     

if __name__ == '__main__':
    app = QApplication([])
    
#qtmodern.styles.dark(app)

#window = qtmodern.windows.ModernWindow(MainWindow())
    window =TestWindow(data)
    window.show()
    app.exec_()