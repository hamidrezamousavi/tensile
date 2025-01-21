from PyQt5.QtWidgets import (
    QMainWindow,
    QPushButton,
    QGridLayout,
    QWidget,
    QFileDialog,
    QToolBar,
    QAction,
    QApplication,
)
from PyQt5.QtGui import QIcon,QCursor
from resultgraph import Graph, GraphEnhanced
from engineering import (
    force_displacement_calculatoin,
    eng_stress_strain_calculatoin,
    real_stress_strain_calculatoin,
)
from widgets import ( 
InputLabel,
InputLine,
ResultsTable,
TwoRadioGroup,
)
import util
class ResultWindow(QMainWindow):
    def __init__(self,data = None):
        super().__init__()
        self.data = data
        self.width = 0
        self.thickness = 0
        self.extl0 = 0
        self.r100l0 = 0 
        self.setWindowTitle("Result")
        self.setGeometry(110, 110, 900, 700)
        self.tool_bar = QToolBar()
        self.addToolBar(self.tool_bar)
        self.save_action = QAction(text='Save Result', icon=QIcon('save1.png'))
        self.save_action.triggered.connect(self.save_result)
        self.tool_bar.addAction(self.save_action)
        self.print_action = QAction(text='print', icon=QIcon('print.png'))
        self.print_action.triggered.connect(self.print_result)
        self.tool_bar.addAction(self.print_action)
        self.load_action = QAction(text='Load Previous Result', icon=QIcon('load.png'))
        self.load_action.triggered.connect(self.load_result)
        self.tool_bar.addAction(self.load_action)
        self.thickness_label = InputLabel('Thickness')
        self.thickness_input = InputLine('')
        self.thickness_input.textChanged.connect(self.take_input)
        self.thickness_unit_label = InputLabel('mm')
        self.width_label = InputLabel('Width')
        self.width_input = InputLine('')
        self.width_input.textChanged.connect(self.take_input)
        self.width_unit_label = InputLabel('mm')
        self.extl0_label = InputLabel('Extension\'s L0')
        self.extl0_unit_label = InputLabel('mm')
        self.extl0_input = InputLine('')
        self.extl0_input.textChanged.connect(self.take_input)
        self.r100l0_label = InputLabel('100R Extension L0')
        self.r100l0_unit_label = InputLabel('mm')
        self.r100l0_input = InputLine('')
        self.r100l0_input.textChanged.connect(self.take_input)

        self.displacement_choice = TwoRadioGroup('Displacement Reading',
        'From Ext',1,'From 100R',2)

        self.graph1 = Graph()
        self.graph2 = GraphEnhanced()
       # self.graph3 = GraphEnhanced()
        self.table = ResultsTable()
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
        self.layout.setRowStretch(4,0)

        self.layout.addWidget(self.graph1,0,3,7,5)
        self.layout.addWidget(self.graph2,7,3,1,5)
      #  self.layout.addWidget(self.graph3,10,3,1,5)
        self.layout.addWidget(self.table, 7,0,1,3)
        self.layout.addWidget(self.show_graph_button,6,0)
        self.w = QWidget()
        self.w.setLayout(self.layout)
        self.setCentralWidget(self.w)
    def take_input(self):
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

    def show_graph(self):
        force_displacement = force_displacement_calculatoin(
                               data  = self.data,
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
       
        eng_stress_strain = eng_stress_strain_calculatoin(
                               data = self.data,
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


        real_stress_strain = real_stress_strain_calculatoin(
                               data = self.data,
                               width = self.width,
                               thickness = self.thickness,
                               extl0 = self.extl0,
                               r100l0 = self.r100l0,
                               displacement_choice = self.displacement_choice.check_id()
                               )
  #      self.graph3.refresh(data = real_stress_strain,
  #                         title = 'Real Stress Strain',
  #                         x_ax_label = 'Strain (mm/mm)',
  #                         y_ax_label= ' Stress (Mpa)')
  #
        self.table.set_value(
            ['Ext', 'R100','Force','Strain','Stress'],
            self.data, eng_stress_strain
            )

    def refresh_input(self):
        width = str(self.width)
        thickness = str(self.thickness)
        extl0 = str(self.extl0)
        r100l0 = str(self.r100l0)
        self.thickness_input.setText(width)
        self.width_input.setText(thickness)
        self.extl0_input.setText(extl0)
        self.r100l0_input.setText(r100l0)

    def save_result(self):
        self.file_dialog = QFileDialog()
        self.file_path = self.file_dialog.getSaveFileName()[0]
        if not self.file_path:
            return
        if not self.file_path.endswith('.txt'):
            self.file_path += '.txt'

        with open(self.file_path, 'w') as file_obj:
            util.write_data(file_obj, width= self.width,
                                 thickness = self.thickness,
                                 extl0 = self.extl0,
                                 r100l0 = self.r100l0,
                                 data = self.data,
                                 )
    def load_result(self):
        self.file_dialog = QFileDialog()
        self.file_path = self.file_dialog.getOpenFileName( filter="Text (*.txt);;All  (*.*)")[0]

        with open(self.file_path, 'r')as file_obj:
            self.width, self.thickness, self.extl0, self.r100l0 = util.read_header(file_obj)
            print(self.width, self.thickness, self.extl0, self.r100l0)
            self.refresh_input()

            _ = file_obj.readline()  # skip title of data
            self.data.clear()
            for item in util.read_fer(file_obj):
                self.data.append(item)
            self.show_graph()


    def print_result(self):
        print('print')


if __name__ == '__main__':
    app = QApplication([])
    window =ResultWindow([])
    window.show()
    app.exec_()